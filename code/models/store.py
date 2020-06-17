# import sqlite3
from db import db
from typing import Dict, List, Union
from models.item import ItemJSON
#this import is for this line below
StoreJSON = Dict[str, Union[int, str, List[ItemJSON]]]

class StoreModel(db.Model):
  __tablename__ = "stores"

  id = db.Column(db.Integer, primary_key=True)       #we tell it what column the table contains i.e we tell alchemy their is column called id which is an integer and has ptimary key
  name = db.Column(db.String(80), unique=True)  #when the database is created it will add uniqueness constraint to the table so that no two items have thesame name

  #creating a back reference
  #it allows the store to see which items are in the items database or in items table with the store_id equals to it's own id
  items = db.relationship("ItemModel", lazy="dynamic")
  #lazy="dynamic" : do not go into items table and create an object for each items

  def __init__(self, name:str):
    self.name = name
    # self.price = price

  def json(self) -> StoreJSON:
    # return {"name": self.name, "items": self.items}
    return {"id": self.id, "name": self.name, "items": [item.json() for item in self.items.all()]} #we include .all() because of lazy=dynamic that will throw error

  @classmethod        #we continue with the class method here because it returns an object of item model as oppose to a dictionary
  def find_by_name(cls, name:str) -> "StoreModel":
    return cls.query.filter_by(name=name).first()    # select * FROM items  WHERE name = name LIMIT =1

  @classmethod
  def find_all(cls) -> List["StoreModel"]:
    return cls.query.all()

  def save_to_db(self) -> None:

    db.session.add(self) #The session is a collections of object to be to the database
    db.session.commit() #This whole method is good for both update and insert
  
  def delete_from_db(self) -> None:
  
    db.session.delete(self)
    db.session.commit()