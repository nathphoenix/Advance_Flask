# import sqlite3
from flask import Flask, request
from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required, 
#  get_jwt_claims,
#  jwt_optional,
#  get_jwt_identity,
 fresh_jwt_required)
from models.item import ItemModel
BLANK_ERROR = "'{}' Cannot be empty"
ITEM_ERROR = "Item not found"
NAME_ERROR = "An item with the name '{}' already exist."
INSERT_ERROR = "An error occurred in inserting item"
ITEM_DELETED = "item deleted successfully"

class Item(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument("price", type=float, required=True, help=BLANK_ERROR.format("price"))
  parser.add_argument("store_id", type=int, required=True, help=BLANK_ERROR.format("store_id"))


  # @jwt_required #this is a decorator, we can use this on any of our method that we want to add
  #authentication to before the method will run, if user has no token it will not work
  #we changing the instance of the class to class method
  @classmethod
  #we can use the classmethod when the method you are defining interract with the main class
  def get(cls, name:str):
    #fetching item from our database
    item = ItemModel.find_by_name(name)
    if item:
      return item.json()      #we can't return item but the json format 

    
    return {"message": ITEM_ERROR}, 404


    #New method this fetch from static database not the main database
    # item = next(filter(lambda x: x["name"] == name, items), None)
    # return {"item": item}, 200 if item else 404
    #old method
    # for item in items:
    #   if item["name"] == name:
    #        return item

  #we define a new mwthod and then allow other methods to inherit from it instead of repition of codes
  @classmethod  #note that classmethod goes on top
  @fresh_jwt_required   #u can use it anywhere u want
  def post(cls, name:str):
    if ItemModel.find_by_name(name):    #we can use slef ot Item which is class name
      return {"message": NAME_ERROR.format(name)}, 400
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
      return {"message": INSERT_ERROR}, 500 #internal server error
    
    return item.json(), 201

  @classmethod
  @jwt_required
  def delete(cls, name:str):

    #commented this out for the advance couse purpose
    #(
    # claims = get_jwt_claims()
    # if not claims["is_admin"]:
    #   return {"message": "Admin priileges is required"}, 401
    #)
    #stopped here
    
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
    return {"message": ITEM_DELETED}
  
  #the orders matter, declare your function before calling them and not after
  
    
  #WE USE THIS TO EDIT AND UPDATE OUR RECORDS
  @classmethod
  def put(cls, name:str):
    
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
  @classmethod
  # @jwt_optional removed this for the advance course
  def get(cls):
      #just using this for refactoring the code to a simpler function for now
    return {"items": [item.json() for item in ItemModel.query.all()]}, 200


    #old
    # user_id = get_jwt_identity() #we get the identity stored in jwt, if there is no jwt key, it returns nonw
    # items = [items.json() for item in ItemModel.find_all()]
    # if user_id:
    #   return{"items: items"}, 200
    # # return {"items": [item.json() for item in ItemModel.query.all()]}
    #       #OR
    # return {
    #     "items": [item["name"] for item in items],
    #     "message": "more data available if you are log in"
    #     }, 200

      
    # connection = sqlite3.connect("data.db")
    # cursor = connection.cursor()

    # query = "SELECT * FROM items"
    # result = cursor.execute(query)
    # items = []
    # for row in result:
    #   items.append({"name":row[0], "price":row[1]})

    
    # connection.close()
    # return {"items": items}


