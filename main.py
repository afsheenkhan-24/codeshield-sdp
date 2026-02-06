from parser import read_file, calculate_complexity
import os

filepath = "test.py"


def process_file(filepath):
    content = read_file(filepath)
    M = calculate_complexity(content)
    print(f"{filepath}")
    print(f"Complexity Score = {M}")


def run_scanner():
    path = input("Enter the path to a file or folder to scan: ").strip()

    if os.path.isfile(path): #Single file
        process_file(path)
    elif os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    process_file(full_path)
    else:
        print("Invalid path. Please enter a valid file or directory.")


if __name__ == "__main__":
    run_scanner()