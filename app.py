from dashboard import Dashboard
from settings import Settings
import streamlit as st
from analysis import calculate_complexity

def Complexity():
    st.title("Code Analysis and Security Tool")

    tab1, tab2 = st.tabs(["Upload", "Paste Code"]) 

    with tab1:
        uploaded_file = st.file_uploader("Choose a .py file to analyse complexity and security issues", type=[".py"])
    
        if uploaded_file is not None:
            st.divider()
            file_content = uploaded_file.read().decode("utf-8")
            st.text_area("Code", value=file_content, height=300, disabled=True, help="This area displays the content of the uploaded file.")
            # st.button("Run Analysis", type="primary", on_click=calculate_complexity, args=(file_content,))
            st.write("Complexity Score: " + str(calculate_complexity(file_content)), ) 
            st.divider()

    with tab2:
        code_input = st.text_area("Paste your Python code here to analyse complexity and security issues", height=300, key="code_input", help="This area allows you to paste your Python code for analysis.")
        st.button("Run Analysis", type="primary", on_click=calculate_complexity, args=(code_input,))
        st.write("Complexity Score: " + str(calculate_complexity(code_input)), ) 

pg = st.navigation([Dashboard, Complexity, Settings])
pg.run()

