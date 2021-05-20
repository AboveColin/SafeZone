#!/usr/bin/python
import sqlite3
from sqlite3 import Error
from SafeZone.logs import logger


db_path = r"C:\Shares\School\Vakken\p3\Project\SafeZone\db\Project.db"


def create_connection(db_file):
    global conn
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file, timeout=10)
    except Error as e:
        logger.warning(e)
    finally:
        return conn


def submit_data_to_db(R_ID, T_ID, ts):
    try:
        conn = create_connection(db_path)
        sql = "INSERT INTO hits(Reader_ID, Tag_ID, ts) VALUES('{}',{},{})".format(str(R_ID), T_ID, str(ts))
        conn.execute(sql)
        conn.commit()
        conn.close()
    except Exception as e:
        logger.warning(e)


def submit_reader_to_db(R_ID,ts):
    try:
        conn = create_connection(db_path)
        sql = "INSERT INTO readers(Reader_ID, last_online) VALUES('{}',{})".format(str(R_ID), str(ts))
        conn.execute(sql)
        conn.commit()
        conn.close()
    except Exception as e:
        logger.warning(e)


def update_reader_last_seen(R_ID,ts):
    try:
        conn = create_connection(db_path)
        sql = "UPDATE readers SET last_online = '{}' WHERE Reader_ID = '{}'".format(str(ts), str(R_ID))
        conn.execute(sql)
        conn.commit()
        conn.close()
    except Exception as e:
        logger.warning(e)


def get_person_from_T_id(T_ID):
    try:
        conn = create_connection(db_path)
        cur = conn.cursor()
        cur.execute("SELECT Name FROM clients WHERE Tag = {}".format(T_ID))
        query_result = cur.fetchone()
        conn.close()
        if query_result is not None:
            return query_result
        else:
            return False
    except Exception as e:
        logger.warning(e)
        return False


def get_all_clients():
    try:
        conn = create_connection(db_path)
        cur = conn.cursor()
        cur.execute("SELECT Name, Tag, ID FROM clients")
        query_result = cur.fetchall()
        conn.close()
        return query_result
    except Exception as e:
        logger.warning(e)
        return False


def get_all_readers():
    try:
        conn = create_connection(db_path)
        cur = conn.cursor()
        cur.execute("SELECT Reader_ID, last_online FROM readers")
        query_result = cur.fetchall()
        conn.close()
        return query_result
    except Exception as e:
        logger.warning(e)
        return False

def get_last_hit(client_id):
    conn = create_connection(db_path)
    cur = conn.cursor()
    cur.execute("SELECT Tag FROM clients WHERE ID = {};".format(client_id))
    query_result = cur.fetchone()
    conn.close()
    conn = create_connection(db_path)
    cur = conn.cursor()
    cur.execute("SELECT max(ts) Time, Reader_ID FROM hits WHERE Tag_ID = {};".format(query_result[0]))
    query_result = cur.fetchone()
    conn.close()
    return [query_result[0], query_result[1]]

