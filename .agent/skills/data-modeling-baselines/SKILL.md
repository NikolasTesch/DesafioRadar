---
name: data-modeling-baselines
description: Baseline machine learning workflow for tabular data. Use when the user asks to build first-pass classification or regression models, compare simple algorithms, evaluate metrics, and produce an experiment summary before advanced tuning.
---

# Data Modeling Baselines

## Overview

Use this skill to move from cleaned tabular data to a defensible baseline result with clear metrics and reproducible assumptions.

## Workflow

1. Define target variable and task type (classification or regression).
2. Validate leakage risk and remove forbidden columns.
3. Split train/test with fixed random seed.
4. Train baseline models (dummy, linear, tree-based).
5. Compare metrics and record the winner.
6. Write experiment summary and next steps.

## Mandatory Inputs

Before training, confirm:

- Target column name
- Business metric (for example, recall vs precision tradeoff)
- Unit cost of false positives and false negatives (classification)
- Unit cost of prediction error (regression)
- Any fairness or explainability requirement

If unknown, proceed with explicit assumptions.

## Quick Command

```bash
python .agent/skills/data-modeling-baselines/scripts/train_baseline.py data/raw/raw-dataset.xlsx --target target_column --output data/baseline-result.json
```

## Evaluation Rules

- Classification default metric: `f1_weighted`.
- Regression default metric: `rmse` (lower is better).
- Always compare against dummy baseline.
- Report both business-facing and technical interpretation.

## References

- Use `references/modeling-checklist.md` before training.
- Use `references/experiment-report-template.md` to structure output.
