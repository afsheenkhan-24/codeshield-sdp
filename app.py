from dashboard import Dashboard
from settings import Settings
import streamlit as st
from analysis import calculate_complexity

def Complexity():
    st.title("Code Analysis and Security Tool")
    if 'analysis_done' not in st.session_state:
        st.session_state.analysis_done = False

    tab1, tab2, tab3 = st.tabs(["Upload", "Paste Code", "Result"]) 

    with tab1:
        uploaded_file = st.file_uploader("Choose a .py file", type=[".py"])
        if uploaded_file is not None:
            st.session_state.file_content = uploaded_file.read().decode("utf-8")
            st.text_area("File Preview", value=st.session_state.file_content, height=200, disabled=True)
            if st.button("Run Analysis", key="run_upload", type="primary"):
                st.session_state.analysis_done = True
                st.success("Analysis complete! Head to the Results tab.")

    with tab2:
        code_input = st.text_area("Paste Python code here", height=200, key="code_input")
        if st.button("Run Analysis", key="run_paste", type="primary"):
            if code_input:
                st.session_state.analysis_done = True
                st.success("Analysis complete! Head to the Results tab.")
            else:
                st.warning("Please paste some code first.") 
    
    with tab3:
        if not st.session_state.analysis_done:
            st.info("No analysis data available. Please upload or paste code in the previous tabs first.")
        else:
            tdi = 0
            tdi_label = "Critical"
            cc = calculate_complexity(st.session_state.file_content)
            nodes, edges = 0, 0
            vd = 0
            red_flags = 0

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f'<div class="card"><div class="title">Technical Depth Index (TDI)</div><div class="value">{tdi}</div><div class="critical-label">{tdi_label}</div></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="card"><div class="title">Cyclomatic Complexity</div><div class="value">{cc}</div><div class="nodes-edges">Nodes(N): {nodes}<br>Edges (E): {edges}</div></div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<div class="card"><div class="title">Vulnerability Density</div><div class="value">{vd}</div><div class="red-flags">No.of.Red Flags: {red_flags}</div></div>', unsafe_allow_html=True)


            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Generate Report"):
                pass

pg = st.navigation([Dashboard, Complexity, Settings])
pg.run()