import pymongo
import json as js
from flask import json
from flask_restful import Resource, request, reqparse
from bson.json_util import dumps, default
from random import random
import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/") #Connecting to the local MongoDB database
mydb = myclient["kindle"] #the json file has been imported as a db
metadata = mydb["metadata"] #the collection inside the database
logdb = myclient['logdb'] #this is the database for logging
logdbcol = logdb['logdbcol'] #the collection for the logging database




import flask
app = flask.Flask(__name__)

@app.route('/addbook') #Route to add a new book that takes in parametrs author, title, overview and time, which acts as asin
def addBook():

    try:
#        code=    request.args.get('code')
        overview = request.args.get('overview')
        method = request.args.get('author')
        function = request.args.get('title')
        time = request.args.get('time')
        tempdic = {'asin' : time, 'author' : method , 'title': function , 'description':overview}
        metadata.insert_one(tempdic)
        return 'success'
    except:
        return 'failure in adding'



@app.route('/getlog') #Gets the list of logs made
def getlog():
    tempstring=""
    entries = logdbcol.find()
    for doc in  entries:
        print(doc)

        tempstring+=str({x: doc[x] for x in doc if x not in ['_id']})+'\n'
    return tempstring
    #return doc #dict(logdbcol.find())
@app.route('/' ) #To test if the server is running
def  hello_world():
    return 'Hello World'

@app.route('/log') #To log a new entry, takes in the method, function, time and code
def log():

#(200,POST,addbook,TIMESTAMP)
    try:
        code=    request.args.get('code')
        method = request.args.get('method')
        function = request.args.get('function')
        time = request.args.get('time')
        tempdic = {'code' : code, 'method' : method , 'function': function, 'time':time}
        logdbcol.insert_one(tempdic)
        return 'success'
    except:
        return 'failure in logging: logging cannot make it'


@app.route('/titles')#Returns the list of books with titles
def titles():
    a =metadata.find({}, {'title':1})
    tempstring = ""
    for doc in a:
        if(len(doc.keys())) ==2:
            tempstring+=doc['title']+"####"
        #print(doc[doc.keys()[0]])

    return tempstring
@app.route('/rando') #Returns a list of 30 random asins
def rando():
    tempstring = ""
    a = metadata.aggregate(
       [ { '$sample': { 'size': 30 } } ]
    )
    for doc in a:
         tempstring+=doc['asin']+"####"
#        print(doc)
    print(tempstring)
    return tempstring
@app.route('/<key>/<value>') #The universal search. returns imgurl,overview and also bought for any key/value. eg: asin/B813J3138
def customSearch(key,value):
    temp = []
    #return  value

    for x in metadata.find({key:value}):
        temp.append(x)
    print(len(temp))
    default_overview = 'Overview not available.'
    if(len(temp)==0):
        return "NOTAVAILABLE####NOTAVAILABLE####NOTAVAILABLE"
    temp =temp[0]

    jsonstring = js.dumps(temp, default=default)
    data = json.loads(jsonstring)
    try:
        image = data['imUrl']
    except:
        image = "NOIMAGE"
    print(data)
    try:
        overview = data['description']
    except:
        overview = "NOOVERVIEW"
    try:
        ab = data['related']['also_bought']
        print(ab)
    except:
        ab = "NOALSOBOUGHT"
    print(image, overview)
    return (image  +"####" + overview+"####"+str(ab))
    #except:
     #   return {"Message": "Failed to retrieve data"}, 500

if __name__ == "__main__": #Running on port 3306
    app.run(host = '0.0.0.0' , port=3306)

