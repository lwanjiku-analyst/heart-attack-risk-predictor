with st.sidebar:
    st.header("Model Snapshot")
    st.write(
        "**Purpose:** Explore survey characteristics associated with "
        "previously reported heart attack status."
    )
    st.write("**Data:** CDC BRFSS 2022 · 444,975 adults")
    st.write("**Model:** Theory-guided Logistic Regression")

    st.divider()
    st.subheader("Why This Matters")
    st.write(
        "Helps researchers explore population patterns and compare "
        "groups within the study data."
    )

    st.divider()
    st.subheader("Behavioral Frameworks")
    st.write("🔴 **SEM** — Social and health context")
    st.write("🔵 **TPB** — Health behaviors")
    st.write("🟢 **HBM** — Health beliefs and engagement")
    st.write("🟣 **ALT** — Stress and health burden")

    st.caption(
        "Research and education only. This model does not predict "
        "future heart attacks or provide medical advice."
    )
