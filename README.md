<br>

<p align="center">
    <img src="https://img.shields.io/github/last-commit/hjh-08/login_page" />
    <img src="https://img.shields.io/github/repo-size/hjh-08/login_page">
<p>


<p align="center">
  <a href="#login-page">About</a> •
  <a href="#recording-of-the-login-page-in-use">Visuals</a> •
  <a href="#prerequisites">Prerequisites</a> •
  <a href="#how-to-run-the-script">Instructions</a> 
</p>

# Login Page

## Combining HTML, CSS, Python, MySQL and Hash Authentication

This project is mostly written in `Python`. A user can register a username and a password. This information is then uploaded into a database, which is hosted live as of the time this project is last edited. The password is stored along with a **hashed string** into the databse. When a user logs in, hash authentication is used to ensure encryption of password (though the plain-text password is stored in the database for debugging purposes right now). A session is created, and the user is directed to a **loggedin** page which cannot be otherwise accessed. The user can change his password, which updates the database. He can then log out, which ends his session. <br>  
The project uses:

* `Flask` framework to build the web application
* `MySQL` as a database to store all the users' login information
* `https://www.freemysqlhosting.net/` to host the database live
* `yaml` to store confidentail (sort of) information of the database and secret key
* `Regular Expressions` to ensure validity of username selected
* `HTML` and `CSS` for styling the web application
* `HMAC` and `hashlib` to safely store and authenticate user login data. This involves cryptographic hash functions as well as a secret key

<br>

## Recording of the login page in use

This shows how the user can register, login, change his password and logout. It also shows the error messages when an incorrect password is entered.


![Recording of login page](https://github.com/HJH-08/login_page/blob/main/Login%20Page%20Video.gif)

___
<br>
     
## Prerequisites
       
`Python` should be installed locally. Check [here](https://www.python.org/downloads/) to install depending on your OS.

### Required Modules
- `flask`
- `flask_mysqldb`
- `yaml`


To install `flask`:
```
$ pip install Flask
```


To install `flask_mysqldb`: 
```
$ pip install Flask-MySQLdb
```

To install `yaml`:
```
$ pip install PyYAML
```

<br>

### How to run the script
``` bash
$ python app.py
```
When the above code is run, something like this should appear in the terminal:
<br>

![Terminal when code is run](https://github.com/HJH-08/login_page/blob/main/login%20page%20instructions.png)
<br>

**Ctrl + click** on the underlined part of the code (http://127.0.0.1:5000 in the case of the picture shown above) to serve the project.
