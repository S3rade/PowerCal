#!/usr/bin/env python3

#all the imports
import os 
from flask import Flask, request ,redirect
from flask_mysqldb import MySQL
import random
from datetime import datetime 
import pyotp
from flask import *
from flask_bootstrap import Bootstrap
import json



app = Flask(__name__)

#Database(DB) Credentials 
app.config['MYSQL_USER'] = "cost"
app.config['MYSQL_PASSWORD'] = "CostGroupA"
app.config['MYSQL_DB'] = "cost"
app.config['MYSQL_TABLE'] = "sensors"
app.config['MYSQL_HOST'] = "127.0.0.1"
app.config['SECRET_KEY'] = "APP_SECRET_KEY"

#init programme 
mysql = MySQL(app)
bootstrap= Bootstrap(app)

#checking if the db is connected
@app.route('/init')
def init():
    #Connecting to DB
    cur = mysql.connection.cursor()

    conn = mysql.connection()

    #Prepared Statement
    cur.execute('SELECT * FROM sensors')

    #Executing the query and assiging the variable.
    db_test = cur.fetchall()

    #Close DB connection
    cur.close()

    #If data is returned, rediret.
    if db_test != None:
        return redirect("/login/")
    else:
        return ("MYSQL is not running")

# login page route
@app.route("/login/")
def login():
    return render_template("login.html")


# login form route
@app.route("/login/", methods=["POST"])
def login_form():
    # demo creds
    creds = {"username": "admin", "password": "password"}

    # getting form data
    username = request.form.get("username")
    password = request.form.get("password")
    #token = auth.get_token(username, password)
    #session['auth_token'] = token


    # authenticating submitted creds with demo creds
    # redirecting users to 2FA page when creds are valid
    if username == creds["username"] and password == creds["password"]:
        session['logined'] = True
        return redirect(url_for("login_2fa"))
    else:
        # inform users if creds are invalid
        flash("You have supplied invalid login credentials!", "danger")
        return redirect(url_for("login"))


# 2FA page route
@app.route("/login/2fa/")
def login_2fa():
    if session.get('logined') == True:
            print("Access Granted")
    else:
        return redirect(url_for('login'))
    # generating random secret key for authentication
    #secret = pyotp.random_base32()
    secret = "QAAGLKQZH5ACKGNX"
    return render_template("login_2fa.html", secret=secret)


# 2FA form route
@app.route("/login/2fa/", methods=["POST"])
def login_2fa_form():
   
    # getting secret key used by user
    secret = request.form.get("secret")
    # getting OTP provided by user
    otp = int(request.form.get("otp"))

    # verifying submitted OTP with PyOTP
    if pyotp.TOTP(secret).verify(otp):
        # inform users if OTP is valid
        flash("The TOTP 2FA token is valid", "success")
        session['authenticated'] = True  
        request.endpoint
        return redirect("/db")
    else:
        # inform users if OTP is invalid
        flash("You have supplied an invalid 2FA token!", "danger")
        return redirect(url_for("login_2fa"))

@app.route('/logout')
def logout():
    session.pop('logined', None)
    session.pop('authenticated', None)
    return redirect(url_for('login'))
# Add Function
@app.route("/db/add/", methods=["GET","PUT"] )
@app.route("/db/add/<appliance_name>", methods=["GET","PUT"] )
def add(appliance_name=None):
    StatusStr = request.args.get('Status')
    if StatusStr == None or appliance_name == None:
        return "Not Valid"
    try:
        cur = mysql.connection.cursor()
        query="insert into sensors(Appliance_Name,Status) values ('" + json.dumps(appliance_name) + "','" + json.dumps(StatusStr) + "');"
        print(query)
        cur.execute(query)
        mysql.connection.commit()

    except Exception as e:
        print("Problem inserting into db: " + str(e))
        return "FAIL"
    cur.close()
    return "OK"
    
#Update Function
@app.route("/db/update/", methods=["GET","PUT"] )
@app.route("/db/update/<device_id>", methods=["GET","PUT"] )
def update(device_id=None):
    StatusStr = request.args.get('Status')
    if StatusStr == None or device_id == None:
        return "Not valid"
   
    try:
        cur = mysql.connection.cursor()
        query="update sensors set Status = '" + json.dumps(StatusStr) + "' where ID = '" + json.dumps(device_id) + "';"
        print(query)
        cur.execute(query)
        mysql.connection.commit()
        
    except:
        return "FAIL"
    cur.close()
    return "OK"

 
 
