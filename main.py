# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 19:05:49 2020
@author: user
"""
# Publishable key : pk_test_iC57QJk6E5OX4yGET2ti9cYN00MW6uUVsd
#Secret Key = sk_test_692Gz0OKlX5IZ38XSGzkal1F009ztBb44Q
# SET in cmd

from flask import Flask
from flask import flash, redirect, render_template, request, session, abort,url_for
import os
# import stripe
import sqlite3
from sqlalchemy import create_engine


from sqlalchemy.orm import sessionmaker
def connect_db():
    return sqlite3.connect(database)

from database import *
engine = create_engine('sqlite:///database.db', echo=True)

#SET STRIPE_PUBLISHABLE_KEY=pk_test_iC57QJk6E5OX4yGET2ti9cYN00MW6uUVsd
#SET STRIPE_SECRET_KEY=sk_test_692Gz0OKlX5IZ38XSGzkal1F009ztBb44Q


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
            return home()
    else:
           flash('Oops,Try again','error')
           return login()
       
@app.route("/home")
def home():
    return render_template('home.html')
       
        

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return login()

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/Transfer")
def Transfer():
    return render_template("Transfer.html") #, key=stripe_keys['publishable_key'])

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

def Registration():
    if request.method=="POST":       
        username=request.form['username']
        password=request.form['password']        
        
        Session = sessionmaker(bind=engine)
        session = Session()
        register = User(username = username, password = password)
#    session.execute("INSERT INTO users(username,password) VALUES(:username,:password)",{"username":username,"password":secure_password})
        session.add(register)
        session.commit()
        flash("Registration successful!")
        
        return redirect(url_for("login"))       
    return render_template("Registration.html")

@app.route("/Account")
def Account():
    return render_template("account.html")


if __name__ == "__main__":
    app.run(debug=True)