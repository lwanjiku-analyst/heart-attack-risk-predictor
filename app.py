"""Streamlit app for Heart Attack Risk Predictor."""

from __future__ import annotations

import numpy as np
import pandas as pd
import shap
import streamlit as st

from src.model import THRESHOLD, train_and_evaluate

st.set_page_config(page_title="Heart Attack Risk Predictor", layout="centered")
st.title("Heart Attack Risk Predictor")


@st.cache_resource
def load_artifacts():
    return train_and_evaluate()


artifacts = load_artifacts()
model = artifacts.pipeline

st.subheader("Patient Inputs")
age = st.slider("Age", min_value=18, max_value=100, value=50)
sex = st.selectbox("Sex", ["Male", "Female"])
general_health = st.selectbox("GeneralHealth", ["Excellent", "Very good", "Good", "Fair", "Poor"])
had_stroke = st.selectbox("HadStroke", ["No", "Yes"])
had_diabetes = st.selectbox("HadDiabetes", ["No", "Yes", "No, pre-diabetes or borderline diabetes", "Yes, but female told only during pregnancy"])
had_kidney_disease = st.selectbox("HadKidneyDisease", ["No", "Yes"])
physical_health_days = st.slider("PhysicalHealthDays", min_value=0, max_value=30, value=2)
bmi = st.number_input("BMI", min_value=10.0, max_value=80.0, value=27.0, step=0.1)
smoker_status = st.selectbox("SmokerStatus", ["Never smoked", "Former smoker", "Current smoker - some days", "Current smoker - every day"])
sleep_hours = st.slider("SleepHours", min_value=0, max_value=24, value=7)

input_df = pd.DataFrame(
    [
        {
            "AgeCategory": f"{age}",
            "Sex": sex,
            "GeneralHealth": general_health,
            "HadStroke": had_stroke,
            "HadDiabetes": had_diabetes,
            "HadKidneyDisease": had_kidney_disease,
            "PhysicalHealthDays": physical_health_days,
            "BMI": bmi,
            "SmokerStatus": smoker_status,
            "SleepHours": sleep_hours,
            "MentalHealthDays": 0,
        }
    ]
)

if st.button("Predict Risk"):
    probability = float(model.predict_proba(input_df)[:, 1][0])
    predicted = int(probability >= THRESHOLD)

    decile = int(np.clip(np.ceil(probability * 10), 1, 10))

    st.metric("Risk Probability", f"{probability:.2%}")
    st.metric("Predicted Label (threshold=0.05)", "High Risk" if predicted else "Lower Risk")
    st.metric("Decile Tier", f"D{decile}")

    explainer = shap.Explainer(model.named_steps["model"])
    transformed = model.named_steps["preprocessor"].transform(input_df)
    shap_values = explainer(transformed)

    try:
        feature_names = model.named_steps["preprocessor"].get_feature_names_out()
    except Exception:
        feature_names = [f"feature_{i}" for i in range(transformed.shape[1])]

    contrib = np.abs(shap_values.values[0])
    top_idx = np.argsort(contrib)[-3:][::-1]
    top_features = [feature_names[i] for i in top_idx]

    st.subheader("Top 3 SHAP Risk Factors")
    for idx, feat in enumerate(top_features, start=1):
        st.write(f"{idx}. {feat}")
