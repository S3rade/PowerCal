#all the imports
import os 
from flask import Flask, request ,redirect
from flask_mysqldb import MySQL
import random
from datetime import datetime 


app = Flask(__name__)

#Database(DB) Credentials 
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "cost"
app.config['MYSQL_HOST'] = "127.0.0.1"

#init programme 
mysql = MySQL(app)

#checking if the db is connected
@app.route('/init')
def init():
    #Connecting to DB
    cur = mysql.connection.cursor()

    #Prepared Statement
    cur.execute('SELECT * FROM sensors')

    #Executing the query and assiging the variable.
    db_test = cur.fetchall()

    #Close DB connection
    cur.close()

    #If data is returned, rediret.
    if db_test != None:
        return redirect("/")
    else:
        return ("MYSQL is not running")
    
#Index Page
@app.route('/', methods=["GET","PUT"] )
def default():
    #Same as Init
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM sensors')
    results = cur.fetchall()
    cur.close()

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
            if bool(random.getrandbits(1)): #Check if its a '1' or '0'
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
        <title>COST GROUP A</title>
        <html>
        <body>
            <h1>Sensors Data</h1>
            <table border=\"1\">
            %s
            </table>
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
