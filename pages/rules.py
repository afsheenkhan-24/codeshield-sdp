import re

class SecurityConcerns:
    def __init__(self):
        self.findings = []

    def run_all_rules(self, content, file):
        self.rule_1(content)
        self.rule_2(file)
        return self.findings

    def rule_1(self, content):
        lines = content.splitlines()
        pattern = r"(\w*(?:API|TOKEN)\w*)\s*=\s*['\"]([^'\"]+)['\"]"
        
        for i, line in enumerate(lines):
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                variable_name = match.group(1)
                self.findings.append({
                    "rule_title": "Hardcoded Credential",
                    "rule": "Rule 1",
                    "description": f"Hardcoded credential detected in line {i + 1}: '{variable_name}'",
                    "severity": 2, # High
                    "justification": "If an API key is exposed, malicious actors could take advantage of the source code to cause harm such as a possible data breach."
                })

    def rule_2(self, file):
        if file is None:
            return

        max_size = 1024 * 1024  # 1MB 
        file_size = file.size
        
        # Check size
        if file_size > max_size:
            self.findings.append({
                "rule_title": "File Security issue",
                "rule": "Rule 2",
                "description": f"File size ({file_size / 1024:.2f} KB) exceeds 1MB limit.",
                "severity": 1, 
                "justification": "submitting a malicious file could cause the whole program to break therefore resulting in vulnerabilities"
            })
            
        #double extensions
        if file.name.count('.') > 1:
            self.findings.append({
                "rule_title": "File Security issue",
                "rule": "Rule 2",
                "description": f"Suspicious file naming: '{file.name}'",
                "severity": 1, 
                "justification": "Multiple extensions are used to hide malicious files."
            })