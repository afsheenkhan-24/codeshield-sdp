import streamlit as st
from pages.dashboard import Dashboard
from pages.settings import Settings
from pages.complexity import calculate_complexity, calculate_nodes_and_edges, count_loc
from pages.rules import SecurityConcerns
from utils.supabase_client import insert_code

st.set_page_config(
    page_title="CodeShield",
    layout="wide",
    initial_sidebar_state="expanded",
)

def Complexity():
    st.header("Code Analysis and Security Tool")


    # Initialise session state
    if "analysis_done" not in st.session_state:
        st.session_state.analysis_done = False

    if "file_content" not in st.session_state:
        st.session_state.file_content = ""

    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None

    if "scanner" not in st.session_state:
        st.session_state.scanner = SecurityConcerns()


    # Tabs for Upload, Paste Code, and Result
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

            st.text_area(
                "File Preview",
                value=st.session_state.file_content,
                height=200,
                disabled=True,
            )

            if st.button("Run Analysis", key="run_upload"):
                if file_text:
                    scanner = SecurityConcerns()

                    loc = count_loc(file_text)
                    insert_code(
                        code_title=code_title or "Untitled file",
                        code_type="File Upload",
                        loc=loc,
                        code_file_bytes=file_bytes,
                        pasted_code_text=None,
                    )

                    st.session_state.analysis_done = True
                    st.success("Analysis complete! Go to the Result tab.")
                else:
                    st.warning("Please upload a file first.")

    # ---- Paste Code tab ----
    with tab_paste:
        code_paste_title = st.text_input("Enter a title for your code", key="code_paste_title")
        code_input = st.text_area("Paste Python code here", height=200, key="code_input")
        
        if st.button("Run Analysis", key="run_paste"):
            if code_input.strip():
                st.session_state.file_content = code_input
                st.session_state.uploaded_file = None

                loc = count_loc(code_input)
                insert_code(
                    code_title=code_paste_title or "Untitled paste",
                    code_type="Pasted Code",
                    loc=loc,
                    code_file_bytes=None,
                    pasted_code_text=code_input,
                )

                st.session_state.analysis_done = True
                st.success("Analysis complete! Go to the Result tab.")
            else:
                st.warning("Please paste some code first.")

    
    # ---- Result tab ----
    with tab_result:
        if not st.session_state.analysis_done:
            st.info("No analysis data available."
                "Please upload or paste code in the previous tabs first."
            )
        else:
            code = st.session_state.file_content
            scanner = st.session_state.scanner

            # Run security rules
            results = scanner.run_all_rules(
                code,
                st.session_state.uploaded_file,
            )

            # LOC (non-empty, non-comment)
            LOC = sum(
                1
                for line in code.splitlines()
                if line.strip() and not line.strip().startswith("#")
            )
    
            # Nodes, edges, cyclomatic complexity
            nodes, edges = calculate_nodes_and_edges(code)
            cc = calculate_complexity(nodes, edges)

            # Vulnerability density
            red_flags = len(results)
            vd = (red_flags / LOC) * 1000 if LOC > 0 else 0

            # Technical depth index
            tdi = (cc + vd) / 2

            # Show metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Technical Depth Index (TDI)", f"{tdi:.2f}")
            with col2:
                st.metric("Cyclomatic Complexity", cc)
                st.write(f"Nodes (N): {nodes}")
                st.write(f"Edges (E): {edges}")
            with col3:
                st.metric("Vulnerability Density", f"{vd:.2f}")
                st.write(f"Number of Red Flags: {red_flags}")

            st.markdown("---")

            st.subheader("Identified Security Red Flags")
            if red_flags > 0:
                for report in results:
                    st.write(f"**{report['rule_title']}**")
                    st.write(report["description"])
                    st.write("---")
            else:
                st.write("No security vulnerabilities identified.")

            if st.button("Generate Report"):
                pass

pg = st.navigation([Dashboard, Complexity, Settings])
pg.run()