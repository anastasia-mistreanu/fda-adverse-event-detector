import sqlite3

def main():
    conn = sqlite3.connect("data/fda_adverse_events.db")
    add_reaction_count(conn)
    add_drug_count(conn)
    add_age_in_years(conn)
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

def add_age_in_years(conn):
    #add a new column holding age converted to a consistent unit (years)
    #raw patientonsetage mixes multiple units (decades, years, months, etc)
    try:
        conn.execute("ALTER TABLE reports " \
        "ADD COLUMN patientonsetage_years REAL")
    except sqlite3.OperationalError:
            print("Error adding patientonsetage_years column.")

    conn.execute("UPDATE reports SET patientonsetage_years = CASE " \
    "WHEN patientonsetageunit = '800' THEN patientonsetage * 10 " \
    "WHEN patientonsetageunit = '801' THEN patientonsetage " \
    "WHEN patientonsetageunit = '802' THEN patientonsetage / 12 " \
    "WHEN patientonsetageunit = '803' THEN patientonsetage / 52 " \
    "WHEN patientonsetageunit = '804' THEN patientonsetage / 365 " \
    "WHEN patientonsetageunit = '805' THEN patientonsetage / (24*365) " \
    "ELSE NULL " \
    "END")

    conn.commit()

if __name__ == "__main__":
    main()