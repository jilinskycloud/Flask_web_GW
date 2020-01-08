#!/usr/bin/python3
from flask import Flask
from flask import escape
from flask import url_for
from flask import request
from flask import render_template
#from flask import abort
from flask import redirect
from flask import session
#from flask import flash
from flask import jsonify
#from flask_mysqldb import MySQL
import psutil
import time
from _include.dbClasses import mysqldb as _mysql
import json
import sqlite3
import os
import subprocess

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
#mysql = _mysql.initMysql_(MySQL, app)


conn = sqlite3.connect('gw_FlaskDb.db')
print("Opened database successfully");
conn.close()		
'''
conn.execute('CREATE TABLE login (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)')
print("Table created successfully");
# Insert Data to Login table
conn.execute("INSERT INTO login (username,password) VALUES (?,?)",('admin', 'pass123') )
conn.commit()
msg = "Record successfully added"
'''
#rec = conn.execute("SELECT * FROM login WHERE username=? and password=?", ('admin', 'pass123'))


'''
for row in conn.execute("SELECT * FROM login WHERE username=? and password=?", ('admin', 'pass123')):
	print(row)
'''

#print(rec.fetchall())













'''
print("here is the curser....")
cur = conn.execute("SELECT * FROM students")
rows = cur.fetchall(); 
print(rows)
uname = ('admin',)
cur = conn.execute('SELECT * FROM students WHERE username=?', uname)
rows = cur.fetchone()
print("where clause")
print(type(rows))
'''
@app.route('/getcmd', methods=['GET', 'POST'])
def getcmd():
	if request.method == 'POST':
		print("yaaaaaaaaaaaaaa hooooooooooooo")
		input_json = request.get_json(force=True)
		print(input_json)
		os.system(input_json)
		print('data from client:', input_json)
	dictToReturn = {'answer':42}
	return jsonify(dictToReturn)


# ===================MYSQL FUNCTIONS==========================
@app.route('/createModel')
def createModel():
	#_mysql.createModel_(MySQL, app)
	return 'success'

@app.route('/delProfile/<ids>')
def delProfile(ids=None):
	conn = sqlite3.connect('gw_FlaskDb.db')
	f = conn.execute("DELETE FROM login where id=?", (ids))
	conn.commit()
	conn.close()
	#_mysql.delProfile_(mysql, ids)
	print("deleted..")
	return redirect(url_for('editProfile'))

#=============================================================
#=====================WEB-PAGE FUNCTIONS======================
#=============================================================

# ============================================================INDEX
@app.route('/')
@app.route('/index/')
@app.route('/index')
def index():
	if 'username' in session:
		print("logedin")
		return redirect(url_for('dashboard'))
	return redirect(url_for('login'))

# ============================================================DASHBOARD
@app.route('/dashboard')
@app.route('/dashboard/')
def dashboard():
    if 'username' in session:
        u_name = escape(session['username'])
        print(session.get('device1'))
        print("----------------------------------------------------------------")
        #while(1):
        data = {}
        data['cpu'] = psutil.cpu_percent()
        data['stats'] = psutil.cpu_stats()
        data['cpu_freq'] = psutil.cpu_freq()
        data['cpu_load'] = psutil.getloadavg()
        data['ttl_memo'] = psutil.virtual_memory()
        data['swp_memo'] = psutil.swap_memory()
        data['hostname'] =cm("hostname")
        data['routeM'] = 'TC0981'
        data['FirmV'] = 'v3.0.11_sniffer_TainCloud_r864'
        data['lTime'] = cm('date')
        data['runTime'] = cm('uptime')
        data['network'] = cm('ifconfig')
        data['mount'] = psutil.disk_partitions(all=False)
        data['disk_io_count'] = psutil.disk_io_counters(perdisk=False, nowrap=True)
        data['net_io_count'] = psutil.net_io_counters(pernic=False, nowrap=True)
        data['nic_addr'] = psutil.net_if_addrs()
        data['tmp'] = psutil.sensors_temperatures(fahrenheit=False)
        data['boot_time'] = psutil.boot_time()
        data['c_user'] = psutil.users()
        data['reload'] = time.time()
        #return render_template('dashboard.html',cpu=cpu)
        return render_template('dashboard.html', data=data)
        #return 'Logged in as %s' % escape(session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/updFirm')
