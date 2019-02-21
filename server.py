from flask import Flask, render_template, request
import json
import os
import ibm_db
#from geopy.distance import great_circle
from datetime import datetime
from dateutil import tz

app = Flask(__name__)
# Get service information if on IBM Cloud Platform
if 'VCAP_SERVICES' in os.environ:
    db2info = json.loads(os.environ['VCAP_SERVICES'])['dashDB For Transactions'][0]
    db2cred = db2info["credentials"]
    appenv = json.loads(os.environ['VCAP_APPLICATION'])
else:
    # raise ValueError('Expected cloud environment')
    with open('new.json') as new_file:
        jd_vcap_new_file = json.load(new_file)
        db2info = jd_vcap_new_file['dashDB For Transactions'][0]
        db2cred = db2info["credentials"]

# Time zone conversion
def getLocalTime(rows):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/Chicago')

    for i in rows:
        utc = datetime.strptime(i['time'], '%Y-%m-%d %H:%M:%S')
        utc = utc.replace(tzinfo=from_zone)
        central = utc.astimezone(to_zone)
        i['time'] = central
    return rows


@app.route('/displayDB', methods=['GET', 'POST'])

def displayDB():
    try:
        db2conn = ibm_db.connect("DATABASE=" + db2cred['db'] + ";HOSTNAME=" + db2cred['hostname'] + ";PORT=" + str(
            db2cred['port']) + ";UID=" + db2cred['username'] + ";PWD=" + db2cred['password'] + ";", "", "")
        sql = "Select * from earth"
        stmt = ibm_db.prepare(db2conn, sql)
        ibm_db.execute(stmt)
        result = ibm_db.fetch_assoc(stmt)
        row = []

        while result != False:
           # print sql
            row.append(result.copy())
            result = ibm_db.fetch_assoc(stmt)
        ibm_db.close(db2conn)
        #row = getLocalTime(row)
        return render_template("displayDB.html", row=row)
    except:
        print "Exception Occured in Display Method"
        return render_template("home.html")


@app.route('/search',methods=['GET', 'POST'])
def search():
    try:
        db2conn = ibm_db.connect("DATABASE=" + db2cred['db'] + ";HOSTNAME=" + db2cred['hostname'] + ";PORT=" + str(
            db2cred['port']) + ";UID=" + db2cred['username'] + ";PWD=" + db2cred['password'] + ";", "", "")

        room = request.form['uname']

        sql = "Select * from earth WHERE \"mag\" = ?"
        print room
        stmt = ibm_db.prepare(db2conn, sql)
        ibm_db.bind_param(stmt,1,room)
        ibm_db.execute(stmt)
        result = ibm_db.fetch_assoc(stmt)
        row = []
        while result != False:
            row.append(result.copy())
            result = ibm_db.fetch_assoc(stmt)
        ibm_db.close(db2conn)
        return render_template("search.html", row=row)

    except:
        print "Exception Occured in Display Method"
        return render_template("home.html")

@app.route('/searchcount',methods=['GET', 'POST'])

def searchcount():
    try:
        db2conn = ibm_db.connect("DATABASE=" + db2cred['db'] + ";HOSTNAME=" + db2cred['hostname'] + ";PORT=" + str(
            db2cred['port']) + ";UID=" + db2cred['username'] + ";PWD=" + db2cred['password'] + ";", "", "")

        room = request.form['uname']

        sql = "Select count(*) from earth WHERE \"mag\" > ?"
        print room
        stmt = ibm_db.prepare(db2conn, sql)
        ibm_db.bind_param(stmt,1,room)
        ibm_db.execute(stmt)
        result = ibm_db.fetch_assoc(stmt)
        row = []
        while result != False:
            row.append(result.copy())
            result = ibm_db.fetch_assoc(stmt)
        ibm_db.close(db2conn)
        return render_template("searchcount.html", row=row)

    except:
        print "Exception Occured in Display Method"
        return render_template("home.html")

@app.route('/searchinrange',methods=['GET', 'POST'])

def searchinrange():
    try:
        db2conn = ibm_db.connect("DATABASE=" + db2cred['db'] + ";HOSTNAME=" + db2cred['hostname'] + ";PORT=" + str(
            db2cred['port']) + ";UID=" + db2cred['username'] + ";PWD=" + db2cred['password'] + ";", "", "")

        magnitude1 = request.form['magnitude1']
        magnitude2 = request.form['magnitude2']
        timeDate1 = request.form['date1']
        timeDate2 = request.form['date2']

        print magnitude1
        print magnitude2
        print timeDate1
        print timeDate2

        sql = "Select * from earth WHERE \"mag\" between ? AND ? AND \"time\" between ? AND ?"

        stmt = ibm_db.prepare(db2conn, sql)
        ibm_db.bind_param(stmt,1,magnitude1)
        ibm_db.bind_param(stmt, 2, magnitude2)
        ibm_db.bind_param(stmt, 3, timeDate1)
        ibm_db.bind_param(stmt, 4, timeDate2)
        ibm_db.execute(stmt)
        result = ibm_db.fetch_assoc(stmt)
        row = []
        while result != False:
            row.append(result.copy())
            result = ibm_db.fetch_assoc(stmt)
        ibm_db.close(db2conn)
        return render_template("searchinrange.html", row=row)

    except:
        print "Exception Occured in Display Method"
        return render_template("home.html")


