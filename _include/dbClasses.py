#------------------------------------------MYSQL CLASS
class mysqldb:
	def initMysql_(MySQL, app):
		app.config['MYSQL_HOST'] = 'localhost'
		app.config['MYSQL_USER'] = 'root'
		app.config['MYSQL_PASSWORD'] = 'root'
		app.config['MYSQL_DB'] = 'FlaskDb'
		mysql = MySQL(app)
		print(mysql)
		print("---------------Init -MYSQLDB---------------")
		return mysql
	# Create the DataBase-----------------------------------------------------------------------------------This One have to edit 
	def createModel_(MySQL, app):
		app.config['MYSQL_HOST'] = 'localhost'
		app.config['MYSQL_USER'] = 'root'
		app.config['MYSQL_PASSWORD'] = 'root'
		mysql = MySQL(app)
		print(mysql)
		cur = mysql.connection.cursor()
		dbs_ = cur.execute("SHOW DATABASES")
		ax = cur.fetchall()
		print(ax)
		for a in ax:
			if('FlaskDb' in a[0]):
				print(a)
				print("it exist")
				cur.close()
				mysql=0
				return 'OK'
			else:
				#query = "DROP DATABASE FlaskDb"
				#cur.execute(query)
				cur = mysql.connection.cursor()
				cur.execute("CREATE DATABASE FlaskDb")
				cur.execute("USE FlaskDb")
				cur.execute("CREATE TABLE login_(id int(11) PRIMARY KEY AUTO_INCREMENT, firstName VARCHAR(30), lastName VARCHAR(30))")      
				cur.execute("INSERT INTO login_(firstName, lastName) VALUES (%s, %s)", ("admin", "pass"))
				print("inserted....")
				mysql.connection.commit()
				cur.close()
				return "OK"
		print("---------------Create Model -MYSQLDB---------------")
		return "OK"
	# Login Verify
	def verify_(u_name, u_pass, mysql):
		cur = mysql.connection.cursor()
		print(u_name)
		print(u_pass)
		print("---------------Verify Login -MYSQLDB---------------")
		flag1 = cur.execute("SELECT * FROM login_ WHERE firstName=%s and lastName=%s", (u_name, u_pass))
		print(flag1)
		if(flag1 < 1):
			cur.close()
			return -1
		else:
			myresult = cur.fetchone()
			print(myresult)
			cur.close()
			return 0

	def show_(mysql):
		cur = mysql.connection.cursor()
		#print(cur.execute("SELECT version()"))
		#print(cur.fetchall())
		#print(cur)
		if(cur.execute("SELECT * FROM login_") == 0):
			print("There is no record!")
		rec = cur.fetchall()
		print("---------------Show Table -MYSQLDB---------------")
		return rec

	def editProfile_(mysql, data):
		cur = mysql.connection.cursor()    
		cur.execute("INSERT INTO login_(firstName, lastName) VALUES (%s, %s)", (data[0], data[1]))
		mysql.connection.commit()
		cur.close()
		print("---------------Update Profile -MYSQLDB---------------")
		return 'OK'

	def delProfile_(mysql, ids):
		cur = mysql.connection.cursor()    
		cur.execute("DELETE FROM login_ where id= %s", (ids))
		mysql.connection.commit()
		cur.close()
		print("---------------Delete Profile -MYSQLDB---------------")
		return 'OK'
		

