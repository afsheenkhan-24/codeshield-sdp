import streamlit as st
from utils.supabase_client import get_supabase_client
from datetime import datetime, timedelta, timezone
import pandas as pd


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


def render_metric_card(label, value, delta_text=None, delta_positive=None):
    """Render a styled metric with optional delta indicator."""
    if delta_text is not None:
        icon = "▲" if delta_positive else "▼"
        color = "green" if delta_positive else "red"
        st.metric(label=label, value=value, delta=f"{icon} {delta_text}")
    else:
        st.metric(label=label, value=value)


def Dashboard():
    st.header("Dashboard")
    name = st.session_state.get("profile", {}).get("full_name", "")
    greeting = f"Welcome back, {name}!" if name else "Welcome back!"
    st.subheader(greeting)
    st.caption("Here's an overview of your code analysis activity.")

    # ---- Load data ----
    with st.spinner("Loading dashboard data..."):
        try:
            records = get_dashboard_data()
            # st.table(records)
        except Exception as e:
            st.error(f"Failed to load data from Supabase: {e}")
            return

    if not records:
        st.info("No scans yet. Upload or paste code in the **Complexity** tab to get started.")
        return
    
    # st.markdown("---")
    
    metrics = compute_metrics(records)
 
    # ---- Summary metric cards ----
    col1, col2, col3 = st.columns(3)
 
    with col1:
        delta_str = None
        delta_pos = None
        if metrics["week_delta"] is not None:
            delta_str = f"{abs(metrics['week_delta'])}% vs last week"
            delta_pos = metrics["week_delta"] >= 0
        render_metric_card(
            "Total scans",
            metrics["total_scans"],
            delta_str,
            delta_pos,
        )
 
    with col2:
        render_metric_card(
            "Scans this week",
            metrics["scans_this_week"],
        )
 
    with col3:
        render_metric_card(
            "Avg lines of code",
            metrics["avg_loc"],
        )
 
    st.markdown("---")

    # ---- Charts row ----
    chart_col, breakdown_col = st.columns([1, 1])
 
    with chart_col:
        st.subheader("Scan activity (last 7 days)")
        activity = metrics["activity"]
        st.bar_chart({"Scans": list(activity.values())}, x_label="Day", y_label="Scans")
        label_cols = st.columns(len(activity))
        for i, label in enumerate(activity.keys()):
            with label_cols[i]:
                st.caption(label.split(" ")[0])  # Show Mon, Tue, ....
 
    with breakdown_col:
        st.subheader("Scan type breakdown")
        type_counts = metrics["type_counts"]
        if type_counts:
            
            df = pd.DataFrame(
                {"Type": list(type_counts.keys()), "Count": list(type_counts.values())}
            ).set_index("Type")
            st.bar_chart(df)
        else:
            st.caption("No data available.")
 
    st.markdown("---")

    # ---- Recent scans table ----
    st.subheader("Recent scans")
 
    recent = records[:5]  # Show latest 5
 
    for scan in recent:
        raw_ts = scan.get("created_at", "")
        try:
            ts = datetime.fromisoformat(raw_ts.replace("Z", "+00:00"))
            date_str = ts.strftime("%d %b %Y, %H:%M")
        except Exception:
            date_str = raw_ts
 
        title = scan.get("codeTitle") or "Untitled"
        scan_type = scan.get("codeType", "—")
        loc = scan.get("linesOfCode", "—")
 
        with st.container(border=True):
            c1, c2, c3, c4 = st.columns([3, 2, 1, 2])
            c1.markdown(f"**{title}**")
            c2.caption(scan_type)
            c3.caption(f"{loc} LOC")
            c4.caption(date_str)
 
    if len(records) > 5:
        st.caption(f"Showing 5 of {len(records)} scans.")
 
 