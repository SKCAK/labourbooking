from flask import Flask,render_template,request,url_for,redirect
import sqlite3
import pandas as pd
 
app = Flask(__name__)
 
 
@app.route("/home")
@app.route("/")
def Home():
    return render_template("home.html",title="Welcome")
 
@app.route("/Worker/login",methods=['Get','POST'])
def Worker_login():
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	table = cur.execute("select * from worker")
	df = pd.DataFrame(table,
		columns=('Id','Username','Mail','Pno','Domain','Exp','Pass'))
	user = list(df['Username'])

	if request.method == "POST":
		name = request.form['wname']
		passw = request.form['pass']

		if user.count(name)>0:
			index = user.index(name)
			data = list(df.loc[index])
			print(data)
			print(name,passw,data[1],data[6])
			if str(data[1])==str(name) and str(data[6])==str(passw):
				return "Welcome "+data[1]
			else:
				return render_template("errot.html",
					title="Error",msg="Wrong Username or Password")
		else:
			return render_template("errot.html",
				title="Error",msg="Username Dose Not Exist")

	return render_template("login.html",title="Worker Login")
 
@app.route("/admin/login",methods=['Get','POST'])
def Admin_login():

	if request.method == "POST":
		name = request.form['wname']
		passw = request.form['pass']

		if name == 'admin' and passw == 'admin':
			return "Welcome"
		else:
			return render_template("errot.html",
				title="Error",msg="Wrong Username or Password")
	return render_template("login.html",title="Admin Login")

@app.route("/Worker/register",methods=['GET','POST'])
def worker_register():
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	table = cur.execute("select * from worker")
	df = pd.DataFrame(table,
		columns=('Id','Usename','Mail','Pno','Domain','Exp','Pass'))
	Usename = list(df['Usename'])
	ids = list(df['Id'])
	ids = len(ids)+1
	if request.method == 'POST':
		username = request.form['uname']
		mail = request.form['mail']
		pno = request.form['pno']
		domin = request.form['domain']
		exp = request.form['exp']
		pas1 = request.form['pass1']
		pas2 = request.form['pass2']

		if Usename.count(username)==0:
			if pas1 == pas2:
				qur = "insert into worker(id,username,mail,pno,domin,exp,password) values(?,?,?,?,?,?,?)"
				val = (ids,username,mail,pno,domin,exp,pas1)
				cur.execute(qur,val)
				con.commit()
				return redirect(url_for("Worker_login"))
			else:
				return render_template("errot.html",
					title="Error",msg="Password Not Maching")
		else:
			return render_template("errot.html",
				title="Error",msg="Username Already Exists")
	return render_template("worker_register.html",title="Worker Register")

@app.route("/Worker/password/reset",methods=['GET','POST'])
def wroker_password_reset():
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	table = cur.execute("select * from worker")
	df = pd.DataFrame(table,
		columns=('Id','Username','Mail','Pno','Domain','Exp','Pass'))
	user = list(df['Username'])
	if request.method == 'POST':
		username = request.form['uname']
		passw1 = request.form['pass1']
		passw2 = request.form['pass2']

		if user.count(username)>0:
			if passw1 == passw2:
				qur = 'update worker set password=? where username=?'
				val = (passw1,username)
				cur.execute(qur,val)
				con.commit()
				return render_template("sucess.html",
					title="Password Reset",msg="Password has been sucessfully changed",
					link="/Worker/login",value="Login")
			else:
				return render_template("errot.html",
					title="Password",msg="Password not maching")
		else:
			return render_template("errot.html",
				title="Username Error",msg="Username Dose Not Exist")

	return render_template("password_change.html",title="Password Reset")


 
if __name__ == "__main__":
    app.run(debug=True)

