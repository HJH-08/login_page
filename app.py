from flask import Flask, render_template, url_for, redirect, request, session
from flask_mysqldb import MySQL
import yaml
import re

app = Flask(__name__)
app.secret_key = "chicken"

db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
# Returns data as dictionary instead of tuples
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    msg=''
    cur = mysql.connection.cursor()
    cur.execute("SHOW TABLES LIKE 'login_info'")
    result = cur.fetchone()
    if not result:
        cur.execute('''CREATE TABLE login_info (username VARCHAR(30), password VARCHAR(30))''')
        mysql.connection.commit()
    

    cur.execute('SELECT * FROM login_info')
    all = cur.fetchall()
    print(all)


    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        cur.execute('SELECT * FROM login_info where username = %s AND password = %s', (username, password))
        account = cur.fetchone()

        if account:
            session['loggedin'] = True
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('loggedin'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # If username and password fields are empty but attributes:required covers this
    elif request.method == 'POST':
        msg = 'Enter both your username and your password!'
    return render_template('index.html', msg=msg)

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return render_template('loggedout.html')

    

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

         # Check if account exists using MySQL
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM login_info WHERE username = %s', (username))
        account = cur.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into login_info table
            cur.execute('INSERT INTO login_info(username, password) VALUES (%s, %s)', (username, password))
            mysql.connection.commit()
            cur.close()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

@app.route('/loggedin')
def loggedin():
    if 'loggedin' in session:
        return render_template('loggedin.html', username=session['username'])
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
    