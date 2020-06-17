import sqlite3
from db import db

from typing  import Dict, List, Union 
#we are adding type hinting to make sure that the parameter and the methods are of thye right type when we interract with them
#when we do type hinting we can access the primitive types by default without having to import anything, but if we want to use complex types like dictionaries,
# list etc we have to import them from the typing module
# the type hint is really optional

# Creating our custom json
ItemJSON =Dict[str, Union[int, str, float]]
#means the itemJSON is a dictionary that has strings as keys and either int str o float as values

class ItemModel(db.Model):
  __tablename__ = "items"

  id = db.Column(db.Integer, primary_key=True)       #we tell it what column the table contains i.e we tell alchemy their is column called id which is an integer and has ptimary key
  name = db.Column(db.String(80), unique=True)  #we are adding uniqueness so that no two items have thesame name on the table
  price = db.Column(db.Float(precision=2))

  store_id = db.Column(db.Integer, db.ForeignKey("stores.id")) #stores.id which is the name of the column in stores.py
  store = db.relationship("StoreModel")

  def __init__(self, name: str, price:float, store_id:int):
    self.name = name
    self.price = price
    self.store_id = store_id

#self is the object that we are calling, we can hint what the json method is going to return
  # -> means return
  #we are now using ItemJSON in place of Dict since we have decleared it at the top
  def json(self) -> ItemJSON: #this means we are returning dictionary
    return {"id":self.id, "name": self.name, "price": self.price, "store_id":self.store_id}

  @classmethod        #we continue with the class method here because it returns an object of item model as oppose to a dictionary
  #retuning a current class as a type in our type hints
  # "ItemModel", this is the way python reccommends returning self type
  def find_by_name(cls, name:str) -> "ItemModel":
    return cls.query.filter_by(name=name).first()    # select * FROM items  WHERE name = name LIMIT =1
    # connection = sqlite3.connect("data.db")
    # cursor = connection.cursor()

    # query = "SELECT * FROM items WHERE name=?"
    # result = cursor.execute(query, (name,))
    # row = result.fetchone()
    # connection.close()
    
    # if row:
    #     # return {"item": {"name": row[0], "price":row[1]}}
    #     return cls(*row)
  @classmethod
  def find_all(cla) -> List["ItemModel"]:
    return cls.query.all()

#This should return an object of item model instead fo a dictionary
  def save_to_db(self) -> None: # ->None ia not necessary
  # def insert(self):
    # if self.find_by_name(name):    #we can use slef ot Item which is class name
    #   return {"message": "An item with the name '{}' already exist. ".format(name)}, 400
    # # if next(filter(lambda x: x["name"] == name, items), None):
    # #   return {"message": "An item with the name '{}' already exist. ".format(name)}, 400
    # # data = request.get_json()
    # data = Item.parser.parse_args()
    # item = {"name": name, "price": data["price"]}  #we create json of the database
    #ues before adding to database
    # items.append(item) #append this new item, after you have append then return the item
    #second method
    # connection = sqlite3.connect("data.db")
    # cursor = connection.cursor()

    # query = "INSERT INTO items VALUES(?, ?)"
    # cursor.execute(query, (self.name, self.price))
    
    # connection.commit()
    # connection.close()

    #third method with sqlalchemy
    db.session.add(self) #The session is a collections of object to be pass to the database
    db.session.commit() #This whole method is good for both update and insert
  def delete_from_db(self) -> None:
  # def update(self):
  #     connection = sqlite3.connect("data.db")
  #     cursor = connection.cursor()

  #     query = "UPDATE items SET price=? WHERE name=?"
  #     cursor.execute(query, (self.price, self.name))

  #     connection.commit()
  #     connection.close()
    db.session.delete(self)
    db.session.commit()