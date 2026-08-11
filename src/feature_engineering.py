import sqlite3

def main():
    conn = sqlite3.connect("data/fda_adverse_events.db")
    add_reaction_count(conn)
    add_drug_count(conn)
    conn.close()


def add_reaction_count(conn):
    #add reaction_count column to reports table
    try:
        conn.execute("ALTER TABLE reports " \
        "ADD COLUMN reaction_count INTEGER")

    except sqlite3.OperationalError:
        print("Error adding reaction_count column.")

    #count matching rows existing in rxns and reports tables and store count in new column
    conn.execute("UPDATE reports " \
    "SET reaction_count = (" \
    "SELECT COUNT(*) FROM reactions " \
    "WHERE reactions.safetyreportid = reports.safetyreportid)"
    )
    conn.commit() 


def add_drug_count(conn):
    #add drug_count column to reports table
    try:
        conn.execute("ALTER TABLE reports " \
        "ADD COLUMN drug_count INTEGER")
    except sqlite3.OperationalError:
        print("Error adding drug_count column.")

    #count matching rows existing in reports and drugs tables and store count in new column
    conn.execute("UPDATE reports " \
    "SET drug_count = (" \
    "SELECT COUNT(*) FROM drugs " \
    "WHERE drugs.safetyreportid = reports.safetyreportid)"
    )
    conn.commit()



if __name__ == "__main__":
    main()