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
import stripe
import sqlite3
from sqlalchemy.orm import sessionmaker
def connect_db():
    return sqlite3.connect(database)

from database import *
engine = create_engine('sqlite:///database.db', echo=True)

#SET STRIPE_PUBLISHABLE_KEY=pk_test_iC57QJk6E5OX4yGET2ti9cYN00MW6uUVsd
#SET STRIPE_SECRET_KEY=sk_test_692Gz0OKlX5IZ38XSGzkal1F009ztBb44Q


app = Flask(__name__)
stripe_keys = {
  'secret_key': os.environ['STRIPE_SECRET_KEY'],
  'publishable_key': os.environ['STRIPE_PUBLISHABLE_KEY']
}
app.secret_key = "super secret key"

stripe.api_key = stripe_keys['secret_key']

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
    return render_template("Transfer.html", key=stripe_keys['publishable_key'])

@app.route("/Registration")
def Registration():
    return render_template("Registration.html")

@app.route("/Account")
def Account():
    return render_template("account.html")

@app.route('/charge', methods=['POST'])
def charge():

    # amount in cents
    amount = 500

    customer = stripe.Customer.create(
        email='first@customer.com',
        source=request.form['stripeToken']
    )

    stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )

    return render_template('charge.html', amount=amount)
if __name__ == "__main__":
    app.run(debug=True)