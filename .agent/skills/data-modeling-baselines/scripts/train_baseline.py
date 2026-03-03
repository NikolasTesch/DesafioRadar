#!/usr/bin/env python3
"""
Train baseline ML models for tabular datasets.

Usage:
    python train_baseline.py <dataset_path> --target <target_column> [--task auto|classification|regression] [--output result.json]
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import pandas as pd  # type: ignore
except Exception:
    pd = None

try:
    from sklearn.compose import ColumnTransformer  # type: ignore
    from sklearn.dummy import DummyClassifier, DummyRegressor  # type: ignore
    from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor  # type: ignore
    from sklearn.impute import SimpleImputer  # type: ignore
    from sklearn.linear_model import LinearRegression, LogisticRegression  # type: ignore
    from sklearn.metrics import (  # type: ignore
        accuracy_score,
        f1_score,
        mean_absolute_error,
        mean_squared_error,
        precision_score,
        r2_score,
        recall_score,
    )
    from sklearn.model_selection import train_test_split  # type: ignore
    from sklearn.pipeline import Pipeline  # type: ignore
    from sklearn.preprocessing import OneHotEncoder, StandardScaler  # type: ignore
except Exception:
    ColumnTransformer = None


def _load_dataset(path: Path, sheet: str | None, max_rows: int) -> "pd.DataFrame":
    ext = path.suffix.lower()
    if ext == ".csv":
        return pd.read_csv(path, nrows=max_rows)
    if ext in {".xlsx", ".xls"}:
        return pd.read_excel(path, sheet_name=sheet or 0, nrows=max_rows)
    if ext == ".parquet":
        return pd.read_parquet(path).head(max_rows)
    if ext == ".json":
        return pd.read_json(path).head(max_rows)
    raise ValueError(f"Unsupported extension: {ext}")


def _infer_task(y: "pd.Series", requested: str) -> str:
    if requested in {"classification", "regression"}:
        return requested
    if str(y.dtype) in {"object", "category", "bool"}:
        return "classification"
    unique = y.nunique(dropna=True)
    if unique <= 15:
        return "classification"
    return "regression"


def _build_preprocessor(x: "pd.DataFrame") -> tuple["ColumnTransformer", list[str], list[str]]:
    numeric_columns = x.select_dtypes(include=["number", "bool"]).columns.tolist()
    categorical_columns = [name for name in x.columns if name not in numeric_columns]

    numeric_pipe = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipe = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipe, numeric_columns),
            ("cat", categorical_pipe, categorical_columns),
        ]
    )
    return preprocessor, numeric_columns, categorical_columns


def _classification_scores(y_true: Any, y_pred: Any) -> dict[str, float]:
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "f1_weighted": float(f1_score(y_true, y_pred, average="weighted", zero_division=0)),
        "precision_weighted": float(precision_score(y_true, y_pred, average="weighted", zero_division=0)),
        "recall_weighted": float(recall_score(y_true, y_pred, average="weighted", zero_division=0)),
    }


def _regression_scores(y_true: Any, y_pred: Any) -> dict[str, float]:
    rmse = mean_squared_error(y_true, y_pred, squared=False)
    return {
        "rmse": float(rmse),
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "r2": float(r2_score(y_true, y_pred)),
    }


def run_baselines(
    dataset_path: Path,
    target: str,
    task: str,
    test_size: float,
    random_state: int,
    sheet: str | None,
    max_rows: int,
) -> dict[str, Any]:
    if pd is None or ColumnTransformer is None:
        raise RuntimeError(
            "Missing dependencies. Install with: pip install pandas scikit-learn openpyxl pyarrow"
        )

    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    frame = _load_dataset(dataset_path, sheet=sheet, max_rows=max_rows)
    if target not in frame.columns:
        raise ValueError(f"Target column not found: {target}")

    frame = frame.dropna(subset=[target]).copy()
    if frame.empty:
        raise ValueError("No rows left after dropping missing target values.")

    y = frame[target]
    x = frame.drop(columns=[target])

    inferred_task = _infer_task(y, task)
    preprocessor, numeric_columns, categorical_columns = _build_preprocessor(x)

    stratify = None
    if inferred_task == "classification":
        class_counts = y.value_counts(dropna=False)
        if len(class_counts) < 2:
            raise ValueError("Classification requires at least 2 target classes.")
        if int(class_counts.min()) >= 2:
            stratify = y

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=stratify,
    )

    if inferred_task == "classification":
        models = {
            "dummy_most_frequent": DummyClassifier(strategy="most_frequent"),
            "logistic_regression": LogisticRegression(max_iter=1000),
            "random_forest": RandomForestClassifier(
                n_estimators=250,
                random_state=random_state,
                n_jobs=-1,
            ),
        }
        metric_name = "f1_weighted"
        higher_is_better = True
    else:
        models = {
            "dummy_mean": DummyRegressor(strategy="mean"),
            "linear_regression": LinearRegression(),
            "random_forest": RandomForestRegressor(
                n_estimators=300,
                random_state=random_state,
                n_jobs=-1,
            ),
        }
        metric_name = "rmse"
        higher_is_better = False

    leaderboard: list[dict[str, Any]] = []
    for model_name, estimator in models.items():
        pipeline = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("model", estimator),
            ]
        )
        pipeline.fit(x_train, y_train)
        predictions = pipeline.predict(x_test)

        if inferred_task == "classification":
            metrics = _classification_scores(y_test, predictions)
        else:
            metrics = _regression_scores(y_test, predictions)

        leaderboard.append(
            {
                "model": model_name,
                "metrics": metrics,
            }
        )

    leaderboard.sort(
        key=lambda item: item["metrics"][metric_name],
        reverse=higher_is_better,
    )

    best = leaderboard[0]
    return {
        "tool": "train_baseline",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "dataset": str(dataset_path),
        "rows_used": int(len(frame)),
        "features_used": int(x.shape[1]),
        "target": target,
        "task": inferred_task,
        "metric_priority": metric_name,
        "train_rows": int(len(x_train)),
        "test_rows": int(len(x_test)),
        "numeric_features": numeric_columns,
        "categorical_features": categorical_columns,
        "leaderboard": leaderboard,
        "recommended_model": best["model"],
        "recommended_metric_value": best["metrics"][metric_name],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Train baseline models for tabular data.")
    parser.add_argument("dataset", help="Dataset path (csv/xlsx/parquet/json).")
    parser.add_argument("--target", required=True, help="Target column name.")
    parser.add_argument(
        "--task",
        default="auto",
        choices=["auto", "classification", "regression"],
        help="Task type. Use auto to infer from target.",
    )
    parser.add_argument("--test-size", type=float, default=0.2, help="Test split ratio.")
    parser.add_argument("--random-state", type=int, default=42, help="Random state.")
    parser.add_argument("--sheet", default=None, help="Sheet name/index for XLSX.")
    parser.add_argument("--max-rows", type=int, default=200000, help="Maximum rows to load.")
    parser.add_argument("--output", default=None, help="Optional JSON output path.")
    args = parser.parse_args()

    dataset_path = Path(args.dataset).resolve()
    output_path = Path(args.output).resolve() if args.output else None

    try:
        result = run_baselines(
            dataset_path=dataset_path,
            target=args.target,
            task=args.task,
            test_size=max(0.05, min(0.5, args.test_size)),
            random_state=args.random_state,
            sheet=args.sheet,
            max_rows=max(1, args.max_rows),
        )
    except Exception as exc:
        error_payload = {
            "tool": "train_baseline",
            "passed": False,
            "error": str(exc),
        }
        print(json.dumps(error_payload, indent=2))
        sys.exit(1)

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(json.dumps(result, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
