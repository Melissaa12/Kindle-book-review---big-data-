from flask import Flask, render_template, request, redirect,url_for, flash
from flask_restful import Api, Resource, reqparse
import json
import jinja2
from flask import json
from flask_restful import Resource, request, reqparse
from bson.json_util import dumps, default
from random import random
import pymongo
from urllib.parse import unquote
import html
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import string
import html
import csv
import requests
import sys

import numpy as np
import pandas as pd
import math 
import sys
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql.session import SparkSession
from pyspark.ml.feature import CountVectorizer, IDF, Tokenizer
from pyspark.sql.functions import udf, col
from pyspark.mllib.feature import HashingTF
from pymongo import MongoClient
from pyspark.sql.types import StringType
from pyspark.sql.functions import *
from pyspark.sql.functions import length
conf=SparkConf()
conf.set("spark.driver.memory", "5g")
sc = SparkContext.getOrCreate(conf)
sc.setCheckpointDir("hdfs://"+masternodeip+':9000:'+"/project")
spark = SparkSession(sc)

masternodeip = sys.argv[3]
print('This is the mongo public IP Address' +  sys.argv[2])
mongopublicip = sys.argv[1]
mongopublicipadd = 'http://' + mongopublicip + '/asin/'

print('This is the sql public IP Address' +  sys.argv[1])
sqlpublicip = sys.argv[2]

# mongopublicip = '54.198.27.228'
# sqlpublicip = '34.230.26.152'
# port=3306

app = Flask(__name__)
api = Api(app)

class GetBookDetails():
    #Returns book details based on asin

    def __init__(self, mongoip, port):
        self.mongoip = mongoip
        self.port = port
    
    def getValues(self, asin):

        try:
            #r = requests.get('http://54.198.27.228:3306/asin/'+asin)
            r =  requests.get("http://"+ self.mongoip + ":" + str(port) + "/asin/" + asin)
            imgUrl = r.text.strip().split("####")[0]
            overview = r.text.strip().split("####")[1]
            ab = r.text.strip().split("####")[2]
            ab = ab.strip("]").strip("[").strip().split(",")
            ab = [i.strip().strip("u'").strip("'") for i in ab]
            #overview = unquote(overview)
            overview = html.unescape(overview)
            return imgUrl, overview, ab

        except Exception as e:
                print("Unable to connect to MongoDB: {}".format(e))

    def getDetails(self, asin):


        default_image = '/static/purple.jpg'
        default_overview = 'Overview not available.'
        default_recommended = 'Recommended not available'

        try:
            #cursor = mycol.find_one({"asin": asin})
            #jsonstring = dumps(cursor, default=default)
            #data = json.loads(jsonstring)
            data = self.getValues(asin)

            if data != None:
                image, overview, recommended = data[0], data[1], data[2]
                return (image or default_image, overview or default_overview, recommended or default_recommended)

            else:
                return (["Not available","Not available","Not available"])  

        except Exception as e:
            print("Unable to retrieve data: {}".format(e))
    
    def get(self, asin):
        try:
            image, overview, recommended = self.getDetails(asin)
            default_recos = "No recs"
            recommended_images_overviews = []
            for i in range(min(4,len(recommended))):
                book = recommended[i]
                #print(book)
                r_image, r_overview, r_recommended = self.getDetails(book)
                recommended_images_overviews.append((r_image, r_overview, book))

            #print(image, overview, recommended_images_overviews or default_recos)
            return (image, overview, recommended_images_overviews or default_recos)
        
        except:
            return {"Message": "Failed to retrieve data"}, 500
class GetReviewData():

    def __init__(self, sqlip, port):
        self.sqlip = sqlip
        self.port = port
    
    def connectMysql(self):
        connection = mysql.connector.connect(host=self.sqlip, port = self.port, database='books', user='admin', password='bookreviewer')
        connection.autocommit = False
        return connection

    def dictfetchall(self,cursor):        #helper function - Returns all rows from a cursor as a list of dicts
 
        desc = cursor.description

        return [dict(zip([col[0] for col in desc], row)) 
                for row in cursor.fetchall()]

    def get(self, asin):

        connection = self.connectMysql()

        try:
            cursor = connection.cursor()
            query = "SELECT * FROM kindle WHERE asin = '%s'" % (asin)
            cursor.execute(query)
            results = self.dictfetchall(cursor)
            default_ratings = 'No Ratings'
            default_reviews = []
            ratings = []
            username_reviews = []
            
            for i in results:
                ratings.append(i.get('overall'))
                username_reviews.append((i.get('reviewerName'), i.get('overall'), html.unescape(i.get('reviewText'))))
                
            if len(ratings)!= 0:
                avg_rating = round((sum(ratings)/len(ratings)),1)
            else:
                avg_rating = 0

            return avg_rating or default_ratings, username_reviews or default_reviews


        except Exception as e:
            print(e)
            return {"message": "Something goes wrong"}, 500

        finally:
            cursor.close()
            print("Cursor is closed")

    def put(self, insert_query, values):

        connection = self.connectMysql()

        try:
            cursor = connection.cursor()
            cursor.execute(insert_query,values)
            
            connection.commit()
            return {"Message": "Inserted"}, 200

        except Exception as e:
            connection.rollback()
            print("Failed to update record to database rollback: {}".format(e))

        finally:
            cursor.close()
            print("Cursor is closed")

    def getAllReviews(self,r_id):
        connection = self.connectMysql()
        print("connected")
        cursor = connection.cursor()
        query = "SELECT asin, reviewText FROM kindle WHERE reviewerID = '%s'" % (r_id)
        cursor.execute(query)
        results = self.dictfetchall(cursor)
        #print(results)
        all_review_data = []
        for i in results:
            asin = i.get('asin')
            reviewText = i.get('reviewText')
            r = GetBookDetails(mongopublicip, port)
            imgUrl, overview, ab = r.getValues(asin)
            all_review_data.append((imgUrl, reviewText))
        print(all_review_data)
        cursor.close()
        #connection.close()
        return all_review_data

    def totalReviews(self):

        connection = self.connectMysql()
        try:
            cursor = connection.cursor()
            query = "SELECT asin, reviewText FROM kindle"
            cursor.execute(query)
            results = cursor.fetchall()
            
            fp = open('/Users/varsha/Desktop/asin_review.csv', 'w')
            myFile = csv.writer(fp)
            myFile.writerows(results)
            fp.close()
            print("Completed")

        except Exception as e:
            print("Unable to get data: {}".format(e))

        finally:
            cursor.close()


