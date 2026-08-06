from __future__ import annotations

from pathlib import Path

import streamlit as st

from src.draven_engine import build_report, calculate_metrics, load_json, milestone_per_share, validate_case


ROOT = Path(__file__).resolve().parent
CASE_DIR = ROOT / "cases"
SCHEMA_PATH = ROOT / "schemas" / "case.schema.json"

st.set_page_config(page_title="Draven Biotech Event Engine", page_icon="◈", layout="wide")
st.title("Draven Biotech Event Engine")
st.caption("Evidence-first underwriting for binary and path-dependent biotechnology equity events")

case_files = sorted(CASE_DIR.glob("*.json"))
if not case_files:
    st.error("No case dossiers found in cases/.")
    st.stop()

selected = st.sidebar.selectbox("Case dossier", case_files, format_func=lambda path: path.stem)
case = load_json(selected)
schema = load_json(SCHEMA_PATH)
errors = validate_case(case, schema)

if errors:
    st.error("Case failed publication gates")
    for error in errors:
        st.write(f"- {error}")
    st.stop()

metrics = calculate_metrics(case)
report, _ = build_report(selected, SCHEMA_PATH)
security = case["security"]

st.sidebar.success("Publication gates passed")
st.sidebar.code(f"version: {metrics.version_hash}")
st.sidebar.write(f"Evidence cutoff: {case['cutoff']}")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Reference price", f"${security['price']:.2f}")
col2.metric("Event fair value", f"${metrics.probability_weighted_value:.2f}")
col3.metric("Expected return", f"{metrics.expected_return:.1%}")
col4.metric("Probability above spot", f"{metrics.upside_probability:.1%}")
per_share = milestone_per_share(case)
col5.metric("Milestone per share", f"${per_share:.2f}" if per_share is not None else "N/A")

st.subheader("Investment conclusion")
st.write(case["investment_conclusion"])

st.subheader("Scenario distribution")
scenario_rows = [
    {
        "Scenario": item["name"],
        "Probability": item["probability"],
        "Terminal price": item["terminal_price"],
        "Return vs. spot": item["terminal_price"] / security["price"] - 1,
        "Drivers": "; ".join(item["drivers"]),
    }
    for item in case["scenarios"]
]
st.dataframe(
    scenario_rows,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Probability": st.column_config.NumberColumn(format="%.1f%%"),
        "Terminal price": st.column_config.NumberColumn(format="$%.2f"),
        "Return vs. spot": st.column_config.NumberColumn(format="%.1f%%"),
    },
)

left, right = st.columns(2)
with left:
    st.subheader("Catalysts")
    for catalyst in case["catalysts"]:
        st.markdown(f"**{catalyst['timing']} — {catalyst['name']}**")
        st.caption(f"Status: {catalyst['status']} | Evidence: {', '.join(catalyst['source_ids'])}")
with right:
    st.subheader("Instrument gate")
    st.success(case["instrument_gate"]["preferred"])
    for rejected in case["instrument_gate"].get("rejected", []):
        st.write(f"- {rejected}")

st.subheader("Evidence ledger")
st.dataframe(case["evidence"], use_container_width=True, hide_index=True)

st.subheader("Falsifiers and kill criteria")
for falsifier in case["falsifiers"]:
    st.write(f"- {falsifier}")

st.subheader("Publication output")
st.download_button(
    "Download versioned Markdown report",
    report,
    file_name=f"{case['case_id']}-{metrics.version_hash}.md",
    mime="text/markdown",
)
with st.expander("Preview generated report"):
    st.markdown(report)

st.warning("Independent research generated from a versioned public-information dossier. Not investment advice.")
