from flask import json
from flask_restful import Resource, request, reqparse
#from common.util import mongo
from bson.json_util import dumps, default
from random import random
import pymongo
from urllib.parse import unquote
import html

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["metadata"]
mycol = mydb["metada"]

import requests

def getValues(asin):

    r =requests.get('http://3.238.71.18:3306/asin/'+asin)
    imgUrl = r.text.strip().split("####")[0]
    overview = r.text.strip().split("####")[1]
    ab = r.text.strip().split("####")[2]
    ab = ab.strip("]").strip("[").strip().split(",")
    ab = [i.strip().strip("u'").strip("'") for i in ab]
    #overview = unquote(overview)
    overview = html.unescape(overview)
    return imgUrl, overview, ab

#print(getValues('B00HZNSXHW'))

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
        #data = getValues(asin)

        if data != None:
            #image, overview, recommended = data[0], data[1], data[2]
            image = data.get('imUrl')
            overview = data.get('description')
            recommended = data.get('related', {}).get('also_bought')
        else:
            return (["Not available","Not available","Not available"])
        #print(recommended)

        return (image or default_image, overview or default_overview, recommended or default_recommended)

class GetBookDetails(Resource):
    #Returns book details based on asin
    
    def get(self, asin):
        try:
            image, overview, recommended = getDetails(asin)
            default_recos = "No recs"
            recommended_images_overviews = []
            for i in range(min(4,len(recommended))):
                book = recommended[i]
                r_image, r_overview, r_recommended = getDetails(book)
                recommended_images_overviews.append((r_image, r_overview, book))

            #print(image, overview, recommended_images_overviews or default_recos)
            return (image, overview, recommended_images_overviews or default_recos)
        
        except:
            return {"Message": "Failed to retrieve data"}, 500

#print(getDetails('B00HZNSXHW'))
c = GetBookDetails()
print(c.get('B000F83TEQ'))

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
