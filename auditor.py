import sys

# Step 1: Create the main class to handle SQL files
class SQLAuditor:
    def __init__(self, file_path):
        # We need to try and open the file the user gives us
        try:
            with open(file_path, 'r') as f:
                self.sql_content = f.read()
            self.reports = [] 
            self.total_issues = 0  # Added this to keep track of total errors found
            print(f"--- Loaded SQL File: '{file_path}' ---")
        except FileNotFoundError:
            print(f"Error: I couldn't find the file '{file_path}'. Check the path!")
            sys.exit(1)
# This part runs when we call the script from the terminal
if __name__ == "__main__":
    # If the user forgot to provide a filename, show them how to use it
    if len(sys.argv) < 2:
        print("Usage: python auditor.py <your_sql_file.sql>")
    else:
        # Start the auditor with the filename provided
        app = SQLAuditor(sys.argv[1])