import sqlite3

conn = sqlite3.connect("data/fda_adverse_events.db")

cursor = conn.execute("SELECT COUNT(*) FROM reports")
for row in cursor:
    print(row)

cursor = conn.execute("SELECT COUNT(*) FROM drugs")
for row in cursor:
    print(row)

cursor = conn.execute("SELECT COUNT(*) FROM reactions")
for row in cursor:
    print(row)

cursor = conn.execute("SELECT safetyreportid, reaction_count, drug_count " \
"FROM reports " \
"LIMIT 5")
for row in cursor:
    print(row)

conn.close()