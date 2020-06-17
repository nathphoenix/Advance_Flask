#HOW TO TURN AN OBJECT INTO A DICTIONARY USING MARSHMALLOW

from marshmallow import Schema, fields


#this defines what fields are in a field
#Bookschema must inherit from the imported marshmallow schema
#this is what we want our user to see and work with
# THIS IS WHAT MARSHMALLOW IS BUILD FOR OR ATLEAST THE SERIALIZATION  PART OF MARSHMALLOW
#Which is turning classes into dictionaries

class BookSchema(Schema):   #this class has been turned into ditionaries
  title = fields.Str()
  author = fields.Str()

#this is what our program is going to work with
class Book :
  def __init__(self, title, author, description):
    self.title = title
    self.author = author
    self.description = description
book = Book("Clean code", "Bob Martin", "A book about cleaner code")
book_schema = BookSchema()
book_dict = book_schema.dump(book)
print(book_dict)













