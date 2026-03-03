---
description: Run exploratory data analysis workflow on tabular files and produce a structured analysis report.
---

# /analyze-data - Exploratory Data Analysis

$ARGUMENTS

---

## Purpose

Use this workflow to profile a dataset, identify quality issues, and produce actionable insights tied to business objectives.

## Inputs

- Dataset path from `$ARGUMENTS`
- If path is missing, default to `data/raw/raw-dataset.xlsx`

## Execution Steps

1. Load `data-analyst` agent and `data-analysis-eda` skill.
2. Run:

```bash
python .agent/skills/data-analysis-eda/scripts/data_profile.py <dataset-path> --output data/profile-summary.json
```

3. Review the checklist in:
   - `.agent/skills/data-analysis-eda/references/eda-checklist.md`
4. Generate report using:
   - `.agent/skills/data-analysis-eda/references/analysis-report-template.md`
5. Present:
   - Top quality risks
   - Top insights
   - Recommended next step

## Output Contract

- Profile artifact: `data/profile-summary.json`
- Written report in chat using template structure

## Examples

```text
/analyze-data
/analyze-data data/raw/raw-dataset.xlsx
/analyze-data data/interim/sales.csv
```
