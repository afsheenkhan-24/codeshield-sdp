import streamlit as st
from utils.supabase_client import get_supabase_client
from datetime import datetime, timedelta, timezone


def get_dashboard_data():
    supabase = get_supabase_client()

    # Fetch all scan records, ordered by newest first
    response = (
        supabase.table("Codes")
        .select("codeId, codeTitle, codeType, linesOfCode, created_at")
        .order("created_at", desc=True)
        .execute()
    )
    return response.data or []

def Dashboard():
    st.title("Dashboard")
    st.caption("Overview of your code analysis activity")

    # ── Load data ──────────────────────────────────────────────────────────────
    with st.spinner("Loading dashboard data..."):
        try:
            records = get_dashboard_data()
            st.table(records)
        except Exception as e:
            st.error(f"Failed to load data from Supabase: {e}")
            return

    if not records:
        st.info("No scans yet. Upload or paste code in the **Complexity** tab to get started.")
        return

    st.markdown("---")
