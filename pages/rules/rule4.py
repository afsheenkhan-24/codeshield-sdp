import ast

def rule_4(content, file_object=None):
    findings = []
    
    if not content:
        return findings

    class SQLVisitor(ast.NodeVisitor):
        def visit_Call(self, node):
            if isinstance(node.func, ast.Attribute) and node.func.attr == 'execute':
                if node.args:
                    arg = node.args[0]
                    if isinstance(arg, ast.JoinedStr):
                        self.add_finding(node.lineno, "F-string SQL Injection")
                    elif isinstance(arg, ast.BinOp):
                        self.add_finding(node.lineno, "Dynamic string SQL Injection")
                    elif isinstance(arg, ast.Call) and isinstance(arg.func, ast.Attribute) and arg.func.attr == 'format':
                        self.add_finding(node.lineno, "Format string SQL Injection")
            
            for kw in node.keywords:
                if kw.arg in ('user', 'username') and isinstance(kw.value, ast.Constant) and kw.value.value == 'root':
                    self.add_finding(node.lineno, "Violation of Least Privilege (Root User)")
            
            self.generic_visit(node)
            
        def visit_Assign(self, node):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in ('user', 'username'):
                    if isinstance(node.value, ast.Constant) and node.value.value == 'root':
                        self.add_finding(node.lineno, "Violation of Least Privilege (Root User)")
            
            self.generic_visit(node)

        def add_finding(self, line, risk_type):
            findings.append({
                "rule": "Rule 4",
                "line": line,
                "description": f"SQL Risk detected: {risk_type}",
                "severity": 3,
                "justification": "if the SQL database is not protected an attacker can easily gain access to the confidential information stored on the database"
            })

    try:
        tree = ast.parse(content)
        SQLVisitor().visit(tree)
    except SyntaxError:
        pass
        
    return findings