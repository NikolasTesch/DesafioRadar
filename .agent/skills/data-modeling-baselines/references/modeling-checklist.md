# Modeling Checklist

## 1. Problem Framing

- Confirm target column.
- Confirm task type (classification or regression).
- Confirm business objective and deployment use case.

## 2. Data Preconditions

- Ensure target has enough valid rows.
- Remove or flag leakage columns.
- Handle missing values explicitly.
- Check for class imbalance or skewed target.

## 3. Baseline Setup

- Set fixed random state.
- Define train/test strategy.
- Include dummy model as floor.
- Include one linear and one tree baseline.

## 4. Metrics

- Classification: accuracy, f1_weighted, precision, recall.
- Regression: rmse, mae, r2.
- Highlight metric that matters most for business.

## 5. Robustness

- Validate if split is representative.
- Check extreme segments separately.
- Note overfitting risk if train/test gap is large.

## 6. Reporting

- Record model settings and preprocessing.
- Provide ranked leaderboard.
- Recommend next action (feature engineering, data collection, threshold tuning).
