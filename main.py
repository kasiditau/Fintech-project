# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 19:05:49 2020
@author: user
"""
# Publishable key : pk_test_iC57QJk6E5OX4yGET2ti9cYN00MW6uUVsd
#Secret Key = sk_test_692Gz0OKlX5IZ38XSGzkal1F009ztBb44Q
# SET in cmd

from flask import Flask
from flask import flash, redirect, render_template, request, session, abort,url_for,g
import os
import sqlite3
# import stripe

#DATABASE = '/Fintech/APP/database.db'
DATABASE = 'C:/Users/Ronisha Basker/venv/Fintech-project-28-4-20(Kas new)/database.db'
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv
conn = sqlite3.connect('database.db')
c = conn.cursor()


from sqlalchemy.orm import sessionmaker
from database import *
from database import User
def connect_db():
    return sqlite3.connect()
# conn = connect_db(database.db)
engine = create_engine('sqlite:///database.db', echo=True)

#SET STRIPE_PUBLISHABLE_KEY=pk_test_iC57QJk6E5OX4yGET2ti9cYN00MW6uUVsd
#SET STRIPE_SECRET_KEY=sk_test_692Gz0OKlX5IZ38XSGzkal1F009ztBb44Q

firstname = 'Kas'
def store(string):
    return string
app = Flask(__name__)
app.secret_key = "super secret key"

# stripe_keys = {
#   'secret_key': os.environ['STRIPE_SECRET_KEY'],
#   'publishable_key': os.environ['STRIPE_PUBLISHABLE_KEY']
# }
# app.secret_key = "super secret key"

# stripe.api_key = stripe_keys['secret_key']

@app.route("/")
def login():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return logout()
    
@app.route('/login', methods=['POST'])
def do_admin_login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
            session['logged_in'] = True
            # cur = conn.cursor()
            # cur.execute("SELECT * FROM users WHERE username=?",(POST_USERNAME,))
            # conn.commit
            # conn.close
            # curr.fetchall
            #fname = User.query.filter_by(username=username).first()
            user = query_db('select * from users where username = ?',
                [POST_USERNAME], one=True)
            global firstname,lastname,username,password
            firstname = user[0]
            lastname = user[1]
            username = user[2]
            password = user[3]
            session['firstname'] = user[1]
            session['lastname'] = user[2]
            session['username'] = user[3]
            session['password'] = user[4]
            
            
            return home()
    else:
           flash('Oops,Try again','error')
           return login()
       
@app.route("/home")
def home():
    # user = query_db('select * from users where username = ?',
    #             [do_admin_login.POST_USERNAME], one=True)
    # if user is None:
    #     flash('No such user')
    # else:
    #     usernamee = do_admin_login.POST_USERNAME, 'has the id', user['user_id']
    return render_template('home.html')
       
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return login()

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/Transfer", methods=['GET','POST'])
def Transfer():
    if request.method=="POST":
        paymenttype = str(request.form['paymenttype'])
        paidamount = int(request.form['paidamount'])
        # payment = query_db('select * from transaction where username = ?',session['username'], one=True)
        #newpayment=transaction(username=session['username'],payment_type=paymenttype,amount=paidamount)
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO transactions (username,payment_type,amount) VALUES (?,?,?)", (session['username'], paymenttype, paidamount))
       # c.execute("INSERT INTO transaction (username,payment_type,amount)\
             # VALUES(session['username'], paymenttype, paidamount)")
       # c.execute("INSERT INTO students (name) VALUES (?)",(name))
        conn.commit()
        conn.close()
        flash("payment successful")
    return render_template("Transfer.html")
    # return render_template("charge.html") #, key=stripe_keys['publishable_key'])

@app.route("/Registration", methods=['GET','POST'])
#def Registration():
#    return render_template("Registration.html")

#def checkRegister():
#    POST_USERNAME = str(request.form["username"])
#    POST_PASSWORD = str(request.form["password"])
#    Session = sessionmaker(bind=engine)
#    s = Session()
#    query = s.query(User).filter(User.username.in_([POST_USERNAME]))
#    result = query.first()
#    if result:
#            flash('Username has been taken','error')
#    else:
#            return register()
@app.route('/Register', methods=['GET', 'POST'])
def Registration():
    # Session = sessionmaker(bind=engine)
    # s = Session()
    if request.method=="POST":
        # if not request.form.get('username'):
        #     error = 'You have to enter a firstname'
        #     flash(error)
        # elif not request.form.get('lastnanme'):
        #     error = 'You have to enter a lastname'
        #     flash(error)
        # elif not request.form.get('password'):
        #     error = 'You have to enter a password'
        #     flash(error)
        # elif not request.form.get('confirmpassword'):
        #     error = 'You have to confirm a password'
        #     flash(error)
        # # elif get_user_id(request.form['username']) is not None:
        # #     error = 'The username is already taken'
        # #     flash(error)
        # else:
            firstname=request.form['firstname']
            lastname=request.form['lastname']
            username=request.form['username']
            password=request.form['password'] 
            confirmpassword=request.form['confirmpassword']  
                
            Session = sessionmaker(bind=engine)
            session = Session()
            register = User(firstname= firstname,lastname=lastname,username = username, password = password)
        #    session.execute("INSERT INTO users(username,password) VALUES(:username,:password)",{"username":username,"password":secure_password})
            session.add(register)
            session.commit()

            flash("Registration successful!")
            return render_template("login.html")
    return render_template("Registration.html")

@app.route("/Account")
def Account():
    # Session = sessionmaker(bind=engine)
    # session = Session()
    # user = query_db('select * from users where username = ?',
    #         do_admin_login().POST_USERNAME, one=True)
    # firstname = user[0]
    # session['firstname'] = firstname
    # session.commit
    return render_template("account.html")
@app.route("/charge")
def charge():
    return render_template("charge.html")

if __name__ == "__main__":
    app.run(debug=True)
    app.config['database.db'] = 'sqlite:////database.db'