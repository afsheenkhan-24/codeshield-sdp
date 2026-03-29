import ast

def rule_5(content, file_object=None):
    findings = []
    
    if not content:
        return findings

    class ExecutionVisitor(ast.NodeVisitor):
        def visit_Call(self, node):
            if isinstance(node.func, ast.Name):
                if node.func.id in ('eval', 'exec'):
                    self.add_finding(node.lineno, f"Arbitrary Code Execution ({node.func.id})")
                    
            elif isinstance(node.func, ast.Attribute):
                if node.func.attr in ('system', 'popen'):
                    self.add_finding(node.lineno, f"Unsafe OS Execution ({node.func.attr})")
                elif node.func.attr in ('loads', 'load'):
                    self.add_finding(node.lineno, f"Unsafe Deserialization ({node.func.attr})")

            for kw in node.keywords:
                if kw.arg == 'shell' and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                    self.add_finding(node.lineno, "OS Command Injection (shell=True)")
                    
            self.generic_visit(node)

        def add_finding(self, line, risk_type):
            findings.append({
                "rule": "Rule 5",
                "line": line,
                "description": f"Unsafe input handling detected: {risk_type}",
                "severity": 3,
                "justification": "if the program runs the code, it could contain malware and infect the program entirely"
            })

    try:
        tree = ast.parse(content)
        ExecutionVisitor().visit(tree)
    except SyntaxError:
        pass
        
    return findings