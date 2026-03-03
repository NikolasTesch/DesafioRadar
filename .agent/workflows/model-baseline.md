---
description: Train and compare baseline models for tabular datasets using a reproducible pipeline.
---

# /model-baseline - Baseline Modeling

$ARGUMENTS

---

## Purpose

Use this workflow to run baseline ML models (classification or regression), compare metrics, and decide the next modeling iteration.

## Inputs

- Dataset path from `$ARGUMENTS`
- Required target column (ask if missing)
- Optional task type: `classification`, `regression`, or `auto`

## Execution Steps

1. Load `ml-engineer` agent and `data-modeling-baselines` skill.
2. Confirm target and metric priority.
3. Run:

```bash
python .agent/skills/data-modeling-baselines/scripts/train_baseline.py <dataset-path> --target <target-column> --output data/baseline-result.json
```

4. Review:
   - `.agent/skills/data-modeling-baselines/references/modeling-checklist.md`
5. Report with:
   - `.agent/skills/data-modeling-baselines/references/experiment-report-template.md`

## Output Contract

- Result artifact: `data/baseline-result.json`
- Leaderboard + recommendation in chat

## Examples

```text
/model-baseline data/raw/raw-dataset.xlsx
/model-baseline data/interim/churn.csv
```
