from flask import Flask, render_template
import sys
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)

@app.route("/")
def db_connect():
    try:
        cnx = mysql.connector.connect(
                                    host='dbclass.cs.nmsu.edu',
                                    user='srahman',
                                    password='test_dbms1',
                                    database='test')
        cursor = cnx.cursor(buffered=True)
        return render_template("index.html")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            return "Something is wrong with your user name or password"
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            return "Database does not exist"
        else:
            return err