@app.route('/searchinradius',methods=['GET', 'POST'])

def searchinradius():
    try:
        db2conn = ibm_db.connect("DATABASE=" + db2cred['db'] + ";HOSTNAME=" + db2cred['hostname'] + ";PORT=" + str(
            db2cred['port']) + ";UID=" + db2cred['username'] + ";PWD=" + db2cred['password'] + ";", "", "")

        latitude = (request.form['latitude'])
        longitude =(request.form['longitude'])
        radius = (request.form['radius'])

        #sql = "select * from earth"
        sql ="select * from (select *,(((acos(sin(("+latitude+"*3.14/180))* sin ((\"latitude\"*3.14/180))+cos(("+latitude+\
             "*3.14/180))*cos((\"latitude\"*3.14/180))*COS((("+longitude+" - \"longitude\")*3.14/180))))*180/3.14)*60*1.1515*1.609344) " \
                                                                         "as distance From earth) where distance <= "+radius+""

        stmt = ibm_db.prepare(db2conn, sql)
        ibm_db.execute(stmt)
        result = ibm_db.fetch_assoc(stmt)
        row = []
        while result != False:
            row.append(result.copy())
            result = ibm_db.fetch_assoc(stmt)
        ibm_db.close(db2conn)
        return render_template("searchinradius.html", row=row)

    except:
        print "Exception Occured in Display Method"
        return render_template("home.html")

@app.route('/searchinmagintudeclusters',methods=['GET', 'POST'])

def searchinmagintudeclusters():
    try:
        db2conn = ibm_db.connect("DATABASE=" + db2cred['db'] + ";HOSTNAME=" + db2cred['hostname'] + ";PORT=" + str(
            db2cred['port']) + ";UID=" + db2cred['username'] + ";PWD=" + db2cred['password'] + ";", "", "")

        mag = request.form['mag']

        mag2 = mag+".99"
        print mag2

        sql = "select * from earth where (\"mag\" between ? and ?)"
        stmt = ibm_db.prepare(db2conn, sql)
        ibm_db.bind_param(stmt,1,mag)
        ibm_db.bind_param(stmt, 2, mag2)
        ibm_db.execute(stmt)
        result = ibm_db.fetch_assoc(stmt)
        row = []
        while result != False:
            row.append(result.copy())
            result = ibm_db.fetch_assoc(stmt)
        ibm_db.close(db2conn)
        return render_template("searchinmagintudeclusters.html", row=row)

    except:
        print "Exception Occured in Display Method"
        return render_template("home.html")

@app.route('/midnight', methods=['GET', 'POST'])

def midnight():
    try:
        db2conn = ibm_db.connect("DATABASE=" + db2cred['db'] + ";HOSTNAME=" + db2cred['hostname'] + ";PORT=" + str(
            db2cred['port']) + ";UID=" + db2cred['username'] + ";PWD=" + db2cred['password'] + ";", "", "")

        # Night time
        sql = "select count(*) from earth where \"mag\" > 5.0 and (EXTRACT(hour FROM \"time\") >= 18 OR EXTRACT(hour FROM \"time\") <= 6)"
        stmt = ibm_db.prepare(db2conn, sql)
        ibm_db.execute(stmt)
        result = ibm_db.fetch_assoc(stmt)
        row = []

        while result != False:
            row.append(result.copy())
            result = ibm_db.fetch_assoc(stmt)

        # Day time
        sql = "select count(*) from earth where \"mag\" > 5.0 and (EXTRACT(hour FROM \"time\") >= 7 OR EXTRACT(hour FROM \"time\") <= 17)"
        stmt = ibm_db.prepare(db2conn, sql)
        ibm_db.execute(stmt)
        result = ibm_db.fetch_assoc(stmt)
        while result != False:
            row.append(result.copy())
            result = ibm_db.fetch_assoc(stmt)

        ibm_db.close(db2conn)

        return render_template("midnight.html", row=row)
    except:
        print "Exception Occured in Display Method"
        return render_template("home.html")

@app.route('/')
def index():

    return render_template('home.html')


port = os.getenv('PORT', '10000')
if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=int(port))
    app.run(host='0.0.0.0', port=int(port))