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
                                    host = session.get("hostname"),
                                    user = session.get("username"),
                                    password = session.get("password"),
                                    database = session.get("dbname"))                    
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

@app.route("/", methods = ["POST"])
def login():
    try:
        cnx = mysql.connector.connect(
                                    host = request.form["hostname"],
                                    user = request.form["username"],
                                    password = request.form["password"],
                                    database = request.form["dbname"])
        if cnx.is_connected():
            session["hostname"] = request.form["hostname"]
            session["username"] = request.form["username"]
            session["password"] = request.form["password"]
            session["dbname"] = request.form["dbname"]
            return redirect(url_for("home"))
        error_msg = "Something went wrong: {}".format("not connected to the database!")
        return render_template("index.html", success_msg = "")
    except mysql.connector.Error as err:
        error_msg = "Something went wrong: {}".format(err)
        return render_template("index.html", error_msg = error_msg)

@app.route("/home")
def home():
    cnx = db_connect()
    if not (cnx is None) and cnx.is_connected():
        cursor = cnx.cursor(buffered = True)
        query = ("select * from DigitalDisplay")
        cursor.execute(query)
        res = cursor.fetchall()
        if not (request.args.get("success_msg") is None):
            return render_template("home.html", digital_displays = res, 
                success_msg = request.args.get("success_msg"))
        else:
            return render_template("home.html", digital_displays = res)
    error_msg = "Something went wrong: {}".format("got disconnected!")
    return render_template("index.html", error_msg = error_msg)

@app.route("/displays-models")
def displays_and_models():
    cnx = db_connect()
    if not (cnx is None) and cnx.is_connected():
        cursor = cnx.cursor(buffered = True)
        all_digital_displays = ("select * from DigitalDisplay")
        cursor.execute(all_digital_displays)
        digital_displays = cursor.fetchall()
        all_models = ("select * from Model")
        cursor.execute(all_models)
        models = cursor.fetchall()
        if not (request.args.get("success_msg") is None):
            return render_template("home.html", digital_displays = digital_displays, models = models, 
                success_msg= request.args.get("success_msg"))
        else:
            return render_template("home.html", digital_displays = digital_displays, models = models)
    error_msg = "Something went wrong: {}".format("got disconnected!")
    return render_template("index.html", error_msg = error_msg)

@app.route("/create-display")
def create_display():
    cnx = db_connect()
    if not (cnx is None) and cnx.is_connected():
        return render_template("create_display.html")
    return redirect(url_for("home"))

@app.route("/save-display", methods = ["POST"])
def save_display():
    try:
        cnx = db_connect()
        if not (cnx is None) and cnx.is_connected():
            cursor = cnx.cursor(buffered = True)
            find_model_query = ("select count(*) from Model where modelNo = %s;")
            modelNoVal = (request.form["modelNo"], )
            cursor.execute(find_model_query, modelNoVal)
            resModelNoCount = cursor.fetchall()
            if int(list(resModelNoCount)[0][0]) == 0:
                return render_template("create_display.html", 
                    error_msg = "Model Doesn't Exist! Please create a Model first.")
            query = ("INSERT INTO DigitalDisplay (serialNo, schedulerSystem, modelNo) VALUES (%s, %s, %s);")
            vals = (request.form["serialNo"], request.form["schedulerSystem"], request.form["modelNo"])
            cursor.execute(query, vals)
            cnx.commit()
            return redirect(url_for("home", success_msg = "Digital Display Created Successfully!"))
    except mysql.connector.Error as err:
        error_msg = "Something went wrong: {}".format(err)
        return render_template("create_display.html", error_msg = error_msg)

@app.route("/edit-display/<serialNo>")
def edit_display(serialNo):
    try:
        cnx = db_connect()
        if not (cnx is None) and cnx.is_connected():
            cursor = cnx.cursor(buffered = True)
            find_digital_display = ("select * from DigitalDisplay where serialNo = %s;")
            serialNoVal = (serialNo, )
            cursor.execute(find_digital_display, serialNoVal)
            digital_display = cursor.fetchall()
            if not (request.args.get("error_msg") is None):
                return render_template("edit_display.html", digital_display = digital_display,
                    error_msg = request.args.get("error_msg"))
            else:
                return render_template("edit_display.html", digital_display = digital_display)
        return redirect(url_for("home"))
    except mysql.connector.Error as err:
        error_msg = "Something went wrong: {}".format(err)
        return render_template("home.html", error_msg = error_msg)

