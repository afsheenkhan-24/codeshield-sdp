def calculate_complexity(content):
    decision_keywords = ["if ", "elif ", "while ", "for "]
    
    count = 1 #M = D.P + 1
    lines = content.splitlines()
    
    for line in lines:
        line = line.strip()
        for word in decision_keywords:
            if line.startswith(word):
                count += 1
    
    return count

