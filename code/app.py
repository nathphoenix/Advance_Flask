from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = "Jose"
api = Api(app)

# class Student(Resource):
#   def get(self, name):
#     return {'student': name}
jwt = JWT(app, authenticate, identity)  #/auth

# api.add_resource(Student, "/student/<string:name>")
items = []

class Item(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument("price", type=float, required=True, help="Price Cannot be empty")

  @jwt_required() #this is a decorator, we can use this on any of our method that we want to add
  #authentication to before the method will run, if user has no token it will not work
  def get(self, name):
    #New method
    item = next(filter(lambda x: x["name"] == name, items), None)
    return {"item": item}, 200 if item else 404
    #old method
    # for item in items:
    #   if item["name"] == name:
    #        return item
    
  def post(self, name):
    if next(filter(lambda x: x["name"] == name, items), None):
      return {"message": "An item with the name '{}' already exist. ".format(name)}, 400
    # data = request.get_json()
    data = Item.parser.parse_args()
    item = {"name": name, "price": data["price"]}
    items.append(item) #append this new item, after you have append then return the item
    return item, 201

  def delete(self, name):
    global items #we are calling the main items list from above
    items = list(filter(lambda x: x["name"] != name, items)) #if name is not equal to that name return the remaining item list
    return {"message": "item deleted successfully"}
    
  #WE USE THIS TO EDIT AND UPDATE OUR RECORDS
  def put(self, name):
    
    # data = request.get_json()  #not using this cos of the new variable parser
    data = Item.parser.parse_args()    #we use Item cos parser belongs to the class Item

    item = next(filter(lambda x: x["name"] == name, items), None)
    if item is None:
      item = {"name": "name", "price": data["price"]}
      items.append(item)
    else:
      item.update(data)
    return item

class ItemList(Resource):
  def get(self):
    return {"items": items}

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")

app.run(port=5000, debug=True)