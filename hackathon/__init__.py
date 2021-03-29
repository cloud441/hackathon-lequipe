import sys

import hackathon.DBManager.manager as db
import hackathon.DataAnalyser.analyser as analyser


''' Entry point of the project '''
def run():
    table = db.openTable("FIXME.csv")

    db.closeTable(table)


run()
