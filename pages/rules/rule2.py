import ast

def rule_2(content, file_object=None):
    findings = []
    
    if not content:
        return findings

    class DoSVisitor(ast.NodeVisitor):
        def visit_Import(self, node):
            for alias in node.names:
                if alias.name.startswith('xml.etree'):
                    self.add_finding(node.lineno, "Vulnerable XML Parser (XML Bomb/DoS risk)")
            self.generic_visit(node)

        def visit_ImportFrom(self, node):
            if node.module and node.module.startswith('xml.etree'):
                self.add_finding(node.lineno, "Vulnerable XML Parser (XML Bomb/DoS risk)")
            self.generic_visit(node)

        def visit_Call(self, node):
            if isinstance(node.func, ast.Attribute) and node.func.attr == 'read':
                if not node.args and not node.keywords: # .read() called with no size limit
                    self.add_finding(node.lineno, "Unbound File Read (Memory Exhaustion/DoS risk)")

            self.generic_visit(node)

        def add_finding(self, line, risk_type):
            findings.append({
                "rule": "Rule 2",
                "line": line,
                "description": f"Potential Application Denial of Service (DoS): {risk_type}",
                "severity": 2, 
                "justification": "Malicious individuals may exploit this to flood the application's memory or CPU, causing it to crash or underperform for its users."
            })

    try:
        tree = ast.parse(content)
        DoSVisitor().visit(tree)
    except SyntaxError:
        pass
        
    return findings