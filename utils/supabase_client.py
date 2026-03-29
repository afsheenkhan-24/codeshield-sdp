import streamlit as st
from supabase import create_client, Client
import base64


@st.cache_resource
def get_supabase_client() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


supabase: Client = get_supabase_client()


def insert_code(code_title: str, code_type: str, loc: int,
                code_file_bytes: bytes = None, pasted_code_text: str = None) -> int | None:
    """Insert into Codes table, return codeId."""
    data = {
        "codeTitle": code_title,
        "codeType": code_type,
        "linesOfCode": loc,
        "pastedCode": pasted_code_text,
    }
    if code_file_bytes:
        data["codeFile"] = base64.b64encode(code_file_bytes).decode("utf-8")

    try:
        response = supabase.table("Codes").insert(data).execute()
        return response.data[0]["codeId"] if response.data else None
    except Exception as e:
        st.error(f"Error saving code: {e}")
        return None


def insert_result(code_id: int, complexity_score: int, vulnerability_density: float,
                  tdi_score: float, risk_classification: str,
                  needs_refactoring: bool) -> int | None:
    """Insert into Results table, return resultId."""
    data = {
        "codeId": code_id,
        "complexityScore": complexity_score,
        "vulnerabilityDensity": round(vulnerability_density),
        "tdiScore": round(tdi_score),
        "riskClassification": risk_classification,
        "needsRefactoring": needs_refactoring,
    }
    try:
        response = supabase.table("Results").insert(data).execute()
        return response.data[0]["resultId"] if response.data else None
    except Exception as e:
        st.error(f"Error saving result: {e}")
        return None


def insert_complexity(result_id: int, edges: int, nodes: int,
                      connected_components: int = 1,
                      decision_points: int = 0) -> None:
    """Insert into Complexities table."""
    data = {
        "resultsId": result_id,
        "edges": edges,
        "nodes": nodes,
        "connectedComponents": connected_components,
        "decisionPoints": decision_points,
    }
    try:
        supabase.table("Complexities").insert(data).execute()
    except Exception as e:
        st.error(f"Error saving complexity: {e}")


def insert_rule(rule_name: str, rule_descr: str) -> int | None:
    """Upsert a rule by name, return its ruleId."""
    try:
        existing = supabase.table("Rules").select("ruleId").eq("ruleName", rule_name).execute()
        if existing.data:
            return existing.data[0]["ruleId"]
        response = supabase.table("Rules").insert(
            {"ruleName": rule_name, "ruleDescr": rule_descr}
        ).execute()
        return response.data[0]["ruleId"] if response.data else None
    except Exception as e:
        st.error(f"Error saving rule: {e}")
        return None


def insert_flag(result_id: int, rule_id: int, line_number: int) -> None:
    """Insert into Flags table."""
    try:
        supabase.table("Flags").insert({
            "resultId": result_id,
            "ruleId": rule_id,
            "lineNumber": line_number,
        }).execute()
    except Exception as e:
        st.error(f"Error saving flag: {e}")