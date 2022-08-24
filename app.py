
from flask import Flask, render_template, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'sql6.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql6514845'
app.config['MYSQL_PASSWORD'] = 'G78VEgnEUk'
app.config['MYSQL_DB'] = 'sql6514845'
# Returns data as dictionary instead of tuples
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    #cur.execute('''CREATE TABLE login_info (username VARCHAR(30), password VARCHAR)''')
    #cur.executre('''INSERT INTO login_info VALUES ('joe', 'pw;)''')
    #mysql.connection.commit()

    #cur.execute('''SELECT * FROM login_info''')
    #results = cur.fetchall()
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    return render_template('index.html', msg='')

if __name__ == "__main__":
    app.run(debug=True)