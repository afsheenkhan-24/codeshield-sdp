import streamlit as st
from pages.dashboard import Dashboard
from pages.settings import Settings
from pages.complexity import calculate_complexity, calculate_nodes_and_edges, count_loc
from pages.rules import *
from utils.supabase_client import insert_code, insert_result, insert_complexity, insert_flag, insert_rule
from auth import run_auth, sign_out
import requests
import os

st.set_page_config(
    page_title="CodeShield",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---- Logo ----
LOGO_PATH = "logo.jpeg"
if os.path.exists(LOGO_PATH):
    st.logo(LOGO_PATH)

# ---- Auth gate — stop here if not logged in ----
if not run_auth():
    st.stop()

# ---- Logout button in sidebar ----
with st.sidebar:
    user = st.session_state.get("user")
    if user:
        email = user.email or ""
        name = st.session_state.get("profile", {}).get("full_name", email)
        st.caption(f"Signed in as **{name}**")
        if st.button("Sign out"):
            sign_out()


# ---- LLM (Groq API) ----
def get_llm_recommendations(code: str, findings: list, tdi: float) -> str:
    if not findings and tdi < 25:
        return "No significant issues found. Code looks clean."
 
    findings_summary = "\n".join(
        f"- Line {f['line_number']}: {f['rule_title']} — {f['description']}"
        for f in findings
    )
 
    prompt = f"""You are a senior software security engineer reviewing a Python code scan.
 
TDI Score: {tdi:.2f} (threshold for high risk: 50)
Security findings:
{findings_summary}
 
Give 3-5 concise, actionable recommendations to fix the issues above.
Be specific. Reference line numbers where relevant. Keep it under 200 words."""
 
    try:
        api_key = st.secrets["GROQ_API_KEY"]
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 512,
            },
            timeout=30,
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        return f"API error {response.status_code}: {response.text}"
    except KeyError:
        return "API KEY not found."
    except Exception as e:
        return f"LLM error: {e}"

# ---- Analysis pipeline ----
def run_analysis(code: str, uploaded_file=None) -> dict:

    raw_findings = []

    if 'rule_1' in globals(): raw_findings.extend(rule_1(code, uploaded_file))
    if 'rule_2' in globals(): raw_findings.extend(rule_2(code, uploaded_file))
    if 'rule_3' in globals(): raw_findings.extend(rule_3(code, uploaded_file))
    if 'rule_4' in globals(): raw_findings.extend(rule_4(code, uploaded_file))
    if 'rule_5' in globals(): raw_findings.extend(rule_5(code, uploaded_file))
    if 'rule_6' in globals(): raw_findings.extend(rule_6(code, uploaded_file))

    findings = []
    for f in raw_findings:
        f["line_number"] = f.get("line", 0)
        f["rule_title"] = f.get("rule", "Security Alert")
        findings.append(f)

    loc = count_loc(code)
    nodes, edges = calculate_nodes_and_edges(code)
    cc = calculate_complexity(nodes, edges)

    red_flags = len(findings)
    vd = (red_flags / loc) * 1000 if loc > 0 else 0
    tdi = (cc * 0.5) + (vd * 0.5)

    if tdi >= 50:
        risk = "High Risk"
        needs_refactoring = True
    elif tdi >= 25 and tdi < 50:
        risk = "Medium Risk"
        needs_refactoring = False
    else:
        risk = "Low Risk"
        needs_refactoring = False

    return {
        "loc": loc,
        "nodes": nodes,
        "edges": edges,
        "cc": cc,
        "vd": vd,
        "tdi": tdi,
        "risk": risk,
        "needs_refactoring": needs_refactoring,
        "findings": findings,
    }


def save_to_supabase(code_title: str, code_type: str, analysis: dict, file_bytes: bytes = None, pasted_text: str = None):
    """All five table inserts after a completed analysis."""

    # 1. Codes
    code_id = insert_code(
        code_title=code_title,
        code_type=code_type,
        loc=analysis["loc"],
        code_file_bytes=file_bytes,
        pasted_code_text=pasted_text,
    )
    if code_id is None:
        st.error("Failed to save code record — aborting further saves.")
        return

    # 2. Results
    result_id = insert_result(
        code_id=code_id,
        complexity_score=analysis["cc"],
        vulnerability_density=analysis["vd"],
        tdi_score=analysis["tdi"],
        risk_classification=analysis["risk"],
        needs_refactoring=analysis["needs_refactoring"],
    )
    if result_id is None:
        st.error("Failed to save result record — aborting further saves.")
        return

    # 3. Complexities
    insert_complexity(
        result_id=result_id,
        edges=analysis["edges"],
        nodes=analysis["nodes"],
        connected_components=1,
        decision_points=analysis["nodes"],
    )

    # 4. Rules + Flags
    for finding in analysis["findings"]:
        rule_id = insert_rule(
            rule_name=finding["rule_title"],
            rule_descr=finding["justification"],
        )
        if rule_id:
            insert_flag(
                result_id=result_id,
                rule_id=rule_id,
                line_number=finding.get("line_number", 0),
            )


