---
name: data-analysis-eda
description: Exploratory data analysis workflow for tabular datasets. Use when the user asks to inspect CSV/XLSX/Parquet files, check data quality, profile columns, detect missing values/outliers, and produce an analysis report with hypotheses and next actions.
---

# Data Analysis EDA

## Overview

Use this skill to run EDA in a consistent order: scope the business question, profile the dataset, evaluate quality, extract insights, and deliver a report.

## Workflow

1. Define analysis scope before touching data.
2. Load dataset and inspect schema shape.
3. Measure data quality (missing, duplicates, inconsistent types).
4. Segment columns into numeric, categorical, datetime.
5. Produce quick descriptive statistics and top categories.
6. Write hypotheses, risks, and recommended next actions.

## Scope Checklist

Always ask or infer these points:

- Business objective and decision to support
- Unit of analysis (row meaning)
- Time window and refresh cadence
- Success metric and acceptable error margin
- Constraints (latency, explainability, tooling)

If any item is unclear, state assumptions explicitly.

## Quick Commands

### 1) Profile data file

```bash
python .agent/skills/data-analysis-eda/scripts/data_profile.py data/raw/raw-dataset.xlsx --output data/profile-summary.json
```

### 2) Use references while writing the report

- Read `references/eda-checklist.md` during analysis.
- Use `references/analysis-report-template.md` for final output.

## Decision Rules

- If dataset has fewer than 100 rows, focus on data integrity and manual validation.
- If dataset has many missing values in target columns, prioritize data collection or imputation strategy before modeling.
- If strong class imbalance exists, mark baseline metrics that hide failure (for example, accuracy).
- If leakage risk appears (future data, IDs, target-derived fields), stop and isolate suspect columns.

## Deliverable Standard

Final output must include:

- Dataset path and timestamp
- Data quality summary
- Key distributions and anomalies
- 3 to 5 actionable insights
- Open questions and recommended next step
