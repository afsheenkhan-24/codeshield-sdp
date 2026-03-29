import os
import sqlite3
import hashlib
import subprocess
import pickle


# --- INSECURE CONFIGURATIONS (Rule 6) ---
DEBUG = True
admin_pass = "123456"
db_user = 'root'  # Also triggers Rule 4 (Least Privilege)
secure = False
external_api = "http://insecure-api.example.com/v1/data"

def process_user_data(user_input, serialized_payload):
    # --- UNSAFE INPUT HANDLING (Rule 5) ---
    
    # 1. Arbitrary Code Execution
    calculated_value = eval(user_input)
    
    # 2. OS Command Injection
    subprocess.Popen(f"echo {user_input}", shell=True)
    
    # 3. Unsafe OS Execution
    os.system("ping -c 4 " + user_input)
    
    # 4. Unsafe Deserialization
    data_object = pickle.loads(serialized_payload)
    
    return calculated_value, data_object

def authenticate_user(username, password):
    # --- WEAK CRYPTOGRAPHY (Rule 3) ---
    
    # 1. Weak Hashing
    password_hash = hashlib.md5(password.encode()).hexdigest()
    

    
    # --- SQL INJECTION (Rule 4) ---
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # F-string SQL Injection
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password_hash}'"
    cursor.execute(query)
    
    # Format string SQL Injection
    cursor.execute("UPDATE users SET last_login = 'now' WHERE username = '{}'".format(username))
    
    return True