# ---- Complexity page ----
def Complexity():
    st.header("Code Analysis and Security Tool")

    # Session state initialisation
    for key, default in [
        ("analysis_done", False),
        ("file_content", ""),
        ("uploaded_file", None),
        ("analysis_result", None),
        ("llm_response", None),
    ]:
        if key not in st.session_state:
            st.session_state[key] = default

    tab_upload, tab_paste, tab_result = st.tabs(["Upload", "Paste Code", "Result"])

    # ---- Upload tab ----
    with tab_upload:
        code_title = st.text_input("Enter a title for your code", key="code_title")
        uploaded_file = st.file_uploader("Choose a .py file", type=[".py"])

        if uploaded_file is not None:
            st.session_state.uploaded_file = uploaded_file
            file_bytes = uploaded_file.getvalue()
            file_text = file_bytes.decode("utf-8")
            st.session_state.file_content = file_text
            st.text_area("File preview", value=file_text, height=200, disabled=True)

            if st.button("Run Analysis", key="run_upload", type='primary'):
                if file_text:
                    with st.spinner("Analysing..."):
                        result = run_analysis(file_text, uploaded_file)
                        save_to_supabase(
                            code_title=code_title or "Untitled file",
                            code_type="File Upload",
                            analysis=result,
                            file_bytes=file_bytes,
                        )
                        st.session_state.analysis_result = result
                        st.session_state.analysis_done = True
                        st.session_state.llm_response = None  # reset previous
                    st.success("Analysis complete! Go to the Result tab.")
                else:
                    st.warning("Please upload a file first.")

    # ---- Paste tab ----
    with tab_paste:
        code_paste_title = st.text_input("Enter a title for your code", key="code_paste_title")
        code_input = st.text_area("Paste Python code here", height=200, key="code_input")

        if st.button("Run Analysis", key="run_paste", type='primary'):
            if code_input.strip():
                with st.spinner("Analysing..."):
                    result = run_analysis(code_input)
                    save_to_supabase(
                        code_title=code_paste_title or "Untitled paste",
                        code_type="Pasted Code",
                        analysis=result,
                        pasted_text=code_input,
                    )
                    st.session_state.file_content = code_input
                    st.session_state.uploaded_file = None
                    st.session_state.analysis_result = result
                    st.session_state.analysis_done = True
                    st.session_state.llm_response = None
                st.success("Analysis complete! Go to the Result tab.")
            else:
                st.warning("Please paste some code first.")

    # ---- Result tab ----
    with tab_result:
        if not st.session_state.analysis_done or st.session_state.analysis_result is None:
            st.info("No analysis yet. Upload or paste code first.")
            return

        r = st.session_state.analysis_result

        if r["tdi"] >= 50:
            st.error(
                f"HIGH RISK — TDI score of {r['tdi']:.2f} exceeds the threshold of 50. "
                "Immediate refactoring is recommended."
            )
        elif r["tdi"] >= 25:
            st.warning(f"MEDIUM RISK — TDI score of {r['tdi']:.2f}.")
        else:
            st.success(f"LOW RISK — TDI score of {r['tdi']:.2f}.")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Technical Debt Index (TDI)", f"{r['tdi']:.2f}")
            st.caption(f"Risk: {r['risk']}")
        with col2:
            st.metric("Cyclomatic Complexity", r["cc"])
            st.write(f"Nodes (N): {r['nodes']}")
            st.write(f"Edges (E): {r['edges']}")
        with col3:
            st.metric("Vulnerability Density", f"{r['vd']:.2f}")
            st.write(f"Red flags found: {len(r['findings'])}")
            st.write(f"Lines of code: {r['loc']}")

        st.markdown("---")

        st.subheader("Security red flags")
        if r["findings"]:
            severity_styles = {
                1: {"label": "Low", "color": "green", "bg-color": "green-background"},
                2: {"label": "Medium", "color": "orange", "bg-color": "orange-background"}, 
                3: {"label": "High", "color": "red", "bg-color": "red-background"}
            }
            for finding in r["findings"]:
                with st.container(border=True):
                    style = severity_styles.get(finding["severity"], {"label": "Unknown", "color": "gray", "bg-color": "gray-background"})
                    col_a, col_b = st.columns([4, 1])
                    col_a.markdown(f"**{finding['description']}**")
                    col_b.markdown(f":{style['bg-color']}[**:{style['color']}[{style['label']}]**]")
                    st.caption(f"Why this matters: {finding['justification']}")
        else:
            st.success("No security vulnerabilities identified.")

        st.markdown("---")

        # LLM recommendations via Groq API
        st.subheader("AI recommendations")
 
        if st.button("Generate AI recommendations", type='primary'):
            with st.spinner("Asking LLM..."):
                llm_response = get_llm_recommendations(
                    st.session_state.file_content,
                    r["findings"],
                    r["tdi"],
                )
                st.session_state.llm_response = llm_response
 
        if st.session_state.llm_response:
            st.info(st.session_state.llm_response)


pg = st.navigation([Dashboard, Complexity, Settings])
pg.run()