#Database Page
@app.route('/db', methods=["GET","PUT"] )
def default():
    if session.get('authenticated') == True:
    	#Same as Init
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM sensors')
        results = cur.fetchall()
        cur.close()
        print("Access Granted")
    else:
        return redirect(url_for('login'))
    
    

    #Generation of Table
    if results != None :
        #Table Headers
        completeTable="<tr >"
        completeTable += "<th> No. </th>"
        completeTable += "<th> Name </th>"
        completeTable += "<th> Status </th>"
        completeTable += "<th> Up Time (Min) </th>"
        completeTable += "<th> Total Cost ($) </th>"
        completeTable+="</tr>"
        #Printing Results from the query.
        for c in results:
            completeTable+="<tr >"
            #Retreiving the first Variable from DB Query
            completeTable += "<th>" + str(c[0]) + "</th>"

            #Retreiving the second Variable from DB Query
            completeTable += "<th>" + str(c[1]) + "</th>"

            #Retreiving the third Variable from DB Query and check for Boolean, '1' means ON and '0' means OFF
            hi = str(c[2])
            
            if str(c[2]) == '1': #Check if its a '1' or '0'
                
            
                completeTable += "<th> ON </th>"
                #Takes the Fourth Variable from the DB Query and Call Time Diff
                start_time = c[3]

                #Calculation of time difference & Printing it into the table.
                current_time = datetime.now()
                difference = (current_time - start_time)
                difference_in_s = difference.total_seconds()
                minutes = divmod(difference_in_s, 60)[0]
                completeTable += "<th>" + str(minutes) + "</th>" 
                
                #Calculation of Cost & Printing it into the table.
                total_cost = (difference_in_s * 0.6)
                completeTable += "<th>" + str(total_cost) + "</th>"                            

            else:
                completeTable += "<th> OFF </th>"
                completeTable += "<th> 0</th>"
                completeTable += "<th> 00.00 </th>"
                completeTable+="</tr>"

        #Priting the Table Generated above to a HTML File
        return """
        <!DOCTYPE html>
        <title>Sensify</title>
        <html>
        
        <style>
        .w3-top {
        	 background-color: #EBEBEB;
        }
        
        .bg {
            height:1080px;
            width:1900px;
        }
        
        </style>
        
        <head>
	<link rel="stylesheet" href="{{ url_for('static', filename='css/w3css.css') }}">
	<link rel="stylesheet" href="{{ url_for('static', filename='css/googleapi.css') }}">
	<link rel="stylesheet" href="{{ url_for('static', filename='css/font-awesome.css') }}">
	</head>
	
        <body>        
        <div class="w3-top">
	  <div class="w3-bar w3-white w3-card" id="myNavbar">
	    <a href="/" class="w3-bar-item w3-button w3-wide">Sensify</a>
	     <a href="/about" class="w3-bar-item w3-button">About</a>
	     <a href="/info" class="w3-bar-item w3-button">Code Info</a>
	     <a href="/logout" class="w3-bar-item w3-button">Logout</a>
	  </div>
	</div>
	
	<hr>
    <div class="bg" style="background-image:url('static/background.jpg');>    
        <div class="title1"> 
        Welcome to Sensify!
        <br>
        
        For more information about the team, visit the About page <br> or <br> If you'd like to learn about how we did this, visit the Code info page.
                   
        <h1>Data</h1>
            <table border=\"1\">
            %s
            </table>
        <br>
   
        Take advantage of our application to find out how much money your appliance is costing you! This'll help you when planning out your budget and help you save your money.
   </div>
        <br>
        <hr>
    </div>
        
        <footer>
        Follow our social media for more information on our upcoming projects!
        </footer>
        
        </body>
        </html>
        """ %(completeTable)
    else:
        return(" MYSQL is not running or NO Data in Table")

#Running the programme on localhost
if __name__ == "__main__":
    host = os.getenv("IP", "0.0.0.0")
    port = int(os.getenv("PORT", 8080))
    app.run(host=host, port=port, debug=False, use_reloader=True, use_evalex=False)
