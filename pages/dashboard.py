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


def compute_metrics(records):
    # Total scans
    total_scans = len(records)
 
    # Scans this week vs last week
    now = datetime.now(timezone.utc)
    one_week_ago = now - timedelta(days=7)
    two_weeks_ago = now - timedelta(days=14)
 
    this_week = [
        r for r in records
        if datetime.fromisoformat(r["created_at"].replace("Z", "+00:00")) >= one_week_ago
    ]
    last_week = [
        r for r in records
        if two_weeks_ago
        <= datetime.fromisoformat(r["created_at"].replace("Z", "+00:00"))
        < one_week_ago
    ]
 
    scans_this_week = len(this_week)
    scans_last_week = len(last_week)
 
    if scans_last_week > 0:
        week_delta = round(((scans_this_week - scans_last_week) / scans_last_week) * 100)
    else:
        week_delta = None
 
    # Average LOC
    locs = [r["linesOfCode"] for r in records if r.get("linesOfCode") is not None]
    avg_loc = round(sum(locs) / len(locs)) if locs else 0
 
    # Scan activity for the last 7 days (count per day)
    activity = {}
    for i in range(6, -1, -1):
        day = (now - timedelta(days=i)).strftime("%a %d %b")
        activity[day] = 0
 
    for r in records:
        ts = datetime.fromisoformat(r["created_at"].replace("Z", "+00:00"))
        if ts >= one_week_ago:
            day_key = ts.strftime("%a %d %b")
            if day_key in activity:
                activity[day_key] += 1
 
    # Breakdown by scan type
    type_counts = {}
    for r in records:
        t = r.get("codeType", "Unknown")
        type_counts[t] = type_counts.get(t, 0) + 1
 
    return {
        "total_scans": total_scans,
        "scans_this_week": scans_this_week,
        "week_delta": week_delta,
        "avg_loc": avg_loc,
        "activity": activity,
        "type_counts": type_counts,
    }


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
