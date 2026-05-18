import sqlite3
import pandas as pd
import os

# Path to the database
DB_PATH = os.path.join(os.path.dirname(__file__), "data", "td_V2.db")

print(f"Looking for database at: {DB_PATH}")
print(f"Database exists: {os.path.exists(DB_PATH)}")

conn = sqlite3.connect(DB_PATH)

query = """
SELECT
    sr.SYSTEM_TAGS,
    COUNT(*) as n_issues
FROM SONAR_ISSUES si
JOIN SONAR_RULES sr ON REPLACE(REPLACE(si.RULE, 'squid:', ''), 'findbugs:', '') = sr.PLUGIN_RULE_KEY
WHERE si.TYPE IN ('BUG', 'CODE_SMELL', 'VULNERABILITY')
GROUP BY sr.SYSTEM_TAGS
ORDER BY n_issues DESC
LIMIT 50;
"""
print("Running tag frequency query...")
df = pd.read_sql_query(query, conn)
conn.close()

print(df)
df.to_csv("tag_frequency_output.csv", index=False)
print("\nSaved to tag_frequency_output.csv")