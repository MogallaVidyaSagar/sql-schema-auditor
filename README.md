# Automated SQL Schema Auditor

A Python-based tool designed to analyze SQL schema files for database normalization errors and best practices. This project helps developers catch common mistakes before they reach production.

## 🚀 Key Features (In Progress)
- **Primary Key Detection:** Identifies tables missing mandatory primary keys.
- **Regex-based Parsing:** Scans SQL files without needing a live database connection.
- **Static Analysis:** Provides instant feedback on schema quality.

## 🛠️ How to Run
Ensure you have Python installed, then run:
```bash
python auditor.py <your_file>.sql