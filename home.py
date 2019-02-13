from flask import *
from datetime import date,datetime
import sqlite3, hashlib, os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key ='random string'
UPLOAD_FOLDER ='static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

def getLoginDetails():
	if 'email' not in session:
		loggedIn = False
		firstName=''
		email=''
		return (loggedIn, firstName, email)
	else:
		with sqlite3.connect('database.db') as conn:
			cur=conn.cursor()
			loggedIn=True
			cur.execute("SELECT firstName,email FROM users WHERE email='"+session['email']+"'")
			firstName,email = cur.fetchone()
		conn.close()
		return (loggedIn, firstName,email)
@app.route("/StudentLogin.html")
def root():
	loggedIn,firstName,email=getLoginDetails()
	with sqlite3.connect('database.db') as conn:
		if loggedIn:
			cur=conn.cursor()
			cur.execute('SELECT title, blog, createddate FROM blogs ORDER BY createddate')
			itemData=cur.fetchall()
			itemData=parse(itemData)
			return render_template('homes.html', itemData=itemData, loggedIn=loggedIn,firstName=firstName, email=email)
		else:
			cur=conn.cursor()
			cur.execute('SELECT title, blog, createddate FROM blogs ORDER BY createddate')
			itemData=cur.fetchall()
			itemData=parse(itemData)
			return render_template('homes.html', itemData=itemData, loggedIn=loggedIn)

@app.route("/root1")
def root1():
	loggedIn,firstName,email=getLoginDetails()
	with sqlite3.connect('database.db') as conn:
		if loggedIn:
			cur=conn.cursor()
			cur.execute('SELECT title, blog, createddate FROM blogs ORDER BY createddate')
			itemData=cur.fetchall()
			itemData=parse(itemData)
			return render_template('homes.html', itemData=itemData, loggedIn=loggedIn,firstName=firstName, email=email)
		else:
			cur=conn.cursor()
			cur.execute('SELECT title, blog, createddate FROM blogs ORDER BY createddate')
			itemData=cur.fetchall()
			itemData=parse(itemData)
			return render_template('homes.html', itemData=itemData, loggedIn=loggedIn)

@app.route("/logout")
def logout():
	session.pop('email', None)
	return redirect(url_for('root'))

def parse(data):
	print(data)
	ans=[]
	i=0
	while i<len(data):
		cur=[]
		for j in range(1):
			if i>=len(data):
				break
			print(data[i])
			cur.append(data[i])
			i+=1
			print(cur)
		ans.append(cur)
	return ans

@app.route("/loginForm")
def loginForm():
	if 'email' in session:
		return redirect(url_for('root'))
	else:
		return render_template('logins.html', error='')

@app.route("/login", methods=['POST','GET'])
def login():
	if request.method=='POST':
		email=request.form['email']
		password = request.form['password']
		if is_valid(email,password):
			session['email'] = email
			return redirect(url_for('root'))
		else:
			error='Invalid UserID/Password'
			return render_template('logins.html', error=error)

def is_valid(email,password):
	con = sqlite3.connect('database.db')
	cur=con.cursor()
	cur.execute('SELECT email, password FROM users')
	data= cur.fetchall()
	for row in data:
		if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
			return True
	return False

@app.route("/register", methods=['GET','POST'])
def register():
	if request.method=='POST':
		password=request.form['password']
		email=request.form['email']
		firstName=request.form['firstName']
		lastName=request.form['lastName']

		with sqlite3.connect('database.db') as con:
			try:
				cur=con.cursor()
				cur.execute('INSERT INTO users (password, email, firstName, lastName) VALUES(?,?,?,?)', (hashlib.md5(password.encode()).hexdigest(), email, firstName, lastName))
				con.commit()
				msg="registered successfully"

			except:
				con.rollback()
				msg="error occured"
		con.close()
		return render_template("logins.html", error = msg)

@app.route("/registrationForm")
def registrationForm():
	return render_template("registers.html")

@app.route("/viewmine")
def viewmine():
	loggedIn,firstName,email=getLoginDetails()
	with sqlite3.connect('database.db') as conn:
		cur=conn.cursor()
		cur.execute("SELECT title,blog,createddate FROM blogs WHERE email='"+session['email']+ "' ORDER BY createddate DESC")
		itemData=cur.fetchall()
	itemData=parse(itemData)
	return render_template('homes.html', itemData=itemData, loggedIn=loggedIn,firstName=firstName, email=email)


