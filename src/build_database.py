from fetch_data import fetch_all_drug_data
import sqlite3

def main():
    conn = sqlite3.connect("data/fda_adverse_events.db") #connect to db
    create_tables(conn) #create the 3 tables
    data = fetch_all_drug_data() #fetch data from FDA API for all 15 drugs

    seen_report_ids = set() #tracks safetyreportids to avoid duplicates

    for report in data:  #loop through fetched reports
        report_id = report.get("safetyreportid")

        if report_id in seen_report_ids:  #if report already added, skip
            pass
        else:
            seen_report_ids.add(report_id) #mark report as seen
            insert_report(conn, report)  #insert its data into respective tables

        conn.commit()
    conn.close()


def create_tables(conn):

    #create reports table
    conn.execute("CREATE TABLE IF NOT EXISTS " \
        "reports (" \
        "safetyreportid TEXT PRIMARY KEY, " \
        "serious TEXT, " \
        "seriousnessdeath TEXT, " \
        "seriousnesshospitalization TEXT, " \
        "seriousnessdisabling TEXT, " \
        "seriousnesslifethreatening TEXT, " \
        "patientonsetage REAL, " \
        "patientonsetageunit TEXT, " \
        "patientsex TEXT, " \
        "receivedate TEXT)")

    #create drugs table 
    conn.execute("CREATE TABLE IF NOT EXISTS " \
        "drugs (" \
        "id INTEGER PRIMARY KEY AUTOINCREMENT, " \
        "safetyreportid TEXT, " \
        "medicinalproduct TEXT, " \
        "drugcharacterization TEXT, " \
        "drugindication TEXT, " \
        "drugadministrationroute TEXT)")
    
    #create reactions table 
    conn.execute("CREATE TABLE IF NOT EXISTS " \
        "reactions (" \
        "id INTEGER PRIMARY KEY AUTOINCREMENT, " \
        "safetyreportid TEXT, " \
        "reactionmeddrapt TEXT)")


def insert_report(conn, report):

    #insert data into reports table
    conn.execute("INSERT INTO reports (" \
    "safetyreportid, serious, seriousnessdeath," \
    "seriousnesshospitalization, seriousnessdisabling," \
    "seriousnesslifethreatening, patientonsetage," \
    "patientonsetageunit, patientsex, receivedate) " \
    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
    (
        report.get("safetyreportid"),
        report.get("serious"),
        report.get("seriousnessdeath"),
        report.get("seriousnesshospitalization"),
        report.get("seriousnessdisabling"),
        report.get("seriousnesslifethreatening"),
        report["patient"].get("patientonsetage"),
        report["patient"].get("patientonsetageunit"),
        report["patient"].get("patientsex"),
        report.get("receivedate")
    )
)

    #insert data into drugs table
    for drug in report["patient"].get("drug", []): #return [] instead of None if None
        conn.execute("INSERT INTO drugs (" \
        "safetyreportid, medicinalproduct, drugcharacterization," \
        "drugindication, drugadministrationroute) " \
        "VALUES (?, ?, ?, ?, ?)", 
        (
            report.get("safetyreportid"),
            drug.get("medicinalproduct"),
            drug.get("drugcharacterization"),
            drug.get("drugindication"),
            drug.get("drugadministrationroute")
        )
    )

    #insert data into reactions table
    for reaction in report["patient"].get("reaction", []):
        conn.execute("INSERT INTO reactions (" \
        "safetyreportid, reactionmeddrapt) " \
        "VALUES (?, ?)", 
        (
            report.get("safetyreportid"),
            reaction.get("reactionmeddrapt")
        )
    )

if __name__ == "__main__":
    main()