# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 00:27:09 2020

@author: user
"""

from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000)