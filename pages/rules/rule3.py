import ast

def rule_3(content, file_object=None):
    findings = []
    
    if not content:
        return findings

    class CryptoVisitor(ast.NodeVisitor):
        def visit_Call(self, node):
            weak_methods = {'md5', 'sha1', 'des', 'des3', 'arc4', 'rc4', 'blowfish'}
            
            if isinstance(node.func, ast.Attribute):
                if node.func.attr.lower() in weak_methods:
                    self.add_finding(node.lineno, node.func.attr)
                    
            elif isinstance(node.func, ast.Name):
                if node.func.id.lower() in weak_methods:
                    self.add_finding(node.lineno, node.func.id)
                    
            self.generic_visit(node)

        def add_finding(self, line, algo):
            findings.append({
                "rule": "Rule 3",
                "line": line,
                "description": f"Use of weak cryptography detected: {algo}",
                "severity": 2,
                "justification": "old hashing algorithms and old encryption techniques are easily crackable or reversable causing private data to be decrypted by a malicious user"
            })

    try:
        tree = ast.parse(content)
        CryptoVisitor().visit(tree)
    except SyntaxError:
        pass
        
    return findings