def upfirm():
	return "upfirm ok"
@app.route('/ble')
def ble():
	return render_template('ble.html')

@app.route('/wifi')
def wifi():
	return render_template('wifi.html')


def cm(dt):
	klog = subprocess.Popen(dt, shell=True, stdout=subprocess.PIPE).stdout
	klog1 =  klog.read()
	pc = klog1.decode()
	return pc
# ============================================================MQTT-CONSOLE
@app.route('/mqtt-console')
@app.route('/mqtt-console/')
def mqtt_on():
    if 'username' in session:
        print("1111111111111111111111111111111111111111111111111111111111")
        klog = subprocess.Popen("dmesg", shell=True, stdout=subprocess.PIPE).stdout
        klog1 =  klog.read()
        pc = klog1.decode()
        print(klog)
        return render_template('mqtt-console.html', data=pc)
    else:
        return redirect(url_for('login'))

# =============================================================CMD LINE
@app.route('/sendcmd/<cmd>')
def sendcmd(cmd=None):
	if 'username' in session:
		return "comand received!"

# ============================================================UPDATE ADMIN DETAILS
@app.route('/editProfile/', methods=['GET', 'POST'])
def editProfile():
	error = None
	data = []
	rec=[]
	if 'username' in session:
		if request.method == 'POST':
			print("Posted********************************************")
			data.append(request.form['name'])
			data.append(request.form['pass'])
			print(data)
			#print(_mysql.editProfile_(mysql, data))
			conn = sqlite3.connect('gw_FlaskDb.db')
			conn.execute("INSERT INTO login (username,password) VALUES (?,?)",(data[0], data[1]) )
			conn.commit()
			conn.close()
			msg = "Record successfully added"
		

		conn = sqlite3.connect('gw_FlaskDb.db')
		f = conn.execute("SELECT * FROM login")
		rec = f.fetchall()
		print(rec)
		conn.close()

		#rec = _mysql.show_(mysql)
		print(rec)
		return render_template('editProfile.html', error=error, data=data, rec=rec)
	else:
		return redirect(url_for('login'))



# ============================================================SETUP PAGE
@app.route('/setup',methods = ['POST', 'GET'])
@app.route('/setup/',methods = ['POST', 'GET'])
def setup():
    if 'username' in session:   
        print("this is setup page")
        result = request.form.to_dict()
        print(result)
        with open("./tp.text", "w") as f:
            json.dump(result, f, indent=4)
        return render_template('setup.html')
    else:
        return redirect(url_for('login'))





# ============================================================LOGIN PAGE
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	#print(_mysql.initLogin_(mysql))
	if request.method == 'POST':
		u_name = request.form['username']
		u_pass = request.form['password']
		flag = 0
		conn = sqlite3.connect('gw_FlaskDb.db')
		f = conn.execute("SELECT * FROM login WHERE username=? and password=?", (u_name, u_pass))
		print(f)
		v = f.fetchall()
		if(len(v) > 0):
			flag = 0
		else:
			flag = -1
		print(v)
		conn.close()
		if(flag == -1):
			error = 'Invalid Credentials. Please try again.'
		else:
			session['username'] = request.form['username']
			return redirect(url_for('index'))
	return render_template('login.html', error=error)

# ============================================================LOGOUT PAGE
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


if  __name__  ==  '__main__' : 
    app.run(host = '0.0.0.0',  port = 5000, threaded = True,  debug = True) #, ssl_context='adhoc') #Ssl_context = Context ,