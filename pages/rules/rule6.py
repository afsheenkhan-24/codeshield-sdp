import ast

def rule_6(content, file_object=None):
    findings = []
    
    if not content:
        return findings

    class ConfigVisitor(ast.NodeVisitor):
        def visit_Assign(self, node):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    target_id = target.id.lower()
                    
                    if target_id in ('password', 'passwd', 'pwd', 'admin_pass'):
                        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                            if node.value.value.lower() in ('admin', 'password', '123456', 'root', 'changeme'):
                                self.add_finding(node.lineno, "Default Configuration Password")
                    
                    if target_id == 'debug':
                        if isinstance(node.value, ast.Constant) and node.value.value is True:
                            self.add_finding(node.lineno, "Debug Mode Enabled")
                            
                    if target_id in ('secure', 'httponly'):
                        if isinstance(node.value, ast.Constant) and node.value.value is False:
                            self.add_finding(node.lineno, "Insecure Cookie Configuration")

            self.generic_visit(node)

        def visit_Constant(self, node):
            if isinstance(node.value, str):
                if node.value.startswith('http://'):
                    if not any(safe_host in node.value for safe_host in ('localhost', '127.0.0.1', 'testserver')):
                        self.add_finding(node.lineno, "Unencrypted Traffic (HTTP)")
            self.generic_visit(node)

        def add_finding(self, line, config_type):
            findings.append({
                "rule": "Rule 6",
                "line": line,
                "description": f"Insecure configuration value detected: {config_type}",
                "severity": 1,
                "justification": "using vulnerable settings causes the application to be infected more easily by an attacker."
            })

    try:
        tree = ast.parse(content)
        ConfigVisitor().visit(tree)
    except SyntaxError:
        pass
        
    return findings