@app.route('/', methods=['GET'])
def index_page_landing():
    r = GetReviewData(sqlpublicip,port)
    reviews = r.getAllReviews(r_id = 'A1UG4Q4D3OAH3A')
    #print(reviews)
    return render_template('index.html',reviews=reviews)
    #return render_template('index3.html')


@app.route('/book/<string:asin>')
def hello_world(asin):
   #api.add_resource(BookDetail,'/book/<string:asin>')
   reviews = []
   c = GetBookDetails(mongopublicip,port)
   image, overview, recommended = c.get(asin)
   r = GetReviewData(sqlpublicip,port)
   rating, reviews = r.get(asin)
   print(reviews)
   return render_template('book.html', img = image, overview = overview, recommended = recommended, avg_rating = rating, reviews = reviews)
   #overview = data["description"]

def create_query(title, summary, genre, rating, review):
    query = ''
    query = "INSERT INTO kindle (idx, asin, overall, reviewText, summary, reviewerID) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (None,'ABC45678', rating, review, summary, 'A1F6404F1VG29J')
    return query,values


def getArgs():
    

    title = request.args.get('booktitle') 
    summary = request.args.get('summary') 
    genre = request.args.get('genre') 
    rating = request.args.get('inlineRadioOptions') 
    review = request.args.get('review') 
    return (title,summary,genre,rating,review)

@app.route('/add-review',methods =["GET","POST"])
def add_review():

    default_title = "NO TITLE"
    default_summary = "NO SUMMARY"
    default_genre = "NO GENRE"
    defult_rating = "0"
    default_review = "NO REVIEW"

    title,summary,genre,rating,review = getArgs()

    if title and summary and genre and rating and review:
        insert_query, values = create_query(title,summary,genre,rating,review)
        print(insert_query)
        r = GetReviewData(sqlpublicip,port)
        r.put(insert_query,values)
        print("inserted \n")
        return redirect('/')


    #title = request.args.get('booktitle') or default_title
    #summary = request.args.get('summary') or default_summary
    #genre = request.args.get('genre') or default_genre
    #rating = request.args.get('inlineRadioOptions') or defult_rating
    #review = request.args.get('review') or default_review

    #review = request.args.get('review')
    #print(title,genre,image,rating,review)
    

    return render_template('addReview.html') 


@app.route('/predict', methods=['POST'])
def search():
   # df = totalReviews()
   
   # ,asin,helpful,overall,reviewText,reviewTime,reviewerID,reviewerName,summary,unixReviewTime

   # wordR = request.form['tfidfword']
   data = spark.read.csv("hdfs://"+masternodeip+':9000:'+"/project/kindle_reviews.csv", header=True, sep=",")
   data = data.na.drop(subset=["reviewText"])

   tokenizer = Tokenizer(inputCol="reviewText",outputCol="words")
   wordsData = tokenizer.transform(data)

   cv = CountVectorizer(inputCol="words", outputCol="rawFeatures",vocabSize = 2000)
   model = cv.fit(wordsData)
   featurizedData = model.transform(wordsData)
   vocab = model.vocabulary

   idf = IDF(inputCol= "rawFeatures", outputCol="features")
   idfModel = idf.fit(featurizedData)
   resultData = idfModel.transform(featurizedData)
   tfidfRow=[]
   #get tfidf of each row
   def searchFunc (row,vocab,req):
      a = {}
      index = vocab.index(req)
      array = row.toArray()
      tfidfWord = 0
      for i in range(len(row)):
         if (array[i]!=0  ):
            tfidf=array[i]
            word= vocab[i]
            if(word==req):
            # print(tfidf)
               tfidfWord = tfidf
               a[word]= tfidf
      tfidfRow.append(tfidfWord)
      return str(a)

   def searchFunc1(row, vocab):
      d = {}
      array = row.toArray()
      # print(array[0])
      # print(vocab[0])
      # print(array[1])
      # print(vocab[1])
      for i in range(len(row)):
         if (array[i] != 0):
            tfidf = array[i]
            word = vocab[i]
            d[word] = tfidf
      return str(d)

   def map_to_word(vocab):
      return udf(lambda row: searchFunc1(row, vocab))
      # return udf(lambda row: searchFunc(row, vocab, wordR))

   output0 = resultData.withColumn("features", map_to_word(vocab)(resultData.features))
   output = output0.select("asin","reviewerID","features")
   output.write.format("csv").save("hdfs://"+masternodeip+':9000:' + "/result7")

   return render_template('tfidfresult.html', data="placeholder")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3306)