#HOW TO TURN A DICTIONARY INTO AN OBJECT USING MARSHMALLOW

from marshmallow import Schema, fields, INCLUDE, EXCLUDE




class BookSchema(Schema):
  title = fields.Str()
  author = fields.Str()
  # description = fields.Str()
  
  # description = fields.Str(required=True) the equired is also a form of validation
  #if required  and was removed fom the incoming_book_data below, it will throw an error

#we have some JSON data that we want to pass through our BookSchema in order
#to get a book out


#this is what our API might recieve from our users which is some JSON
incoming_book_data = {
    "title": "Clean code",
    "author": "Book Martin",
    "description": "A book about cleaner code"
}

#We create an instance of our BookSchema
#the EXCLUDE get rid of description when passed through our BookSchema
book_schema = BookSchema(unknown=EXCLUDE)
book = book_schema.load(incoming_book_data)

print(book)