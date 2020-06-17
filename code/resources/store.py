from flask_restful import Resource
from models.store import StoreModel

STORE_ERROR = "Store not found"
NAME_ERROR = "An item with the name '{}' already exist."
INSERT_ERROR = "An error occured while creating store"
STORE_DELETED = "Store deleted successfully"


class Store(Resource):
  @classmethod
  def get(cls, name:str):
    store = StoreModel.find_by_name(name)
    if store:
      return store.json()
    return {"message": "store not found"}, 404

  @classmethod
  def post(cls, name:str):
    if StoreModel.find_by_name(name):
      return {"message": NAME_ERROR.format(name)}, 400
    
    store = StoreModel(name)
    try:
      store.save_to_db()
    except:
      return {"message": INSERT_ERROR}, 500
    return store.json(), 201
  @classmethod
  def delete(cls, name: str):
    store = StoreModel.find_by_name(name)
    if store:
      store.delete_from_db()
    return {"message": STORE_DELETED}


class StoreList(Resource):
  @classmethod
  def get(cls):
    return {"stores": [store.json() for store in StoreModel.query.all()]}