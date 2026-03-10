import ast

def count_loc(code: str) -> int:
    """Non-blank, non-comment lines."""
    return max(
        sum(1 for l in code.splitlines() if l.strip() and not l.strip().startswith("#")),
        1,
    )

def calculate_complexity(nodes, edges):
    if nodes == 0:
        return 1  
    # Cyclomatic Complexity Formula: M = E - N + 2
    return edges - nodes + 2

def calculate_nodes_and_edges(code):
    try:
        tree = ast.parse(code)
    except Exception as e:
        print(f"Error parsing code: {e}")
        return 0, 0

    class MetricVisitor(ast.NodeVisitor):
        def __init__(self):
            self.nodes = 0
            self.edges = 0

        def visit_If(self, node):
            self.nodes += 1
            self.edges += 2
            self.generic_visit(node)

        def visit_For(self, node):
            self.nodes += 1
            self.edges += 2
            self.generic_visit(node)

        def visit_While(self, node):
            self.nodes += 1
            self.edges += 2
            self.generic_visit(node)

        def visit_FunctionDef(self, node):
            self.nodes += 1
            self.edges += 1
            self.generic_visit(node)

    visitor = MetricVisitor()
    visitor.visit(tree)
    
    print(f"--- Metrics Calculated ---")
    print(f"Nodes: {visitor.nodes}")
    print(f"Edges: {visitor.edges}")
    
    return visitor.nodes, visitor.edges

