from parser import read_file, calculate_complexity

filepath = "test.py"

content = read_file(filepath)
M = calculate_complexity(content)
print(content)
print(f"Complexity Score = {M}")