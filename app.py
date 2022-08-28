# Import all libraries used
from flask import Flask, render_template, url_for, redirect, request, session
from flask_mysqldb import MySQL
import yaml
import re
import hmac
import hashlib

# Initialise flask app and secret key
app = Flask(__name__)
app.secret_key = "chicken"

# Copy data from yaml file
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
# Returns data as dictionary instead of tuples
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialise mysql
mysql = MySQL(app)

# Functions that use hmac to encrypt user password in mysql database
secret = db['secret']
def make_secure_password(password):
    # For this project only the password will be stored in this format
    return f"{password}|{hmac.new(secret.encode('utf-8'),password.encode('utf-8'),hashlib.sha256).hexdigest()}"

# Not used yet
def check_secure_password(secure_password):
    password = secure_password.split('|')[0]
    if secure_password == make_secure_password(password):
        return True
    else:
        return False


# Main/Login page
@app.route('/', methods=['GET', 'POST'])
def index():
    msg=''

    # If there isn't already a login_info table, create one
    cur = mysql.connection.cursor()

    #DEBUGGING TOOL: REMOVE TABLE
    #cur.execute("DROP TABLE login_info")

    cur.execute("SHOW TABLES LIKE 'login_info'")
    result = cur.fetchone()
    if not result:
        cur.execute('''CREATE TABLE login_info (username VARCHAR(30), password VARCHAR(100))''')
        mysql.connection.commit()
    
    # Debugging function to look at all info from the mysql table
    cur.execute('SELECT * FROM login_info')
    all = cur.fetchall()
    print(all)


    # Check if "username" and "password" POST requests exist = user submitted form
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        # Verify if there is an account in the database that matches user entered data
        cur.execute('SELECT * FROM login_info where username = %s AND password = %s', (username, make_secure_password(password),))
        account = cur.fetchone()

        # If user has entered valid login details
        if account:
            session['loggedin'] = True
            session['username'] = account['username']

            # Redirect to loggedin page
            return redirect(url_for('loggedin'))

        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    # If username and password fields are empty but attributes:required covers this
    elif request.method == 'POST':
        msg = 'Enter both your username and your password!'
    return render_template('index.html', msg=msg)


    
# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    # Check if "username", "password" and "email" POST requests exist = user submitted form
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        secure_password = make_secure_password(password)

        # Check if account exists in MySQL database
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM login_info WHERE username = %s', (username,))
        account = cur.fetchone()

        # If account exists, show error
        if account:
            msg = 'Account already exists!'
        # Validation checks to ensure username is alphanumeric
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password:
            msg = 'Please fill out the form!'
        else:
            # Account doesn't exist, form data is valid, insert new account into login_info table
            cur.execute('INSERT INTO login_info(username, password) VALUES (%s, %s)', (username, secure_password,))
            mysql.connection.commit()
            cur.close()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty, no POST data
        msg = 'Please fill out the form!'

    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


# Logged in page
@app.route('/loggedin')
def loggedin():
    # Only if loggedin in session, which is set only when user enters valid login details
    if 'loggedin' in session:
        return render_template('loggedin.html', username=session['username'])
    else:
        # Return user back to login page if they just add /loggedin in url
        return redirect(url_for('index'))


# Change password page
@app.route('/changepassword', methods=['GET', 'POST'])
def changepassword():
    # Required attribute will ensure password field is filled in anyways
    msg = ''
    
    # If the user has entered valid login details beforehand
    if 'loggedin' in session:
        # If the user has submitted a form
        if request.method=='POST' and 'password' in request.form and 'current_password' in request.form:
            msg = 'Fill in your new password!'
            current_password = request.form['current_password']
            new_password = request.form['password']
            secure_password = make_secure_password(new_password) 
            cur = mysql.connection.cursor()

            # Validate password entered by user is correct before letting him set a new one
            cur.execute('SELECT * FROM login_info where username = %s AND password = %s', (session['username'], make_secure_password(current_password),))
            account = cur.fetchone()
            if account:
                # Password is verified, new password can now be updated
                cur.execute('UPDATE login_info SET password = %s WHERE username = %s', (secure_password, session['username'],))
                mysql.connection.commit()
                cur.close()
                msg = 'Your password has been updated!'
                return render_template('changepassword.html', username=session['username'], msg=msg)
            # Password is not verified
            else:
                msg = 'The password you entered in the verify current password field is wrong. Try again.'
                return render_template('changepassword.html', msg=msg, username=session['username'])
            
        else:
            return render_template('changepassword.html', username=session['username'], msg=msg)
    else:
    # Return user back to login page if they just add /changepassword in url
        return redirect(url_for('index'))


# Log out page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return render_template('loggedout.html')


# Run the app
if __name__ == "__main__":
    app.run(debug=True)