import sqlite3
import sys
import time
from datetime import datetime
from hashlib import md5
import argparse

from ChangeCapture import ChangeCapture

DB_NAME = "db.nfl_data"
STG_FILE = "nfl_passing.csv"

def create_tables():
    db_con = sqlite3.connect(DB_NAME)
    db_con.execute("DROP TABLE IF EXISTS nfl_passing_delta")
    db_con.execute("""
       CREATE TABLE IF NOT EXISTS nfl_passing_delta (PLAYER TEXT,
       TEAM TEXT,
       ATT INT,
       COMP INT,
       COMP_PERCENT FLOAT,
       YDS INT,
       YPA FLOAT,
       TD INT,
       TD_PERCENT FLOAT,
       INTERCEPT INT,
       INTERCEPT_PERCENT FLOAT,
       LNG_YDS TXT,
       SACK INT,
       LOSS INT,
       RATE FLOAT,
       CHKSUM TEXT,
       BATCHACTION TEXT,
       BATCHRUNID INT,
       CREATED_DTTM DATETIME DEFAULT CURRENT_TIMESTAMP)"""
    )
    db_con.execute("DROP TABLE IF EXISTS nfl_passing")
    db_con.execute("""
       CREATE TABLE IF NOT EXISTS nfl_passing (PLAYER TEXT,
       TEAM TEXT,
       ATT INT,
       COMP INT,
       COMP_PERCENT FLOAT,
       YDS INT,
       YPA FLOAT,
       TD INT,
       TD_PERCENT FLOAT,
       INTERCEPT INT,
       INTERCEPT_PERCENT FLOAT,
       LNG_YDS TXT,
       SACK INT,
       LOSS INT,
       RATE FLOAT,
       CHKSUM TEXT,
       BATCHACTION TEXT,
       BATCHRUNID INT,
       CREATED_DTTM DATETIME DEFAULT CURRENT_TIMESTAMP)"""
    )
    db_con.close()

def get_old_dataset():
    old_dataset = {}
    db_con = sqlite3.connect(DB_NAME)
    db_cur = db_con.cursor()
    db_cur.execute("SELECT * FROM nfl_passing")
    data_response = db_cur.fetchall()
    for row in data_response:
        key = row[0]
        player = row[0]
        team = row[1]
        att = row[2]
        comp = row[3]
        comp_percent = row[4]
        yds = row[5]
        ypa = row[6]
        td = row[7]
        td_percent = row[8]
        intercept = row[9]
        intercept_percent = row[10]
        lng_yds = row[11]
        sack = row[12]
        loss = row[13]
        rate = row[14]
        chksum = row[15]
        old_dataset.update({key:
                            {
                                "Player": player,
                                "Team": team,
                                "Att": att,
                                "Comp": comp,
                                "Comp_percent": comp_percent,
                                "yds":yds,
                                "ypa": ypa,
                                "td": td,
                                "td_percent": td_percent,
                                "intercept": intercept,
                                "intercept_percent": intercept_percent,
                                "lng_yds": lng_yds,
                                "sack": sack,
                                "loss": loss,
                                "rate": rate,
                                "chksum": chksum
                            }})
    return old_dataset

def parse_line(keyCol, line, sep):
    split_line = line.split(",")
    if len(split_line) < 15:
        return {}
    
    key = split_line[keyCol]
    player = split_line[0]
    team = split_line[1]
    att = split_line[2]
    comp = split_line[3]
    comp_percent = split_line[4]
    yds = split_line[5]
    ypa = split_line[6]
    td = split_line[7]
    td_percent = split_line[8]
    intercept = split_line[9]
    intercept_percent = split_line[10]
    lng_yds = split_line[11]
    sack = split_line[12]
    loss = split_line[13]
    rate = split_line[14]
    chksum = md5(line.encode()).hexdigest()

    return key, {
        key:
        {
            "Player": player,
            "Team": team,
            "Att": att,
            "Comp": comp,
            "Comp_percent": comp_percent,
            "yds":yds,
            "ypa": ypa,
            "td": td,
            "td_percent": td_percent,
            "intercept": intercept,
            "intercept_percent": intercept_percent,
            "lng_yds": lng_yds,
            "sack": sack,
            "loss": loss,
            "rate": rate,
            "chksum": chksum
        }
    }
    
def insert_delta_records(batchDelta, batchRunId):
    db_con = sqlite3.connect(DB_NAME)
    db_cur = db_con.cursor()
    created_dttm = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    for data in batchDelta.values():
        row_data = list(data.values())
        args = row_data + [batchRunId, created_dttm]
        db_cur.execute("INSERT INTO nfl_passing_delta VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", args)
        db_con.commit()
    db_con.close()

def apply_delta_position(batchDelta, batchRunId):
    db_con = sqlite3.connect(DB_NAME)
    db_cur = db_con.cursor()
    created_dttm = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    for key, data in batchDelta.items():
        dbKey = key
        dbAction = data['batchaction']
        row_data = list(data.values())
        if dbAction == "Insert":
            args = row_data + [batchRunId, created_dttm]
            db_cur.execute("INSERT INTO nfl_passing VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", args)
        elif dbAction == "Update":
            args = row_data + [batchRunId, created_dttm, dbKey]
            db_cur.execute("""
                            UPDATE nfl_passing 
                            SET PLAYER=?,
                                TEAM=?,
                                ATT=?,
                                COMP=?,
                                COMP_PERCENT=?,
                                YDS=?,
                                YPA=?,
                                TD=?,
                                TD_PERCENT=?,
                                INTERCEPT=?,
                                INTERCEPT_PERCENT=?,
                                LNG_YDS=?,
                                SACK=?,
                                LOSS=?,
                                RATE=?,
                                CHKSUM=?,
                                BATCHACTION=?,
                                BATCHRUNID=?,
                                CREATED_DTTM=?
                            WHERE player = ?""", args)
        elif dbAction == "Delete":
            args = [dbKey]
            db_cur.execute("DELETE FROM nfl_passing WHERE player = ?", args)
        elif dbAction == "Copy":
            pass
        db_con.commit()
    db_con.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Staging job using ChangeCapture class to calculate batch of data")
    parser.add_argument("--batchrunid", required=True, type=int, help="This is the number representing this batch of data")
    args = parser.parse_args()
    batchDelta = {}
    batchRunId = args.batchrunid
    
    #create_tables()
    old_dataset = get_old_dataset()
    stg_cc = ChangeCapture(old_dataset, "Player", "chksum")
    try:
        nfl_file = open(STG_FILE, 'r')
        file_header = nfl_file.readline()
        for nfl_line in nfl_file:
            nfl_line = nfl_line.strip()
            keyCol, nfl_parsed = parse_line(0, nfl_line, ',')

            if len(nfl_parsed) > 0:
                row_batchaction = stg_cc.check_row_change(nfl_parsed)
                if row_batchaction != 'Copy':
                    nfl_parsed[keyCol]['batchaction'] = row_batchaction
                    batchDelta.update(nfl_parsed)
        
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
    finally:
        nfl_file.close()

    batchDelta.update(stg_cc.get_deletes())
    insert_delta_records(batchDelta, batchRunId)
    apply_delta_position(batchDelta, batchRunId)
