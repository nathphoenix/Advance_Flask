import sqlite3
from db import db
#resources is our external representation of an entity
#model is the internal representation of an entity
#api response to the resources

#this usermodel is an api
class UserModel(db.Model):    # by passing db.model as an argument to the class object, we make it extends db model in both cases
  __tablename__ = "users"  # this way we tell slchemy we are using the users table
  id = db.Column(db.Integer, primary_key=True)       #we tell it what column the table contains i.e we tell alchemy their is column called id which is an integer and has ptimary key
  username = db.Column(db.String(80))
  password = db.Column(db.String(80))
  #this must match the df init method below

  def __init__(self, username, password):
    self.username = username
    self.password = password
    # return super().__init__(*args, **kwargs)()
  
  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  @classmethod #we introduce this because we rae using the classname in our method which is User as we didn't use self
  def find_by_username(cls, username):
    return cls.query.filter_by(username=username).first()
    # connection = sqlite3.connect("data.db")
    # cursor = connection.cursor()

    # query = "SELECT * FROM users WHERE username=?"
    # result = cursor.execute(query, (username,))  # if the comma is not here it means an ordinary bracket instead of a tupple(username,)
    # row = result.fetchone()
    # if row:
    #   user = cls(*row)       # star.row a set of arguments to get multiple rows instead of using row[0] and so on
    # else:
    #   user = None
    # connection.close()
    # return user

  @classmethod #we introduce this because we rae using the classname in our method which is User as we didn't use self
  def find_by_id(cls, _id):
    return cls.query.filter_by(id=_id).first()
    # connection = sqlite3.connect("data.db")
    # cursor = connection.cursor()

    # query = "SELECT * FROM users WHERE id=?"
    # result = cursor.execute(query, (_id,))  # if the comma is not here it means an ordinary bracket instead of a tupple(username,)
    # row = result.fetchone()
    # if row:
    #   user = cls(*row)       # star.row a set of arguments to get multiple rows instead of using row[0] and so on
    # else:
    #   user = None
    # connection.close()
    # return user 
 