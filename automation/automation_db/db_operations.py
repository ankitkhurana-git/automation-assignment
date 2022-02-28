import sqlite3
from flask import render_template, make_response


def insert_device_record(interface_name, request_method, netconf_operation, response):
    """
     This function insert device interaction data to Record table.
    :param interface_name:
    :param request_method:
    :param netconf_operation:
    :param response:
    """
    con = sqlite3.connect("device.db")
    cur = con.cursor()

    cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Record' ''')
    if cur.fetchone()[0] == 1:
        print("Table already created")
    else:
        con.execute(
            "create table Record (id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "interface_name  TEXT NOT NULL, request_method TEXT NOT NULL,"
            "netconf_operation TEXT NOT NULL, response TEXT NOT NULL)")
        print("Table created Successfully")

    cur = con.cursor()
    cur.execute(
        "INSERT into Record (interface_name, request_method, netconf_operation, response) values (?,?,?,?)",
        (interface_name, request_method, netconf_operation, response))
    con.commit()


def show_device_record():
    """
    This function returns Device SQL data in HTML format.
    :return: HTML Data Output
    """
    con = sqlite3.connect("device.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Record")
    rows = cur.fetchall()
    headers = {'Content-Type': 'text/html'}
    return make_response(render_template('record.html', rows=rows), 200, headers)
