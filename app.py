import streamlit as st

# ─────────────────────────────────────────────
# Page config + styling
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Theory-Driven Heart Attack Classification",
    page_icon="❤️",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,300;0,600;0,700;1,300&family=DM+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
h1, h2, h3 { font-family: 'Fraunces', serif !important; }

.metric-card {
    border: 1px solid #e0e6f0;
    border-radius: 16px;
    padding: 1.2rem 1.4rem;
    background: linear-gradient(160deg, #ffffff 0%, #f7f9ff 100%);
    box-shadow: 0 2px 12px rgba(18,38,63,0.06);
    margin-bottom: 0.8rem;
}

.risk-pill {
    display: inline-block;
    padding: 0.4rem 1rem;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.95rem;
    letter-spacing: 0.3px;
}

.equity-flag {
    border-left: 4px solid #E67E22;
    background: #FFF8F0;
    border-radius: 0 12px 12px 0;
    padding: 0.8rem 1rem;
    margin: 0.6rem 0;
    font-size: 0.92rem;
    color: #7D4000;
}

.framework-bar {
    height: 10px;
    border-radius: 999px;
    margin: 4px 0 8px 0;
}

.action-card {
    border-left: 4px solid #1B4F8C;
    background: #F2F6FB;
    border-radius: 0 12px 12px 0;
    padding: 0.7rem 1rem;
    margin: 0.4rem 0;
    font-size: 0.91rem;
}

.action-card-red {
    border-left: 4px solid #C0392B;
    background: #FEF0EE;
}

.action-card-yellow {
    border-left: 4px solid #E67E22;
    background: #FFF8F0;
}

.action-card-green {
    border-left: 4px solid #1A6B2A;
    background: #F0FAF2;
}

.small-note { color: #5f6b7a; font-size: 0.88rem; }

.decile-grid {
    display: flex;
    gap: 4px;
    margin: 8px 0;
}

.decile-cell {
    flex: 1;
    height: 28px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: 700;
}

.benchmark-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
    border-bottom: 1px solid #EEF2F8;
    font-size: 0.9rem;
}

.stCheckbox label { font-size: 0.95rem !important; }
</style>
""", unsafe_allow_html=True)


# Published retrospective study results. These are not computed from the selections.
DECILE_EVENT_RATES = {1: 24.99, 2: 12.49, 3: 7.63, 4: 4.71, 5: 2.80,
                      6: 1.69, 7: 1.00, 8: 0.57, 9: 0.35, 10: 0.20}
FRAMEWORK_COLORS = {"SEM": "#C0392B", "TPB": "#1B4F8C",
                    "HBM": "#1A6B2A", "ALT": "#7D3C98"}

# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Model Snapshot")

    st.markdown("**Purpose**")
    st.markdown("Explore survey characteristics associated with previously reported heart attack status.")

    st.markdown("**Data Source**")
    st.markdown("CDC BRFSS 2022 (444,975 U.S. adults)")

    st.markdown("**Model**")
    st.markdown("Theory-guided Logistic Regression")

    st.markdown("---")
    st.markdown("### 🌎 Why This Matters")
    st.markdown("Helps researchers explore population patterns and compare groups within the study data.")
    st.markdown("---")
    st.markdown("### Behavioral & Public Health Frameworks")
    framework_labels = {
        "SEM": "Chronic Conditions & Structural Factors",
        "TPB": "Health Behaviors & Lifestyle Choices",
        "HBM": "Preventive Care Engagement",
        "ALT": "Chronic Stress & Functional Burden",
    }
    for fw, color in FRAMEWORK_COLORS.items():
        st.markdown(f"<span style='color:{color};font-size:1.3rem;'>●</span> **{fw}** — {framework_labels[fw]}", unsafe_allow_html=True)
    st.markdown("---")
    st.caption("Research and education only. This model does not predict future heart attacks or provide medical advice.")


# ─────────────────────────────────────────────
# Title
# ─────────────────────────────────────────────
st.title("❤️ Theory-Driven Heart Attack Classification")
st.caption("CDC BRFSS 2022 · 444,975 U.S. adults · Exploring previously reported heart attack status")
st.markdown("---")

col1, col2 = st.columns([1.05, 1], gap="large")

# ─────────────────────────────────────────────
# LEFT COLUMN — INPUTS
# ─────────────────────────────────────────────
with col1:
    st.subheader("Explore Study Variables")
    st.write("Select characteristics to see how the study organizes them. This does not calculate a clinical risk score.")

    st.markdown("---")
    st.markdown("### 🔴 SEM — Chronic Conditions")
    high_bp     = st.checkbox("High blood pressure")
    high_chol   = st.checkbox("High cholesterol")
    diabetes    = st.checkbox("Diabetes")
    stroke      = st.checkbox("Prior stroke")
    low_income  = st.checkbox("Low income")

    st.markdown("### 🔵 TPB — Behavioral Lifestyle")
    smoker          = st.checkbox("Current smoker")
    no_exercise     = st.checkbox("No exercise")

    st.markdown("### 🟢 HBM — Preventive Care")
    fruit_veg_daily = st.checkbox("Fruit & vegetables daily")
    good_health     = st.checkbox("Self-rated good/very good health")

    st.markdown("### 🟣 ALT — Stress & Functional Burden")
    difficulty_walking = st.checkbox("Difficulty walking")


# ─────────────────────────────────────────────
# RIGHT COLUMN — STUDY EXPLORER
# ─────────────────────────────────────────────
with col2:
    st.subheader("Framework Explorer")
    selected = {
        "SEM": [name for name, checked in {
            "High blood pressure": high_bp, "High cholesterol": high_chol,
            "Diabetes": diabetes, "Prior stroke": stroke,
            "Lower income": low_income}.items() if checked],
        "TPB": [name for name, checked in {
            "Current smoking": smoker, "No exercise": no_exercise}.items() if checked],
        "HBM": [name for name, checked in {
            "Daily fruit and vegetables": fruit_veg_daily,
            "Good or very good self-rated health": good_health}.items() if checked],
        "ALT": ["Difficulty walking"] if difficulty_walking else [],
    }
    count = sum(len(names) for names in selected.values())
    st.markdown(
        f"<div class='metric-card'><b>{count} selected study "
        f"characteristic{'s' if count != 1 else ''}</b><br>"
        "Framework grouping only; this is not a model score or diagnosis.</div>",
        unsafe_allow_html=True,
    )
    if count:
        for framework, names in selected.items():
            if names:
                st.markdown(f"**{framework}:** {', '.join(names)}")
    else:
        st.info("Select a characteristic to see its study framework.")

    st.markdown("### Published Population Patterns")
    st.write("The highest-scoring 30% of respondents in the study included "
             "**79.95%** of those reporting a prior heart attack. "
             "These findings describe the study population.")
    decile = st.selectbox("Explore a published score decile", list(DECILE_EVENT_RATES),
                          format_func=lambda d: f"Decile {d}")
    st.metric("Observed prior-heart-attack rate in this decile",
              f"{DECILE_EVENT_RATES[decile]:.2f}%")
    st.caption("Checkbox selections do not assign a person to a decile. "
               "The fitted SAS Viya model is not run by this app.")

st.divider()
with st.expander("Study model performance"):
    st.write("The combined-framework Logistic Regression model reported "
             "validation AUC **0.8391** and recall **81.53%** on a "
             "stratified 70/30 split. These metrics describe the study model, "
             "not the checkbox explorer above.")
st.info("**Research and education only.** BRFSS records past, self-reported "
        "heart attack status. This app does not predict future heart attacks, "
        "establish causation, or replace professional medical evaluation.")
st.caption("Lilian Njeri Wanjiku · University of Central Oklahoma · 2026")
