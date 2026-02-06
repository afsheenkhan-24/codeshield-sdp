def read_file(file_path):
    try:
        with open(file_path, "r") as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except IOError:
        print(f"Error: An I/O error occurred while reading the file '{file_path}'.")


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

