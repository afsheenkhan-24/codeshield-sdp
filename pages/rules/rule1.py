import re
def rule_1(content, file_object: None):
    lines = content.splitlines()
    findings=[]
    pattern = r"(\w*(?:API|TOKEN)\w*)\s*=\s*['\"]([^'\"]+)['\"]"
    
    for i, line in enumerate(lines):
        match = re.search(pattern, line, re.IGNORECASE)
        if match:
            variable_name = match.group(1)
            findings.append({
                "rule_title": "Hardcoded Credential",
                "rule": "Rule 1",
                "description": f"Hardcoded credential detected in line {i + 1}: '{variable_name}'",
                "severity": 2, # High
                "justification": "If an API key is exposed, malicious actors could take advantage of the source code to cause harm such as a possible data breach."
            })
    return findings