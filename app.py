"""Sentinel — Streamlit UI. Uses the same pipeline as main.py."""
import json
import html
from pathlib import Path
import streamlit as st
from pipeline import run_pipeline

st.set_page_config(page_title="Sentinel | Cyber Investigation", page_icon="🛡️", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
:root { color-scheme: dark; }
.stApp { background: radial-gradient(ellipse at 8% 0%, #152c43 0%, #08111e 42%, #060b13 100%); color: #e7eef8; font-family: 'Manrope', sans-serif; }
.block-container { max-width: 1280px; padding-top: 2rem; padding-bottom: 3rem; }
header[data-testid="stHeader"] { background: transparent; }
div[data-testid="stMetric"] { background: rgba(17,31,48,.78); border: 1px solid #233b54; border-radius: 16px; padding: 18px 20px; }
div[data-testid="stMetricLabel"] { color: #8fa7bf; }
.hero { border:1px solid #25445e; background:linear-gradient(120deg,rgba(19,48,72,.9),rgba(12,22,36,.9)); border-radius:24px; padding:28px 32px; margin-bottom:22px; box-shadow:0 18px 55px rgba(0,0,0,.18); }
.eyebrow { color:#56e0c0; font:500 12px 'DM Mono',monospace; letter-spacing:2px; text-transform:uppercase; }
.hero h1 { color:#f0f7ff; font-size:38px; font-weight:800; letter-spacing:-1.4px; margin:9px 0 8px; }
.hero p { color:#a6bbd0; font-size:15px; margin:0; }
.section-title { color:#e8f3ff; font-size:20px; font-weight:800; margin:8px 0 12px; }
.q-card { border:1px solid #243e56; border-radius:17px; padding:20px 22px; margin:12px 0; background:linear-gradient(145deg,rgba(17,34,52,.95),rgba(10,20,32,.95)); }
.q-title { font-size:17px; color:#eff7ff; font-weight:800; margin-bottom:12px; }
.q-label { color:#6edbc5; font:500 11px 'DM Mono',monospace; letter-spacing:1.2px; text-transform:uppercase; margin-top:12px; }
.q-body { color:#bdcddd; font-size:14px; line-height:1.65; }
.small-note { color:#7892aa; font-size:12px; }
div.stButton > button[kind="primary"] { background:#57e0bf; color:#06131d; border:0; border-radius:11px; font-weight:800; min-height:44px; }
div.stButton > button[kind="primary"]:hover { background:#8af2d9; color:#06131d; }
[data-testid="stFileUploader"] { border:1px dashed #31516d; border-radius:14px; background:rgba(11,23,36,.65); padding:12px; }
hr { border-color:#20374c; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="eyebrow">◈ Evidence intelligence / SOC workflow</div>
  <h1>Sentinel <span style="color:#59dfc0">/</span> Cyber Investigation</h1>
  <p>Turn incident evidence gaps into focused, prioritized investigation questions.</p>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([1.1, 1], gap="large")
with left:
    st.markdown('<div class="section-title">01 / Incident source</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload an incident JSON file", type=["json"], help="Input is treated as untrusted evidence and validated before model use.")
    use_sample = st.toggle("Use built-in sample incident", value=uploaded is None)
    sample_path = Path("samples/inputs/sample_ok.json")
    if uploaded is not None and not use_sample:
        raw_bytes = uploaded.getvalue()
        temp_path = Path(".sentinel_uploaded_incident.json")
        temp_path.write_bytes(raw_bytes)
        selected_path = str(temp_path)
        st.caption(f"Loaded: {uploaded.name} · {len(raw_bytes):,} bytes")
    else:
        selected_path = str(sample_path)
        st.caption("Built-in sample: suspicious account activity with three related events.")
    with st.expander("Preview incident JSON", expanded=False):
        try:
            st.code(Path(selected_path).read_text(encoding="utf-8"), language="json")
        except Exception:
            st.info("Upload a valid JSON incident to preview it.")
    run_clicked = st.button("✦  Analyze incident", type="primary", use_container_width=True)
with right:
    st.markdown('<div class="section-title">02 / Analysis controls</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="q-card" style="margin-top:0">
      <div class="eyebrow">Processing pipeline</div>
      <div class="q-body" style="margin-top:14px">01&nbsp; Validate incident structure<br>
      02&nbsp; Detect and redact instruction-like evidence<br>
      03&nbsp; Generate evidence-gap questions<br>
      04&nbsp; Validate schema and fact grounding<br>
      05&nbsp; Record model and security events</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<p class="small-note">Safety note: results support an investigator; they do not establish guilt or replace forensic verification.</p>', unsafe_allow_html=True)

if run_clicked:
    result = run_pipeline(selected_path)
    st.divider()
    if result["status"] != "ok":
        if result["status"] == "error":
            st.error(result["error"] or "Input could not be processed.")
        elif result["status"] == "refused":
            st.warning("The model refused to generate investigation questions.")
        else:
            st.warning("The model response did not pass validation. No questions were displayed.")
        st.caption(f"Run status: {result['status']} · Run ID: {result['run_id']}")
    else:
        inc, facts, output = result["incident"], result["facts"], result["output"]
        st.markdown('<div class="section-title">03 / Incident overview</div>', unsafe_allow_html=True)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Incident ID", inc["incident_id"])
        m2.metric("Event count", len(inc["events"]))
        m3.metric("Account", inc["user_account"])
        m4.metric("Questions generated", len(output["questions"]))
        st.caption(f"{inc['incident_type']} · Run ID: {result['run_id']}")
        st.markdown('<div class="section-title">04 / Investigation questions</div>', unsafe_allow_html=True)
        for i, q in enumerate(output["questions"], 1):
            priority = q["priority"]
            label = {"High":"🔴 HIGH PRIORITY","Medium":"🟠 MEDIUM PRIORITY","Low":"🔵 LOW PRIORITY"}[priority]
            question_text = html.escape(q['question'])
            why_text = html.escape(q['why_it_matters'])
            evidence_text = html.escape(q['evidence_needed'])
            fact_text = html.escape(q['related_known_fact'])
            st.markdown(f"""
            <div class="q-card">
              <div class="eyebrow">Question {i} &nbsp; / &nbsp; {label}</div>
              <div class="q-title">{question_text}</div>
              <div class="q-label">Why it matters</div><div class="q-body">{why_text}</div>
              <div class="q-label">Evidence to collect</div><div class="q-body">{evidence_text}</div>
              <div class="q-label">Related known fact</div><div class="q-body">{fact_text}</div>
            </div>
            """, unsafe_allow_html=True)
        st.download_button("Download validated questions (JSON)", data=json.dumps(output, indent=2), file_name=f"{inc['incident_id']}_investigation_questions.json", mime="application/json")
        with st.expander("View extracted facts"):
            st.json(facts)

st.divider()
st.markdown('<p class="small-note">SENTINEL · Evidence-gap driven analysis · All model calls are logged locally; secrets and full prompts are not logged.</p>', unsafe_allow_html=True)
