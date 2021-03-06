import sqlite3
from flask_jwt_extended import create_access_token, get_jwt_identity, create_refresh_token, jwt_refresh_token_required, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp
from flask_restful import Resource, reqparse
from models.user import UserModel
from blacklist import BLACKLIST

BLANK_ERROR = "'{}' cannot be empty"
USER_ERROR = "A user with this email already exist"
USER_CREATED = "User created successfully"
USER_NOT_FOUND = "User not found"
USER_DELETED = "User deleted successfully"
INVALID_CREDENTIALS = "Invalid credentials"
USER_LOGGED_OUT = "User <id={}> Successfully logged out."

#the underscore(_) means this is a private variable
_user_parser = reqparse.RequestParser()
_user_parser.add_argument("username",
                      type=str,
                      required=True,
                      help=BLANK_ERROR.format("username"))
_user_parser.add_argument("password",
                      type=str,
                      required=True,
                      help=BLANK_ERROR.format("password"))

 
class UserRegister(Resource): #we use resource as we are interracting with the api
      # parser = reqparse.RequestParser()
      # parser.add_argument("username", type=str, required=True, help="This field cannot be empty")
      # parser.add_argument("password", type=str, required=True, help="This field cannot be empty")
      @classmethod
      def post(cls):

          data = _user_parser.parse_args()

          if UserModel.find_by_username(data["username"]):
              return {"message": USER_ERROR}, 400

        #   user = UserModel(data["username"], data["password"])
                        #OR....THIS ONE BELOW
          user = UserModel(**data)
          user.save_to_db()
        #   connection = sqlite3.connect("data.db")
        #   cursor = connection.cursor()

        #   query = "INSERT INTO users VALUES (NULL, ?, ?)"
        #   cursor.execute(query, (data["username"], data["password"]))

        #   connection.commit()
        #   connection.close()

          return {"message": USER_CREATED}, 201

class User(Resource):
  @classmethod
  def get(cls, user_id):
    user = UserModel.find_by_id(user_id)
    if not user:
      return {"message": USER_NOT_FOUND}, 404
    return user.json()  #we then go into usermodel and create the return for the json
  
  @classmethod
  def delete(cls, user_id):
    user = UserModel.find_by_id(user_id)
    if not user:
      return{"message": USER_NOT_FOUND}, 404
    user.delete_from_db()    #this function is not yet available in our usermodel, so we go and create it
    return {"message": USER_DELETED}, 200

class UserLogin(Resource):
  
  #we can use a classmethod here might implement it later
  @classmethod
  def post(cls):
    #get data from parser
    data = _user_parser.parse_args()
    #find user in the database
    user = UserModel.find_by_username(data["username"])
    #summary fo the function 
    #This is what the authenticate() function use to do
    #check password
    if user and safe_str_cmp(user.password, data['password']):
      # 'this is what the identity( ) function used to do'
      #create access token
      access_token = create_access_token(identity=user.id, fresh=True) #fresh=true i for token refreshing
      #create refresh token
      refresh_token = create_refresh_token(user.id)
      #return them
      return {
      "access_token": access_token,
      "refresh_token": refresh_token
      }, 200
    return {"message": INVALID_CREDENTIALS}, 401

class UserLogout(Resource):
  @classmethod
  @jwt_required
  def post(cls):
    jti = get_raw_jwt["jti"] #jti is "JWT ID" a unique identifier for a jwt
    BLACKLIST.add(jti)
    return {"message": USER_LOGGED_OUT.format(user_id=user_id)}, 200

class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
      current_user = get_jwt_identity()
      new_token = create_access_token(identity=current_user, fresh=False)
      return {"access_token": new_token}, 200
