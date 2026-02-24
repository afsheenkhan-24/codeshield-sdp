def calculate_complexity(nodes_and_edges):
    nodes=nodes_and_edges[0]
    edges=nodes_and_edges[1]
    count = edges - nodes + 2
    return count



def calculate_nodes_and_edges(content):
 
    lines = content.splitlines()
    nodes = sum(1 for line in lines if line.strip() and not line.strip().startswith("#")) + 2
    
    decision_keywords = ["if ", "elif ", "while ", "for ", "except "]
  
    edges = nodes - 1
    for line in lines:
        line = line.strip()
        for word in decision_keywords:
            if line.startswith(word):
                edges += 1
    
    
    nodes_and_edges = [nodes,edges]
    return nodes_and_edges

