"""Preprocessing pipeline for CDC BRFSS 2022 heart attack risk modeling."""

from __future__ import annotations

from typing import Dict, Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

TARGET = "HadHeartAttack"
DROP_COLUMNS = ["HadAngina", "WeightInKilograms"]
LOG_COLUMNS = ["MentalHealthDays", "PhysicalHealthDays"]
BMI_COLUMN = "BMI"
SLEEP_COLUMN = "SleepHours"


def _bmi_to_who_group(value: float) -> str:
    if pd.isna(value):
        return np.nan
    if value < 18.5:
        return "Underweight"
    if value < 25:
        return "Normal"
    if value < 30:
        return "Overweight"
    return "Obese"


def _impute_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in out.columns:
        if pd.api.types.is_numeric_dtype(out[col]):
            out[col] = out[col].fillna(out[col].median())
        else:
            mode = out[col].mode(dropna=True)
            fill_value = mode.iloc[0] if not mode.empty else "Unknown"
            out[col] = out[col].fillna(fill_value)
    return out


def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Apply feature preprocessing rules to raw BRFSS dataframe."""
    work = df.copy()

    # Remove leakage/unused fields.
    cols_to_drop = [c for c in DROP_COLUMNS if c in work.columns]
    if cols_to_drop:
        work = work.drop(columns=cols_to_drop)

    # Log transform selected day-count columns.
    for col in LOG_COLUMNS:
        if col in work.columns:
            work[col] = np.log1p(work[col].clip(lower=0))

    # Convert BMI to WHO groups.
    if BMI_COLUMN in work.columns:
        work["BMIGroup"] = work[BMI_COLUMN].apply(_bmi_to_who_group)

    # Clip sleep to plausible range.
    if SLEEP_COLUMN in work.columns:
        work[SLEEP_COLUMN] = work[SLEEP_COLUMN].clip(lower=3, upper=12)

    # Impute missing values after transforms.
    work = _impute_dataframe(work)

    return work


def split_train_validation(
    df: pd.DataFrame,
    test_size: float = 0.30,
    random_state: int = 42,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Preprocess and split data with stratification on HadHeartAttack."""
    if TARGET not in df.columns:
        raise ValueError(f"Expected target column '{TARGET}' in dataframe.")

    processed = preprocess_dataframe(df)

    y = processed[TARGET].astype(int)
    X = processed.drop(columns=[TARGET])

    X_train, X_val, y_train, y_val = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )
    return X_train, X_val, y_train, y_val


def load_and_prepare_data(
    csv_path: str = "data/heart_2022_with_nans.csv",
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Convenience loader from local CSV path into train/validation split."""
    df = pd.read_csv(csv_path)
    return split_train_validation(df)


__all__ = [
    "TARGET",
    "preprocess_dataframe",
    "split_train_validation",
    "load_and_prepare_data",
]
