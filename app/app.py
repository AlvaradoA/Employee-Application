from flask import Flask, render_template, request
from pymysql import connections
import os
import random
import argparse


app = Flask(__name__)

DBHOST = os.environ.get("DBHOST") or "localhost"
DBUSER = os.environ.get("DBUSER") or "root"
DBPWD = os.environ.get("DBPWD") or "password"
DATABASE = os.environ.get("DATABASE") or "employees"
IMAGE_FROM_ENV = os.environ.get('BG_IMG')
NAME_FROM_ENV = os.environ.get('NAMES')
DBPORT = int(os.environ.get("DBPORT"))

# Create a connection to the MySQL database
db_conn = connections.Connection(
    host= DBHOST,
    port=DBPORT,
    user= DBUSER,
    password= DBPWD, 
    db= DATABASE
    
)

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('addemp.html', image=IMAGE_FROM_ENV)

@app.route("/about", methods=['GET','POST'])
def about():
    return render_template('about.html', image=IMAGE_FROM_ENV, name=NAME_FROM_ENV)
    
@app.route("/addemp", methods=['POST'])
def AddEmp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    primary_skill = request.form['primary_skill']
    location = request.form['location']

  
    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:
        
        cursor.execute(insert_sql,(emp_id, first_name, last_name, primary_skill, location))
        db_conn.commit()
        emp_name = "" + first_name + " " + last_name

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('addempoutput.html', name=emp_name, image=IMAGE_FROM_ENV)

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    return render_template("getemp.html", image=IMAGE_FROM_ENV)


@app.route("/fetchdata", methods=['GET','POST'])
def FetchData():
    emp_id = request.form['emp_id']

    output = {}
    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location from employee where emp_id=%s"
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql,(emp_id))
        result = cursor.fetchone()
        
        # Add No Employee found form
        output["emp_id"] = result[0]
        output["first_name"] = result[1]
        output["last_name"] = result[2]
        output["primary_skills"] = result[3]
        output["location"] = result[4]
        
    except Exception as e:
        print(e)

    finally:
        cursor.close()

    return render_template("getempoutput.html", id=output["emp_id"], fname=output["first_name"],
                           lname=output["last_name"], interest=output["primary_skills"], location=output["location"], image=IMAGE_FROM_ENV)

if __name__ == '__main__':
    
    # Check if background image is in environment variables
    if IMAGE_FROM_ENV:
        print("Background image URL from environment variable =" + IMAGE_FROM_ENV)
    else:
        print("No environment variable set for background image")

    app.run(host='0.0.0.0',port=81,debug=True)
