import sys
import re

class SQLAuditor:
    def __init__(self, file_path):
        # Step 1: Initialize the auditor and load the file
        try:
            with open(file_path, 'r') as f:
                self.sql_content = f.read()
            self.reports = [] 
            self.total_issues = 0  # Added this to keep track of total errors found
            print(f"--- Loaded SQL File: '{file_path}' ---")
        except FileNotFoundError:
            print(f"Error: I couldn't find the file '{file_path}'. Check the path!")
            sys.exit(1)

    def run_audit(self):
        # Step 2: Use Regex to find table definitions
        table_matches = re.findall(r"CREATE TABLE (.*?) \((.*?)\);", self.sql_content, re.DOTALL | re.IGNORECASE)
        
        for name, body in table_matches:
            # Cleaning up the name (removing quotes or spaces around it)
            clean_name = name.strip().replace('"', '').replace("'", "")
            print(f"\nScanning Table Structure: {clean_name}...")
            
            # CHECK 1: Primary Keys (Crucial for database indexing)
            if "PRIMARY KEY" not in body.upper():
                print(f"  ❌ Issue: '{clean_name}' has no Primary Key. This is a performance risk.")
                self.total_issues += 1  # Increment the counter

            # CHECK 2: Naming Conventions (Looking for spaces)
            if " " in clean_name:
                print(f"  ⚠️ Warning: '{clean_name}' has spaces in the name. Use underscores (snake_case).")
                self.total_issues += 1  # Increment the counter

            # CHECK 3: Performance Optimization (TEXT vs VARCHAR)
            if "TEXT" in body.upper():
                print(f"  💡 Suggestion: Found 'TEXT' type. Consider 'VARCHAR' if the length is under 255 chars.")
                self.total_issues += 1  # Increment the counter

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python auditor.py <your_sql_file.sql>")
    else:
        app = SQLAuditor(sys.argv[1])
        app.run_audit()