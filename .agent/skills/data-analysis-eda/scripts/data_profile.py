#!/usr/bin/env python3
"""
Data profiling utility for CSV/XLSX/Parquet/JSON tabular datasets.

Usage:
    python data_profile.py <dataset_path> [--sheet SHEET] [--max-rows 200000] [--output profile.json]
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import pandas as pd  # type: ignore
except Exception:
    pd = None


def _safe_float(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if text == "":
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _numeric_stats(values: list[float]) -> dict[str, float] | None:
    if not values:
        return None
    ordered = sorted(values)
    return {
        "min": float(ordered[0]),
        "max": float(ordered[-1]),
        "mean": float(statistics.fmean(ordered)),
        "median": float(statistics.median(ordered)),
        "std": float(statistics.pstdev(ordered)) if len(ordered) > 1 else 0.0,
        "p25": float(ordered[max(0, int(0.25 * (len(ordered) - 1)))]),
        "p75": float(ordered[max(0, int(0.75 * (len(ordered) - 1)))]),
    }


def _profile_with_pandas(
    dataset_path: Path,
    sheet: str | None,
    max_rows: int,
) -> dict[str, Any]:
    ext = dataset_path.suffix.lower()
    if ext == ".csv":
        frame = pd.read_csv(dataset_path, nrows=max_rows)
    elif ext in {".xlsx", ".xls"}:
        frame = pd.read_excel(dataset_path, sheet_name=sheet or 0, nrows=max_rows)
    elif ext == ".parquet":
        frame = pd.read_parquet(dataset_path).head(max_rows)
    elif ext == ".json":
        frame = pd.read_json(dataset_path).head(max_rows)
    else:
        raise ValueError(f"Unsupported extension: {ext}")

    columns: list[dict[str, Any]] = []
    for column in frame.columns:
        series = frame[column]
        non_null = series.dropna()
        profile: dict[str, Any] = {
            "name": str(column),
            "dtype": str(series.dtype),
            "missing_count": int(series.isna().sum()),
            "missing_pct": round(float(series.isna().mean() * 100), 4),
            "unique_count": int(series.nunique(dropna=True)),
        }

        if pd.api.types.is_numeric_dtype(series):
            numeric_values = [float(v) for v in non_null.tolist()]
            profile["stats"] = _numeric_stats(numeric_values)
        else:
            top_values = (
                non_null.astype(str)
                .value_counts(dropna=True)
                .head(5)
                .to_dict()
            )
            profile["top_values"] = {str(k): int(v) for k, v in top_values.items()}

        columns.append(profile)

    return {
        "tool": "data_profile",
        "engine": "pandas",
        "dataset": str(dataset_path),
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "rows": int(len(frame)),
        "columns": int(len(frame.columns)),
        "duplicate_rows": int(frame.duplicated().sum()),
        "column_profiles": columns,
    }


def _profile_csv_stdlib(dataset_path: Path, max_rows: int) -> dict[str, Any]:
    with dataset_path.open("r", encoding="utf-8", errors="replace", newline="") as file_obj:
        reader = csv.DictReader(file_obj)
        if not reader.fieldnames:
            raise ValueError("CSV has no header row.")

        raw_fieldnames = list(reader.fieldnames)
        fieldnames = [name.lstrip("\ufeff") if name else name for name in raw_fieldnames]
        field_pairs = list(zip(raw_fieldnames, fieldnames))
        column_values: dict[str, list[str]] = {name: [] for name in fieldnames}
        rows_seen = 0
        duplicate_count = 0
        seen_rows: set[tuple[str, ...]] = set()

        for row in reader:
            rows_seen += 1
            if rows_seen > max_rows:
                break

            row_signature = tuple((row.get(raw_name) or "").strip() for raw_name, _ in field_pairs)
            if row_signature in seen_rows:
                duplicate_count += 1
            else:
                seen_rows.add(row_signature)

            for raw_name, clean_name in field_pairs:
                column_values[clean_name].append((row.get(raw_name) or "").strip())

    columns: list[dict[str, Any]] = []
    for name in fieldnames:
        values = column_values[name]
        missing_count = sum(1 for item in values if item == "")
        non_null_values = [item for item in values if item != ""]
        numeric_values = [_safe_float(item) for item in non_null_values]
        numeric_clean = [item for item in numeric_values if item is not None]

        profile: dict[str, Any] = {
            "name": name,
            "dtype": "numeric" if len(non_null_values) > 0 and len(numeric_clean) == len(non_null_values) else "string",
            "missing_count": int(missing_count),
            "missing_pct": round((missing_count / len(values) * 100), 4) if values else 0.0,
            "unique_count": int(len(set(non_null_values))),
        }

        if profile["dtype"] == "numeric":
            profile["stats"] = _numeric_stats([float(v) for v in numeric_clean])
        else:
            top_values = Counter(non_null_values).most_common(5)
            profile["top_values"] = {key: int(count) for key, count in top_values}

        columns.append(profile)

    return {
        "tool": "data_profile",
        "engine": "stdlib-csv",
        "dataset": str(dataset_path),
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "rows": int(rows_seen if rows_seen <= max_rows else max_rows),
        "columns": int(len(fieldnames)),
        "duplicate_rows": int(duplicate_count),
        "column_profiles": columns,
        "note": "Install pandas for richer profiling and non-CSV formats.",
    }


def build_profile(
    dataset_path: Path,
    sheet: str | None,
    max_rows: int,
) -> dict[str, Any]:
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    extension = dataset_path.suffix.lower()
    if pd is not None:
        return _profile_with_pandas(dataset_path, sheet=sheet, max_rows=max_rows)

    if extension == ".csv":
        return _profile_csv_stdlib(dataset_path, max_rows=max_rows)

    raise RuntimeError(
        "pandas is required for this file format. "
        "Install with: pip install pandas openpyxl pyarrow"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate profile summary for a tabular dataset.")
    parser.add_argument("dataset", help="Path to dataset file (csv/xlsx/parquet/json).")
    parser.add_argument("--sheet", default=None, help="Sheet name or index for XLSX files.")
    parser.add_argument("--max-rows", type=int, default=200000, help="Maximum rows to profile.")
    parser.add_argument("--output", default=None, help="Optional output path for JSON profile.")
    args = parser.parse_args()

    dataset_path = Path(args.dataset).resolve()
    output_path = Path(args.output).resolve() if args.output else None

    try:
        profile = build_profile(dataset_path, sheet=args.sheet, max_rows=max(1, args.max_rows))
    except Exception as exc:
        error_payload = {
            "tool": "data_profile",
            "passed": False,
            "error": str(exc),
        }
        print(json.dumps(error_payload, indent=2))
        sys.exit(1)

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(profile, indent=2), encoding="utf-8")

    print(json.dumps(profile, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
