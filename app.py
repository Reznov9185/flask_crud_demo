from flask import Flask, render_template, request, redirect, url_for
import sys
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def db_connect():
    with app.app_context():
        try:
            cnx = mysql.connector.connect(
                                        host=request.form["hostname"],
                                        user=request.form["username"],
                                        password=request.form["password"],
                                        database=request.form["dbname"])
            return redirect(url_for("home"))
        except mysql.connector.Error as err:
            error_msg = "Something went wrong: {}".format(err)
            return render_template("index.html", msg= error_msg)

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/logout", methods=["POST"])
def logout():
    return render_template("index.html", msg= "Dummy log out")
