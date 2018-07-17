from flask import Flask
from flask import json
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from Classes import users
import pymysql

pymysql.install_as_MySQLdb()
app = Flask(__name__)
conn = pymysql.connect(host='localhost', user='root', password='root', db='users')

#Methods for views
@app.route('/')
def index():
    return render_template('signup.html', title='Sign Up')

@app.route('/login')
def login():
    return render_template('login.html', title='Login')

@app.route('/home')
def home():
    if session.get('user') is not None:
        user = session['user']
        return render_template('home.html', data=user)
    return redirect(url_for('login'))
    
@app.route('/users')
def users():
    if session.get('user') is not None:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        data = cursor.fetchall()
        return render_template('users.html', data=data)
    return redirect(url_for('login'))

@app.route('/user', methods=['GET'])
def user():
    if session.get('user') is not None:
        id = request.args.get('id')
        cursor = conn.cursor()
        query = "SELECT * FROM users where id = '" + id + "'"
        rows = cursor.execute(query)
        if (rows > 0 or id is None):
            user = cursor.fetchone()
            cursor.close()
            return render_template('user.html', user=user)
        else:
            return redirect(url_for('home'))
    return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    if session.get('user') is not None:
        session.clear()
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
#Methods for CRUD
@app.route('/create', methods=['POST'])
def create():
    username = str(request.form['username'])
    password = str(request.form['password'])
    email = str(request.form['email'])
    cursor = conn.cursor()
    cursor.execute('insert into users (name, password, email) values (%s, %s, %s)', (username, password, email))
    conn.commit()
    return redirect(url_for('login'))

@app.route('/read', methods=['POST'])
def read():
    email = str(request.form['email'])
    password = str(request.form['password'])
    cursor = conn.cursor()
    query = "SELECT * FROM users where email = '" + email + "' and password = '" + password + "'"
    rows = cursor.execute(query)
    if (rows > 0):
        user = cursor.fetchone()
        session['user'] = user
        return redirect(url_for('home'))
    else:
        return 'falied'
    
@app.route('/update', methods=['POST'])
def update():
    if session.get('user') is not None:
        id_user = str(request.form['id'])
        username = str(request.form['username'])
        password = str(request.form['password'])
        email = str(request.form['email'])
        cursor = conn.cursor()
        query = "UPDATE users SET name = '" + username + "', password = '" + password + "', email = '" + email + "' WHERE id = '" + id_user + "'"
        cursor.execute(query)
        conn.commit()
        return redirect(url_for('users'))
    return redirect(url_for('login'))

@app.route('/delete', methods=['POST'])
def delete():
    if session.get('user') is not None:
        id_delete = str(request.form['id_delete'])
        cursor = conn.cursor()
        query = "DELETE FROM users WHERE id = '" + id_delete + "'"
        cursor.execute(query)
        conn.commit()
        return redirect(url_for('users'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(debug=True)