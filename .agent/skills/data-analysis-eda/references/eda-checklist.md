# EDA Checklist

## 1. Context

- Define the business question in one sentence.
- Confirm the meaning of each row.
- Confirm the primary KPI and decision deadline.

## 2. Data Inventory

- Identify dataset path and file type.
- Record number of rows and columns.
- Map columns to types: numeric, categorical, datetime, text.

## 3. Data Quality

- Missing values by column (count and percent).
- Duplicate rows and duplicate keys.
- Invalid ranges (negative age, impossible dates).
- Inconsistent categories (case variants, typos).

## 4. Statistical Summary

- Numeric: min, max, mean, median, std, quartiles.
- Categorical: cardinality and top values.
- Target variable distribution (if applicable).

## 5. Bias and Leakage Risk

- Check class imbalance.
- Check time leakage (future information in features).
- Check target leakage (derived columns).
- Check sampling bias by segment or period.

## 6. Insight Extraction

- List top anomalies and possible causes.
- Define 3-5 hypotheses to test.
- Tie each hypothesis to a business action.

## 7. Report Output

- Include assumptions and limits.
- Include what is ready for modeling.
- Include what must be fixed first.
