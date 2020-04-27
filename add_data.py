# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 02:09:00 2020

@author: user
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import User

engine = create_engine('sqlite:///database.db', echo=True)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

user = User("Kas","kpac")
session.add(user)
session.commit()

user = User("Seoyoung","hsy")
session.add(user)
session.commit()

user = User("Ronisha","rnb")
session.add(user)
session.commit()

user = User("Nuthan","ngar")
session.add(user)
session.commit()

# commit the record the database
session.commit()
session.commit()

#INSERT INTO table (column1,column2 ,..)
#VALUES( value1,	value2 ,...);