@app.route("/addblog")
def addblog():
	if 'email' in session:
		return render_template('addblog.html')		
	else:
		return redirect(url_for("root"))

@app.route("/addtoblog", methods=['GET','POST'])
def addtoblog():
	loggedIn,firstName,email=getLoginDetails()
	today=date.today()
	if request.method=='POST':
		title = request.form['title']
		blog = request.form['blog']
		with sqlite3.connect('database.db') as con:
			try:
				cur=con.cursor()
				cur.execute('INSERT INTO blogs ( title, blog, email,createddate) VALUES (?,?,?,?)',(title, blog, email, today) )
				con.commit()
				msg="added successfully"
			except:
				con.rollback()
				msg="error occured"
		con.close()
		return redirect(url_for('root'))
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/log.html", methods=['GET', 'POST'])
def log():
    return render_template('log.html')
@app.route('/departments.html', methods=['GET', 'POST'])   
def department():
    return render_template('departments.html')

@app.route('/CCNSB.html', methods=['GET', 'POST'])  
def CCNSB():
    return render_template('CCNSB.html')
@app.route('/CVIT.html', methods=['GET', 'POST'])  
def CVIT():
    return render_template('CVIT.html')
@app.route('/CogSci.html', methods=['GET', 'POST'])  
def CogSci():
    return render_template('CogSci.html')
@app.route('/DSAC.html', methods=['GET', 'POST'])  
def DSAC():
    return render_template('DSAC.html')
@app.route('/LTRC.html', methods=['GET', 'POST'])  
def LTRC():
    return render_template('LTRC.html')
@app.route('/LSI.html', methods=['GET', 'POST'])  
def LSI():
    return render_template('LSI.html')
@app.route('/SPCRC.html', methods=['GET', 'POST'])  
def SPCRC():
    return render_template('SPCRC.html')

@app.route('/profblog.html', methods=['GET', 'POST'])  
def profblog():
    return render_template('profblog.html')

@app.route('/abhijit.html', methods=['GET', 'POST'])  
def abhijit():
    return render_template('abhijit.html')

@app.route('/nita.html', methods=['GET', 'POST'])  
def nita():
    return render_template('nita.html')

@app.route('/vinod.html', methods=['GET', 'POST'])  
def vinod():
    return render_template('vinod.html')

@app.route('/deva.html', methods=['GET', 'POST'])  
def deva():
    return render_template('deva.html')

@app.route('/harjinder.html', methods=['GET', 'POST'])  
def harjinder():
    return render_template('harjinder.html')

@app.route('/vineet.html', methods=['GET', 'POST'])  
def vineet():
    return render_template('vineet.html')

@app.route('/jawahar.html', methods=['GET', 'POST'])  
def jawahar():
    return render_template('jawahar.html')

@app.route('/deb.html', methods=['GET', 'POST'])  
def deb():
    return render_template('deb.html')

@app.route('/kamalakar.html', methods=['GET', 'POST'])  
def kamalakar():
    return render_template('kamalakar.html')

@app.route('/kishore.html', methods=['GET', 'POST'])  
def kishore():
    return render_template('kishore.html')

@app.route('/rajeev.html', methods=['GET', 'POST'])  
def rajeev():
    return render_template('rajeev.html')

@app.route('/abhishek.html', methods=['GET', 'POST'])  
def abhishek():
    return render_template('abhishek.html')

@app.route('/rama.html', methods=['GET', 'POST'])  
def rama():
    return render_template('rama.html')

@app.route('/shaik.html', methods=['GET', 'POST'])  
def shaik():
    return render_template('shaik.html')

@app.route('/garimella.html', methods=['GET', 'POST'])  
def garimella():
    return render_template('garimella.html')

@app.route('/anil.html', methods=['GET', 'POST'])  
def anil():
    return render_template('anil.html')

@app.errorhandler(404)
def http_404_handler(error):
	return render_template('error404.html')



if __name__ == '__main__':
    app.run(debug=True)