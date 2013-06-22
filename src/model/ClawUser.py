'''
Created on Jun 19, 2013

@author: nick.velloff
'''
from google.appengine.ext import db


class ClawUser(db.Model):
    
    channel = db.StringProperty(required=False)
    timestamp = db.DateTimeProperty(required=False)