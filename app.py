import math
from dataclasses import dataclass

import streamlit as st


# ------------------------------
# Page config + styling
# ------------------------------
st.set_page_config(
    page_title="Heart Attack Risk Predictor",
    page_icon="❤️",
    layout="wide",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=DM+Serif+Display:ital@0;1&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'DM Serif Display', serif !important;
        letter-spacing: 0.2px;
    }

    .metric-card {
        border: 1px solid #e6e8ec;
        border-radius: 14px;
        padding: 1rem 1.1rem;
        background: linear-gradient(180deg, #ffffff 0%, #fbfcff 100%);
        box-shadow: 0 2px 8px rgba(18, 38, 63, 0.04);
    }

    .risk-pill {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.9rem;
    }

    .small-note {
        color: #5f6b7a;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------------------
# Model definition
# ------------------------------
@dataclass
class Feature:
    label: str
    coef: float
    protective_when_true: bool = False


INTERCEPT = -4.10

FEATURES = {
    "age": Feature("Age (per year)", 0.041),
    "male": Feature("Male sex", 0.34),
    "bmi": Feature("BMI (per unit)", 0.017),
    "high_bp": Feature("High blood pressure", 0.64),
    "high_chol": Feature("High cholesterol", 0.46),
    "diabetes": Feature("Diabetes", 0.76),
    "stroke": Feature("Prior stroke", 0.93),
    "chd": Feature("Angina / Coronary heart disease", 1.08),
    "smoker": Feature("Current smoker", 0.41),
    "heavy_drinker": Feature("Heavy alcohol use", 0.24),
    "no_exercise": Feature("No exercise", 0.35),
    "fruit_veg_daily": Feature("Daily fruit & vegetables", -0.21, protective_when_true=True),
    "good_health": Feature("Self-rated good/very good health", -0.49, protective_when_true=True),
    "difficulty_walking": Feature("Difficulty walking", 0.57),
    "low_income": Feature("Low income", 0.32),
}

DECILE_EVENT_RATES = {
    1: 24.99,
    2: 16.40,
    3: 10.60,
    4: 7.20,
    5: 4.90,
    6: 3.40,
    7: 2.30,
    8: 1.40,
    9: 0.70,
    10: 0.20,
}


def sigmoid(z: float) -> float:
    return 1.0 / (1.0 + math.exp(-z))


def calculate_bmi(height_cm: float, weight_kg: float) -> float:
    height_m = height_cm / 100
    return weight_kg / (height_m**2)


def risk_tier(prob_pct: float) -> tuple[str, str, str]:
    if prob_pct < 3:
        return "Low", "#e8f6ee", "#1f7a45"
    if prob_pct < 8:
        return "Moderate", "#fff6df", "#8a6300"
    if prob_pct < 16:
        return "High", "#ffe8e0", "#9b3a20"
    return "Very High", "#fde2e8", "#8b1e3f"


def to_decile(prob_pct: float) -> int:
    # Higher risk => lower decile number (D1 highest risk)
    bins = [20, 14, 9, 6, 4, 2.8, 1.8, 1.0, 0.45]
    for i, cut in enumerate(bins, start=1):
        if prob_pct >= cut:
            return i
    return 10


def contribution_list(values: dict) -> tuple[list[tuple[str, float]], list[tuple[str, float]]]:
    risk_contrib = []
    protect_contrib = []

    for key, val in values.items():
        if key not in FEATURES:
            continue
        coef = FEATURES[key].coef
        contrib = coef * val

        if contrib > 0:
            risk_contrib.append((FEATURES[key].label, contrib))
        elif contrib < 0:
            protect_contrib.append((FEATURES[key].label, abs(contrib)))

    risk_contrib.sort(key=lambda x: x[1], reverse=True)
    protect_contrib.sort(key=lambda x: x[1], reverse=True)
    return risk_contrib, protect_contrib


# ------------------------------
# Sidebar
# ------------------------------
with st.sidebar:
    st.header("Model Snapshot")
    st.markdown("**Algorithm:** Logistic Regression")
    st.markdown("**Data Source:** CDC BRFSS 2022")
    st.markdown("**Validation AUC:** 0.84")
    st.markdown("**Validation Recall:** 0.82")
    st.markdown("**Lift @ D1:** 4.43×")
    st.markdown("---")
    st.markdown("### Estimated Business Impact")
    st.markdown(
        "**$56M annual impact** from improved prevention targeting, early intervention, and high-risk outreach prioritization."
    )


st.title("Heart Attack Risk Predictor")
st.caption("BRFSS-derived logistic model with embedded coefficients (no external model file required).")

col1, col2 = st.columns([1.05, 1], gap="large")

with col1:
    st.subheader("Patient Inputs")

    age = st.slider("Age", min_value=18, max_value=95, value=52)
    sex = st.selectbox("Sex", ["Female", "Male"])

    c1, c2 = st.columns(2)
    with c1:
        height_cm = st.number_input("Height (cm)", min_value=120.0, max_value=230.0, value=170.0, step=0.5)
    with c2:
        weight_kg = st.number_input("Weight (kg)", min_value=35.0, max_value=250.0, value=78.0, step=0.5)

    bmi = calculate_bmi(height_cm, weight_kg)
    st.markdown(f"**Auto-calculated BMI:** `{bmi:.1f}`")

    st.markdown("### Clinical & Behavioral Factors")
    high_bp = st.checkbox("High blood pressure")
    high_chol = st.checkbox("High cholesterol")
    diabetes = st.checkbox("Diabetes")
    stroke = st.checkbox("Prior stroke")
    chd = st.checkbox("Angina / Coronary heart disease")
    smoker = st.checkbox("Current smoker")
    heavy_drinker = st.checkbox("Heavy drinker")
    no_exercise = st.checkbox("No exercise")
    fruit_veg_daily = st.checkbox("Fruit & vegetables daily")
    good_health = st.checkbox("Self-rated good/very good health")
    difficulty_walking = st.checkbox("Difficulty walking")
    low_income = st.checkbox("Low income")

with col2:
    st.subheader("Prediction Results")

    x = {
        "age": age,
        "male": 1 if sex == "Male" else 0,
        "bmi": bmi,
        "high_bp": int(high_bp),
        "high_chol": int(high_chol),
        "diabetes": int(diabetes),
        "stroke": int(stroke),
        "chd": int(chd),
        "smoker": int(smoker),
        "heavy_drinker": int(heavy_drinker),
        "no_exercise": int(no_exercise),
        "fruit_veg_daily": int(fruit_veg_daily),
        "good_health": int(good_health),
        "difficulty_walking": int(difficulty_walking),
        "low_income": int(low_income),
    }

    logit = INTERCEPT + sum(FEATURES[k].coef * v for k, v in x.items())
    risk = sigmoid(logit) * 100

    tier, bg, fg = risk_tier(risk)
    decile = to_decile(risk)
    event_rate = DECILE_EVENT_RATES[decile]

    st.markdown(
        f"""
        <div class="metric-card">
            <h3 style="margin:0;">Predicted Risk</h3>
            <p style="font-size:2rem; font-weight:700; margin:0.2rem 0 0.6rem 0; color:#1c2f52;">{risk:.2f}%</p>
            <span class="risk-pill" style="background:{bg}; color:{fg};">{tier} Risk</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("&nbsp;", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="metric-card">
            <h3 style="margin:0;">Risk Decile</h3>
            <p style="font-size:1.3rem; margin:0.4rem 0 0.3rem 0;"><b>D{decile}</b> (1 = highest risk, 10 = lowest risk)</p>
            <p style="margin:0;" class="small-note">Observed event rate in this decile: <b>{event_rate:.2f}%</b></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    risk_drivers, protective = contribution_list(x)

    st.markdown("### Top Risk Drivers")
    if risk_drivers:
        for name, score in risk_drivers[:5]:
            st.write(f"• **{name}** (+{score:.2f} log-odds)")
    else:
        st.write("• No major risk drivers identified from selected inputs.")

    st.markdown("### Protective Factors")
    if protective:
        for name, score in protective[:5]:
            st.write(f"• **{name}** (-{score:.2f} log-odds)")
    else:
        st.write("• No strong protective factors selected.")

st.markdown("---")
st.info(
    "**Medical Disclaimer:** This tool is for educational and risk-stratification support only, "
    "not for diagnosis or treatment. Predictions are based on population-level associations from "
    "BRFSS-derived modeling and related graduate research findings. Always consult a licensed "
    "clinician for medical decisions."
)
