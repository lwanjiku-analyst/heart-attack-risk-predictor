"""Model training/evaluation for heart attack risk predictor."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.preprocess import load_and_prepare_data

THRESHOLD = 0.05


@dataclass
class ModelArtifacts:
    pipeline: Pipeline
    metrics: Dict[str, float]


def ks_statistic(y_true: pd.Series, y_proba: np.ndarray) -> float:
    fpr, tpr, _ = roc_curve(y_true, y_proba)
    return float(np.max(tpr - fpr))


def lift_at_decile_1(y_true: pd.Series, y_proba: np.ndarray) -> float:
    frame = pd.DataFrame({"y": y_true.values, "p": y_proba})
    frame = frame.sort_values("p", ascending=False).reset_index(drop=True)
    top_n = max(int(np.ceil(0.10 * len(frame))), 1)
    top_rate = frame.iloc[:top_n]["y"].mean()
    base_rate = frame["y"].mean()
    return float(top_rate / base_rate) if base_rate > 0 else 0.0


def build_pipeline(X: pd.DataFrame) -> Pipeline:
    numeric_features = X.select_dtypes(include=[np.number]).columns.tolist()
    categorical_features = [c for c in X.columns if c not in numeric_features]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                numeric_features,
            ),
            (
                "cat",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        (
                            "encoder",
                            OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                        ),
                    ]
                ),
                categorical_features,
            ),
        ]
    )

    model = LogisticRegression(
        class_weight="balanced",
        penalty="l1",
        solver="liblinear",
        max_iter=2000,
        random_state=42,
    )

    return Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])


def train_and_evaluate(csv_path: str = "data/heart_2022_with_nans.csv") -> ModelArtifacts:
    X_train, X_val, y_train, y_val = load_and_prepare_data(csv_path)

    pipeline = build_pipeline(X_train)
    pipeline.fit(X_train, y_train)

    y_proba = pipeline.predict_proba(X_val)[:, 1]
    y_pred = (y_proba >= THRESHOLD).astype(int)

    metrics = {
        "AUC": float(roc_auc_score(y_val, y_proba)),
        "KS": ks_statistic(y_val, y_proba),
        "Recall": float(recall_score(y_val, y_pred, zero_division=0)),
        "Precision": float(precision_score(y_val, y_pred, zero_division=0)),
        "F1": float(f1_score(y_val, y_pred, zero_division=0)),
        "Lift@Decile1": lift_at_decile_1(y_val, y_proba),
    }

    return ModelArtifacts(pipeline=pipeline, metrics=metrics)


if __name__ == "__main__":
    artifacts = train_and_evaluate()
    for k, v in artifacts.metrics.items():
        print(f"{k}: {v:.4f}")
