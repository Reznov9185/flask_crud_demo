from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sys
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)
app.secret_key = b'U\xfcnD\xf0jNK\x06\xa4\x1d\xb0[7\x8c\x04'

def db_connect():
    cnx = None
    try:
        cnx = mysql.connector.connect(
                                    host=session.get("hostname"),
                                    user=session.get("username"),
                                    password=session.get("password"),
                                    database=session.get("dbname"))                    
    except mysql.connector.Error as err:
        error_msg = "Something went wrong: {}".format(err)
        print(error_msg)
    return cnx

@app.route("/")
def index():
    cnx = db_connect()
    if not (cnx is None) and cnx.is_connected():
        return redirect(url_for("home"))
    return render_template("index.html")

@app.route("/", methods=["POST"])
def login():
    try:
        cnx = mysql.connector.connect(
                                    host=request.form["hostname"],
                                    user=request.form["username"],
                                    password=request.form["password"],
                                    database=request.form["dbname"])
        print(cnx)
        if cnx.is_connected():
            session["hostname"] = request.form["hostname"]
            session["username"] = request.form["username"]
            session["password"] = request.form["password"]
            session["dbname"] = request.form["dbname"]
            return redirect(url_for("home"))
        error_msg = "Something went wrong: {}".format("not connected to the database!")
        return render_template("index.html", msg= "")
    except mysql.connector.Error as err:
        error_msg = "Something went wrong: {}".format(err)
        return render_template("index.html", msg= error_msg)

@app.route("/home")
def home():
    cnx = db_connect()
    if not (cnx is None) and cnx.is_connected():
        cursor = cnx.cursor(buffered=True)
        query = ("select * from DigitalDisplay")
        cursor.execute(query)
        res = cursor.fetchall()
        return render_template("home.html", digital_displays = res)
    error_msg = "Something went wrong: {}".format("got disconnected!")
    return render_template("index.html", msg= "")

@app.route("/model/<modelNo>")
def model_index(modelNo):
    cnx = db_connect()
    if not (cnx is None) and cnx.is_connected():
        cursor = cnx.cursor(buffered=True)
        query = ("select * from Model where modelNo = %s")
        vals = (modelNo, )
        cursor.execute(query, vals)
        res = cursor.fetchall()
        return render_template("model.html", model_detail = res)
    error_msg = "Something went wrong: {}".format("got disconnected!")
    return render_template("index.html", msg= "")

@app.route("/search-displays")
def search_displays():
    return render_template("search_displays.html")

@app.route("/search-displays", methods=["POST"])
def search_result():
    cnx = db_connect()
    if not (cnx is None) and cnx.is_connected():
        cursor = cnx.cursor(buffered=True)
        query = ("select * from DigitalDisplay where schedulerSystem like %s;")
        vals = ("%" + request.form["schedulerSystem"] + "%",)
        cursor.execute(query, vals)
        res = cursor.fetchall()
        return render_template("found_displays.html", digital_displays = res)
    error_msg = "Something went wrong: {}".format("got disconnected!")
    return render_template("index.html", msg= "")

@app.route("/logout", methods=["POST"])
def logout():
    cnx = db_connect()
    if not (cnx is None) and cnx.is_connected():
        session.clear()
        return render_template("index.html", msg= "Successfully logged out.")
