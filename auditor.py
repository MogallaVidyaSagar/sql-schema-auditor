import sys
import re

class SQLAuditor:
    def __init__(self, file_path):
        # Initializing the auditor and loading the user's SQL file
        try:
            with open(file_path, 'r') as f:
                self.sql_content = f.read()
            self.reports = [] 
            self.total_issues = 0  # To track how many errors we find in total
            print(f"--- Loaded SQL File: '{file_path}' ---")
        except FileNotFoundError:
            print(f"Error: I couldn't find the file '{file_path}'. Check the path!")
            sys.exit(1)

    def run_audit(self):
        # Using Regex to find table definitions (looking for CREATE TABLE + content inside brackets)
        table_matches = re.findall(r"CREATE TABLE (.*?) \((.*?)\);", self.sql_content, re.DOTALL | re.IGNORECASE)
        
        for name, body in table_matches:
            # Cleaning up the name (removing quotes or spaces around it)
            clean_name = name.strip().replace('"', '').replace("'", "")
            print(f"\nScanning Table Structure: {clean_name}...")
            
            # CHECK 1: Primary Keys (Crucial for database indexing)
            if "PRIMARY KEY" not in body.upper():
                print(f"  ❌ Issue: '{clean_name}' has no Primary Key. This is a performance risk.")
                self.total_issues += 1 

            # CHECK 2: Naming Conventions (Looking for spaces in table names)
            if " " in clean_name:
                print(f"  ⚠️ Warning: '{clean_name}' has spaces in the name. Use underscores (snake_case).")
                self.total_issues += 1

            # CHECK 3: Performance (Suggesting VARCHAR instead of TEXT)
            if "TEXT" in body.upper():
                print(f"  💡 Suggestion: Found 'TEXT' type. Consider 'VARCHAR' for smaller fields.")
                self.total_issues += 1

    # Final method to show the overall results in a clean box
    def print_summary(self):
        print("\n" + "="*40)
        print("📊 FINAL AUDIT SUMMARY")
        print("="*40)
        print(f"Total Database Issues Detected: {self.total_issues}")
        print("="*40)
        
        if self.total_issues == 0:
            print("✨ Perfect! No issues found in your schema.")
        else:
            print("🛠️ Please review the suggestions above to optimize your database.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python auditor.py <your_sql_file.sql>")
    else:
        app = SQLAuditor(sys.argv[1])
        app.run_audit()
        app.print_summary() # Calling the summary at the very end