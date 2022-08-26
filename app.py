from flask import Flask, render_template, url_for
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

db = yaml.load(open('dib.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
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