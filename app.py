"""Streamlit app for Heart Attack Risk Predictor."""

from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st

from src.model import THRESHOLD, train_and_evaluate

st.set_page_config(page_title="Heart Attack Risk Predictor", page_icon="❤️", layout="wide")

st.markdown(
    """
    <style>
    .risk-high {background-color:#ffe5e5;border-left:8px solid #d62828;padding:0.8rem 1rem;border-radius:0.4rem;color:#6a040f;font-weight:700;}
    .risk-moderate {background-color:#fff8e1;border-left:8px solid #ffb703;padding:0.8rem 1rem;border-radius:0.4rem;color:#7f5539;font-weight:700;}
    .risk-low {background-color:#e6f4ea;border-left:8px solid #2a9d8f;padding:0.8rem 1rem;border-radius:0.4rem;color:#1b4332;font-weight:700;}
    .small-note {font-size:0.9rem;color:#555;}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def load_artifacts():
    return train_and_evaluate()


artifacts = load_artifacts()
model = artifacts.pipeline

st.title("❤️ Heart Attack Risk Predictor")
st.caption("Built on CDC BRFSS 2022 data (444,975 observations). Champion logistic regression model validation AUC: 0.8381.")
st.write("Estimate heart attack risk from key self-reported health and behavior factors.")

age_categories = [
    "Age 18 to 24",
    "Age 25 to 29",
    "Age 30 to 34",
    "Age 35 to 39",
    "Age 40 to 44",
    "Age 45 to 49",
    "Age 50 to 54",
    "Age 55 to 59",
    "Age 60 to 64",
    "Age 65 to 69",
    "Age 70 to 74",
    "Age 75 to 79",
    "Age 80 or older",
]

with st.sidebar:
    st.header("Patient Inputs")
    age_category = st.selectbox("AgeCategory", age_categories, index=6)
    sex = st.selectbox("Sex", ["Male", "Female"])
    general_health = st.selectbox("GeneralHealth (1=Excellent, 5=Poor)", [1, 2, 3, 4, 5], index=2)
    had_stroke = st.selectbox("HadStroke", ["No", "Yes"])
    had_diabetes = st.selectbox("HadDiabetes", ["No", "Yes"])
    had_kidney_disease = st.selectbox("HadKidneyDisease", ["No", "Yes"])
    physical_health_days = st.slider("PhysicalHealthDays", min_value=0, max_value=30, value=2)
    bmi = st.slider("BMI", min_value=10.0, max_value=60.0, value=27.0, step=0.1)
    smoker_status = st.selectbox(
        "SmokerStatus",
        ["Never smoked", "Former smoker", "Current smoker - some days", "Current smoker - every day"],
    )
    sleep_hours = st.slider("SleepHours", min_value=4, max_value=12, value=7)

if st.button("Predict Risk", type="primary"):
    general_health_map = {
        1: "Excellent",
        2: "Very good",
        3: "Good",
        4: "Fair",
        5: "Poor",
    }

    input_df = pd.DataFrame(
        [
            {
                "AgeCategory": age_category,
                "Sex": sex,
                "GeneralHealth": general_health_map[general_health],
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

    probability = float(model.predict_proba(input_df)[:, 1][0])
    percent = probability * 100

    if probability >= 0.20:
        tier, style_class = "HIGH", "risk-high"
    elif probability >= THRESHOLD:
        tier, style_class = "MODERATE", "risk-moderate"
    else:
        tier, style_class = "LOW", "risk-low"

    st.subheader("Predicted Risk")
    st.progress(min(max(percent / 100, 0.0), 1.0), text=f"{percent:.1f}% estimated probability")
    st.metric("Risk Probability", f"{percent:.1f}%")
    st.markdown(f"<div class='{style_class}'>Risk Tier: {tier}</div>", unsafe_allow_html=True)

    transformed = model.named_steps["preprocessor"].transform(input_df)
    feature_names = model.named_steps["preprocessor"].get_feature_names_out()
    coefs = model.named_steps["model"].coef_[0]
    contributions = transformed[0] * coefs

    top_idx = np.argsort(np.abs(contributions))[-3:][::-1]
    top_factors = [(feature_names[i], contributions[i]) for i in top_idx]

    st.subheader("Top 3 Risk Factors Driving Prediction")
    for idx, (feat, score) in enumerate(top_factors, start=1):
        direction = "increases" if score >= 0 else "decreases"
        clean_feat = feat.replace("num__", "").replace("cat__", "")
        st.write(f"{idx}. **{clean_feat}** ({direction} risk)")

st.markdown("---")
st.markdown(
    "<p class='small-note'><strong>Disclaimer:</strong> This tool is for educational screening support only and does not diagnose medical conditions. Always consult a licensed clinician for medical advice.</p>",
    unsafe_allow_html=True,
)
