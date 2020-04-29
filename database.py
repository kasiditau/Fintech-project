# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 01:52:32 2020

@author: user
"""

from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///database.db', echo=True)
Base = declarative_base()
#######################################
class User(Base):
    """"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname  = Column(String)
    username = Column(String)
    password = Column(String)
    
    #----------------------------------------------------------------------
    def __init__(self,firstname,lastname, username, password):
        """"""
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.password = password
        
class transaction(Base):
    """"""
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True)
    username = Column(String)
    payment_type = Column(String)
    amount = Column(Integer)
    #----------------------------------------------------------------------
    def __init__(self,username,payment_type, amount):
        """"""
        self.username = username
        self.payment_type = payment_type
        self.amount = amount

                
# create tables
Base.metadata.create_all(engine)