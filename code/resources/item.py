# import sqlite3
from flask import Flask, request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument("price", type=float, required=True, help="Price Cannot be empty")
  parser.add_argument("store_id", type=int, required=True, help="Every items need a store id")


  @jwt_required() #this is a decorator, we can use this on any of our method that we want to add
  #authentication to before the method will run, if user has no token it will not work
  def get(self, name):
    #fetching item from our database
    item = ItemModel.find_by_name(name)
    if item:
      return item.json()      #we can't return item but the json format 

    
    return {"message": "Item not found"}, 404


    #New method this fetch from static database not the main database
    # item = next(filter(lambda x: x["name"] == name, items), None)
    # return {"item": item}, 200 if item else 404
    #old method
    # for item in items:
    #   if item["name"] == name:
    #        return item

  #we define a new mwthod and then allow other methods to inherit from it instead of repition of codes
  
    
  def post(self, name):
    if ItemModel.find_by_name(name):    #we can use slef ot Item which is class name
      return {"message": "An item with the name '{}' already exist. ".format(name)}, 400
    # if next(filter(lambda x: x["name"] == name, items), None):
    #   return {"message": "An item with the name '{}' already exist. ".format(name)}, 400
    # data = request.get_json()
    data = Item.parser.parse_args()
    # item = {"name": name, "price": data["price"]}  #we create json of the database
    item = ItemModel(name, data["price"], data["store_id"])
    #ues before adding to database
    # items.append(item) #append this new item, after you have append then return the item
    try:
      item.save_to_db()
    except:
      return {"message": "An error occurred in inserting item"}, 500 #internal server error
    
    return item.json(), 201

 

  def delete(self, name):
    # with alchemy
    item = ItemModel.find_by_name(name)
    if item:
      item.delete_from_db()
    # global items #we are calling the main items list from above
    # items = list(filter(lambda x: x["name"] != name, items)) #if name is not equal to that name return the remaining item list
    #second method
    # connection = sqlite3.connect("data.db")
    # cursor = connection.cursor()

    # query = "DELETE FROM items WHERE name=?"
    # cursor.execute(query, (name,))
    
    # connection.commit()
    # connection.close()
    return {"message": "item deleted successfully"}
  
  #the orders matter, declare your function before calling them and not after
  
    
  #WE USE THIS TO EDIT AND UPDATE OUR RECORDS
  def put(self, name):
    
    # data = request.get_json()  #not using this cos of the new variable parser
    data = Item.parser.parse_args()    #we use Item cos parser belongs to the class Item

    # item = next(filter(lambda x: x["name"] == name, items), None)
    item = ItemModel.find_by_name(name)
    #not in use cos of alchemy
    # updated_item = ItemModel(name, data["price"])
    if item is None:
      item = ItemModel(name, data["price"], data["store_id"]) # we can represent data["price"], data["store_id"] as **data
      # try:
      #   updated_item.insert()
      # except:
      #   return{"message": "An error occured inserting the item"}, 500
      # # items.append(item)
    else:
      item.price = data["price"]
    item.save_to_db()
      # try:
      #    updated_item.update()   #note that update is a function accepting updated item as argument
      # except:
      #    return {"message": "An error occured, unable to update item"}, 500
    return item.json()
    

#This is for retrieving, many items from database
class ItemList(Resource):
  def get(self):
    # return {"items": [item.json() for item in ItemModel.query.all()]}
          #OR
      return {"items": list(map(lambda x: x.json(), ItemModel.query.all()))}
    # connection = sqlite3.connect("data.db")
    # cursor = connection.cursor()

    # query = "SELECT * FROM items"
    # result = cursor.execute(query)
    # items = []
    # for row in result:
    #   items.append({"name":row[0], "price":row[1]})

    
    # connection.close()
    # return {"items": items}