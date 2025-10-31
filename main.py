# NOTE: contains intentional security test patterns for SAST/SCA/IaC scanning.
import sqlite3
import subprocess
import json  # Changed from pickle to json for safer serialization
import os

# hardcoded API token (Issue 1)
API_TOKEN = "AKIAEXAMPLERAWTOKEN12345"

# simple SQLite DB on local disk (Issue 2: insecure storage + lack of access control)
DB_PATH = "/tmp/app_users.db"
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
conn.commit()

def add_user(username, password):
    # Fixed SQL injection vulnerability by using parameterized query (Issue 3)
    sql = "INSERT INTO users (username, password) VALUES (?, ?)"
    cur.execute(sql, (username, password))
    conn.commit()

def get_user(username):
    # Fixed SQL injection vulnerability by using parameterized query (Issue 3)
    q = "SELECT id, username FROM users WHERE username = ?"
    cur.execute(q, (username,))
    return cur.fetchall()

def run_shell(command):
    # Warning: command injection risk if command includes unsanitized input (Issue 4)
    # Consider using more specific functions instead of arbitrary shell commands
    return subprocess.getoutput(command)

def deserialize_blob(blob):
    # Fixed insecure deserialization by using json instead of pickle (Issue 5)
    try:
        return json.loads(blob)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON data")

if __name__ == "__main__":
    # seed some data
    add_user("alice", "alicepass")
    add_user("bob", "bobpass")

    # Demonstrate risky calls
    print("API_TOKEN in use:", API_TOKEN)
    print(get_user("alice"))  # No longer vulnerable to SQLi
    print(run_shell("echo Hello && whoami"))
    try:
        # attempting to deserialize a JSON string (safer than pickle)
        print(deserialize_blob('{"key": "value"}'))
    except ValueError as e:
        print("Deserialization error:", e)