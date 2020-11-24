from flask import json
from flask_restful import Resource, request, reqparse
#from common.util import mongo
from bson.json_util import dumps, default
from random import random
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["metadata"]
mycol = mydb["metada"]

#mydb2 = myclient["kindle"]mycol = mydb["books"]

#x = mycol.find_one()

#print(x)
def getDetails(asin):

        default_image = '/static/purple.jpg'
        default_overview = 'Overview not available.'
        default_recommended = 'Recommended not available'

        cursor = mycol.find_one({"asin": asin})
        jsonstring = dumps(cursor, default=default)
        data = json.loads(jsonstring)
            
        image = data.get('imUrl')
        overview = data.get('description')
        recommended = data.get('related', {}).get('also_bought')
        #print(recommended)

        return (image or default_image, overview or default_overview, recommended or default_recommended)

class GetBookTitles(Resource):
    #Returns all book titles
    def get(self):
        try:
            cursor = mycol.find({'title': {'$exists': 1}}, {'_id': 0, 'asin': 1,'title': 1})
            json_query = json.loads(dumps(cursor, default=default))
            return {"message": "Successfully retrieve all titles", "titles": json_query}, 200
        except:
            return {"message": "Failed to retrieve all titles"}, 500

class GetBookDetails(Resource):
    #Returns book details based on asin
    
    def get(self, asin):
        try:
            image, overview, recommended = getDetails(asin)
            #print(recommended)
            #print(overview)
            limit = 0
            default_recos = "No recs"
            recommended_images_overviews = []
            #index, item in zip(range(limit), items):
            for index, book in zip(range(4), recommended):
                #limit +=1
                #print(index, book), "\n"
                r_image, r_overview, r_recommended = getDetails(book)
                recommended_images_overviews.append((r_image, r_overview, book))
                #if limit == 2:
                    #break
                #print(recommended_images_overviews, "\n")
            #print(image, overview, recommended_images_overviews)
            return (image, overview, recommended_images_overviews or default_recos)
        
        except:
            return {"Message": "Failed to retrieve data"}, 500

c = GetBookDetails()
print(c.get('B000F83SZQ'))

class RegisterNewBook(Resource):
    #Add new book

    def generate_asin(self):
        random_int = int(random() * 10000000000)
        int2str = str(random_int)
        return int2str.zfill(10)

    def post(self):
        try: 
            _title = req_json['title']
            _imUrl = req_json['imUrl']
            _description = req_json['description']
        except Exception as e:
            print(e)
            return {"message": "title, imUrl and description are required fields"}, 400

        _price = round(float(req_json.get('price')),2)
        _categories = req_json.get('categories')
        _related = req_json.get('related')
        _asin = self.generate_padded_number()

        field_names = ['asin', 'title', 'imUrl', 'description', 'price', 'categories', 'description', 'related']
        fields = [_asin, _title, _imUrl, _description, _price, [_categories], _description, _related]
        query = self.get_filled_fields(field_names, fields)
        try:
            metadata.insert_one(query)
            return {"message": "Book registered", "body": json.loads(dumps(query))}, 200
            
        except Exception as e:
            print(e)
            return {"message": "Server Error"}, 500
