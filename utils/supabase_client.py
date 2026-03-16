import base64
import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def get_supabase_client() -> Client:
    url = st.secrets["SUPABASE_URL"] 
    key = st.secrets["SUPABASE_KEY"] 
    return create_client(url, key)

supabase: Client = get_supabase_client()

def insert_code(code_title: str, code_type: str, loc: int, code_file_bytes: bytes = None, pasted_code_text: str = None):
    data = {
        "codeTitle": code_title,
        "codeType": code_type,
        "linesOfCode": loc,
        "pastedCode": pasted_code_text,
    }

    if code_file_bytes:
        encoded_file = base64.b64encode(code_file_bytes).decode('utf-8')
        data["codeFile"] = encoded_file

    try:
        response = supabase.table("Codes").insert(data).execute()
        return response
    except Exception as e:
        st.error(f"Database insertion error: {e}")
        return None
    