@app.route("/update-display", methods = ["POST"])
def update_display():
    try:
        cnx = db_connect()
        if not (cnx is None) and cnx.is_connected():
            cursor = cnx.cursor(buffered = True)
            find_model_query = ("select count(*) from Model where modelNo = %s;")
            modelNoVal = (request.form["modelNo"], )
            cursor.execute(find_model_query, modelNoVal)
            resModelNoCount = cursor.fetchall()
            if int(list(resModelNoCount)[0][0]) == 0:
                return redirect(url_for("edit_display", serialNo=request.form["serialNo"], 
                    error_msg = "Model Doesn't Exist! Please create a Model first."))
            query = ("update DigitalDisplay set serialNo = %s, schedulerSystem = %s, modelNo = %s where serialNo = %s;")
            vals = (request.form["serialNo"], request.form["schedulerSystem"], request.form["modelNo"], request.form["serialNo"])
            cursor.execute(query, vals)
            cnx.commit()
            return redirect(url_for("home", success_msg = "Digital Display Updated Successfully!"))
    except mysql.connector.Error as err:
        error_msg = "Something went wrong: {}".format(err)
        return render_template("create_display.html", error_msg = error_msg)

@app.route("/delete-display", methods = ["POST"])
def delete_display():
    try:
        cnx = db_connect()
        if not (cnx is None) and cnx.is_connected():
            cursor = cnx.cursor(buffered=True)
            delete_digital_display = ("delete from DigitalDisplay where serialNo = %s;")
            serialNoVal = (request.form["serialNo"], )
            cursor.execute(delete_digital_display, serialNoVal)
            cnx.commit()
            count_model_displays = ("select count(*) from DigitalDisplay where modelNo = %s;")
            modelNoVal = (request.form["modelNo"], )
            cursor.execute(count_model_displays, modelNoVal)
            resModelNoCount = cursor.fetchall()
            if int(list(resModelNoCount)[0][0]) == 0:
                delete_model_row = ("delete from Model where modelNo = %s;")
                cursor.execute(delete_model_row, modelNoVal)
                cnx.commit()
            return redirect(url_for("displays_and_models"))
    except mysql.connector.Error as err:
        error_msg = "Something went wrong: {}".format(err)
        return redirect(url_for("home", error_msg= error_msg))

@app.route("/create-model")
def create_model():
    cnx = db_connect()
    if not (cnx is None) and cnx.is_connected():
        return render_template("create_model.html")
    return redirect(url_for("home"))

@app.route("/save-model", methods = ["POST"])
def save_model():
    try:
        cnx = db_connect()
        if not (cnx is None) and cnx.is_connected():
            cursor = cnx.cursor(buffered = True)
            query = ("INSERT INTO Model (modelNo, width, height, weight, depth, screenSize) VALUES (%s, %s, %s, %s, %s, %s);")
            vals = (request.form["modelNo"], request.form["width"], request.form["height"], 
                        request.form["weight"], request.form["depth"], request.form["screenSize"])
            cursor.execute(query, vals)
            cnx.commit()
            return render_template("create_display.html", success_msg = "Model Created Successfully!")
    except mysql.connector.Error as err:
        error_msg = "Something went wrong: {}".format(err)
        print("Inside errrrrrrrrrrrrrrr!" + error_msg)
        return render_template("create_model.html", error_msg = error_msg)

@app.route("/model/<modelNo>")
def model_index(modelNo):
    cnx = db_connect()
    if not (cnx is None) and cnx.is_connected():
        cursor = cnx.cursor(buffered = True)
        query = ("select * from Model where modelNo = %s")
        vals = (modelNo, )
        cursor.execute(query, vals)
        res = cursor.fetchall()
        return render_template("model.html", model_detail = res)
    error_msg = "Something went wrong: {}".format("got disconnected!")
    return render_template("index.html", success_msg = "")

@app.route("/search-displays")
def search_displays():
    return render_template("search_displays.html")

@app.route("/search-displays", methods = ["POST"])
def search_result():
    cnx = db_connect()
    if not (cnx is None) and cnx.is_connected():
        cursor = cnx.cursor(buffered = True)
        query = ("select * from DigitalDisplay where schedulerSystem like %s;")
        vals = ("%" + request.form["schedulerSystem"] + "%",)
        cursor.execute(query, vals)
        res = cursor.fetchall()
        return render_template("home.html", digital_displays = res)
    error_msg = "Something went wrong: {}".format("got disconnected!")
    return render_template("index.html", success_msg = "")

@app.route("/logout", methods = ["POST"])
def logout():
    cnx = db_connect()
    if not (cnx is None) and cnx.is_connected():
        session.clear()
        return render_template("index.html", success_msg = "Successfully logged out.")
