from flask import Flask, render_template, request, redirect,url_for, flash, session, json
from flask_restful import Api, Resource, reqparse, request
import jinja2
from flask import json
from bson.json_util import dumps, default
from random import random
import pymongo
from urllib.parse import unquote
import html
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import string
import csv
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import quote
import sys
import numpy as np
import pandas as pd
import math 
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql.session import SparkSession
from pyspark.ml.feature import CountVectorizer, IDF, Tokenizer
from pyspark.sql.functions import udf, col, mean
from pyspark.sql.functions import length
from pyspark.mllib.feature import HashingTF
from pyspark.sql.types import StringType
conf=SparkConf()
masternodeip = sys.argv[3]
conf.set("spark.driver.memory", "5g")
sc = SparkContext.getOrCreate(conf)
sc.setCheckpointDir("hdfs://"+masternodeip+':9000'+"/project")
spark = SparkSession(sc)

port='3306'

print('This is the mongo public IP Address' +  sys.argv[2])
mongopublicip = sys.argv[1]
mongopublicipadd = 'http://' + mongopublicip + ":" + port

print('This is the sql public IP Address' +  sys.argv[1])
sqlpublicip = sys.argv[2]

# mongopublicip = '54.221.99.204'
# sqlpublicip = '3.80.241.110'


app = Flask(__name__)
api = Api(app)

class GetBookDetails():
    #Returns book details based on asin

    def __init__(self, mongoip, port):
        self.mongoip = mongoip
        self.port = port
    
    def getValues(self, asin):

        try:
            #r = requests.get('http://3.238.100.151:3306/asin/'+asin)
            r =  requests.get("http://"+ self.mongoip + ":" + self.port + "/asin/" + asin)
            imgUrl = r.text.strip().split("####")[0]
            if imgUrl == 'NOIMAGE' or imgUrl == 'NOTAVALIABLE':
                imgUrl = 'static/default_book.png'
            overview = r.text.strip().split("####")[1]
            ab = r.text.strip().split("####")[2]
            ab = ab.strip("]").strip("[").strip().split(",")
            ab = [i.strip().strip("u'").strip("'") for i in ab]
            #overview = unquote(overview)
            overview = html.unescape(overview)
            return imgUrl, overview, ab

        except Exception as e:
                print("Unable to connect to MongoDB: {}".format(e))

    def insertLog(self,log):
        #insert log into Mongodb
        #http://54.91.81.131:3306/log?code=200&method=GET&function=reviews&time=12000

        insert_values = {}
        insert_values['code'] = log[0]
        insert_values['method'] = log[1]
        insert_values['function'] = log[2]
        insert_values['time'] = log[3]
        r = requests.get("http://"+ self.mongoip + ":" + self.port + "/log", params = insert_values)
        print("done")

    def addBook(self, author, time, title, overview ):
        #add new book into mongodb
        #http://34.235.169.17:3306/addbook?author=supp&time=1021&title=yodawg&overview=adogdied
    
        new_book = {}
        new_book['author'] = author
        new_book['time'] = time
        new_book['title'] = title
        new_book['overview'] = overview

        r =  requests.get("http://"+ self.mongoip + ":" + self.port + "/addbook", params = new_book)
        print("book inserted")

    def getTitles(self):
        #get all titles from mongodb
        
        url = "http://" + self.mongoip + ":" + self.port + "/titles"
        html = urlopen(url).read()
        soup = BeautifulSoup(html, features="html.parser")

        # get text
        text = soup.get_text()
        titles = text.split('####')

        return titles

    def getRandom(self):
        #get random books for display on front page
        url = "http://" + self.mongoip + ":" + self.port + "/rando"
        html = urlopen(url).read()
        soup = BeautifulSoup(html, features="html.parser")

        # get text
        text = soup.get_text()
        random_books = text.split('####')

        book_display = []
        for book in random_books:
            image, overview, recommended = self.getDetails(book)
            book_display.append((image, overview, book))
            
        return book_display

    def searchTitle(self,title):
        #search book in mongodb based on title
        r =  requests.get("http://"+ self.mongoip + ":" + self.port + "/title/" + title)
        imgUrl = r.text.strip().split("####")[0]
        overview = r.text.strip().split("####")[1]
        ab = r.text.strip().split("####")[2]
        ab = ab.strip("]").strip("[").strip().split(",")
        ab = [i.strip().strip("u'").strip("'") for i in ab]
        overview = unquote(overview)
        overview = html.unescape(overview)
        return imgUrl, overview, ab

    def searchAuthor(self,title):
        #search book in mongodb based on author
        r =  requests.get("http://"+ self.mongoip + ":" + self.port + "/author/" + title)
        imgUrl = r.text.strip().split("####")[0]
        overview = r.text.strip().split("####")[1]
        ab = r.text.strip().split("####")[2]
        ab = ab.strip("]").strip("[").strip().split(",")
        ab = [i.strip().strip("u'").strip("'") for i in ab]
        overview = unquote(overview)
        overview = html.unescape(overview)
        return imgUrl, overview, ab
    
    def sortGenre(self, genre):
        #sort by genre and return book asins
        #http://54.85.36.63:3306/genre?genre=Books
        #r = requests.get('http://3.238.100.151:3306/asin/'+asin)
        genres={}
        genres['genre'] = genre
        r = requests.get("http://"+ self.mongoip + ":" + self.port + "/genre", params = genres)
        asins = r.text.strip().split("####")
        asins = html.unescape(asins)
        asins = [i.strip().strip("\n").strip("'") for i in asins]
        return asins

    def getDetails(self, asin):

        #get book details based on asin
        default_image = 'static/default_book.png'
        default_overview = 'Overview not available.'
        default_recommended = 'Recommended not available'

        
        data = self.getValues(asin)

        if data != None:
            image, overview, recommended = data[0], data[1], data[2]
            return (image or default_image, overview or default_overview, recommended or default_recommended)

        else:
            return ([default_image, default_overview, default_recommended])  

    
    def get(self, asin):
        #get book details alogn with recommended book details
        default_image = 'static/default_book.png'
        default_overview = 'Overview not available.'
        default_recommended = 'Recommended not available'

        image, overview, recommended = self.getDetails(asin)
        recommended_images_overviews = []
        for i in range(min(4,len(recommended))):

            book = recommended[i]
            #print(book)
            r_image, r_overview, r_recommended = self.getDetails(book)
            recommended_images_overviews.append((r_image, r_overview, book))

        #print(image, overview, recommended_images_overviews or default_recos)
        return (image or default_image, overview or default_overview, recommended_images_overviews or default_recommended)

    

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
        #get review data ffrom mysql from asin
        connection = self.connectMysql()

        try:
            cursor = connection.cursor()
            query = "SELECT * FROM kindle WHERE asin = '%s'" % (asin)
            cursor.execute(query)
            results = self.dictfetchall(cursor)
            default_ratings = 0
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
        #add review with log
        connection = self.connectMysql()

        try:
            cursor = connection.cursor()
            cursor.execute(insert_query,values)
            connection.commit()
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            log = (200, 'PUT', 'addreview', current_time)
            c = GetBookDetails(mongopublicip, port)
            c.insertLog(log)
            return {"Message": "Inserted"}, 200

        except Exception as e:
            connection.rollback()
            print("Failed to update record to database rollback: {}".format(e))

        finally:
            cursor.close()
            print("Cursor is closed")

    def getAllReviews(self,r_id):
        #get all reviews for user
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
            all_review_data.append((imgUrl, reviewText, asin))
        #print(all_review_data)
        cursor.close()
        #connection.close()
        return all_review_data

    def totalReviews(self):
        #get all reviews and write into csv
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
    review = GetReviewData(sqlpublicip, port)
    reviews = review.getAllReviews(r_id = 'A1UG4Q4D3OAH3A')
    book = GetBookDetails(mongopublicip, port)
    bookdisplay = book.getRandom()
    genretype = request.args.get('genretype')
    if genretype:
        bookdisplay = book.sortGenre()

    #print(reviews)
    return render_template('index.html',reviews=reviews, book_display = bookdisplay)
    #return render_template('index3.html')

@app.route('/search', methods=['GET'])
def search():
    search_value = request.args.get('searchvalue') 
    search_option = request.args.get('searchoption')
    print(search_option,  search_value)
    search_results = (None, None, None)

    if search_option == 'Title':
        title = quote(search_value)
        book = GetBookDetails(mongopublicip, port)
        search_results = book.searchTitle(title)

    elif search_option == 'Author':
        author = quote(search_value)
        book = GetBookDetails(mongopublicip, port)
        search_results = book.searchAuthor(author)

    if search_results[0] == 'NOIMAGE':
        search_results[0] = 'static/default_book.png'

    return render_template('search.html', search = search_results)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    title = request.args.get('booktitle') 
    author = request.args.get('author') 
    time = current_time 
    overview = request.args.get('summary') 

    if author and time and title and overview:
        print("ok")
        author = quote(author)
        time = quote(time)
        title = quote(title)
        overview = quote(overview)
        book = GetBookDetails(mongopublicip, port)
        book.addBook(author, time, title, overview)
        return redirect('/')

    return render_template('addNewBook.html')

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
    values = (None,'ABC45678', rating, review, summary, 'A1UG4Q4D3OAH3A')
    print('query created')
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

    title,summary,genre,rating,review = getArgs()

    if title and summary and genre and rating and review:
        print("ok")
        insert_query, values = create_query(title,summary,genre,rating,review)
        print(insert_query,values)
        review = GetReviewData(sqlpublicip,port)
        review.put(insert_query,values)
        print("inserted \n")
        return redirect('/')
    
    book = GetBookDetails(mongopublicip,port)
    titles = book.getTitles()
    return render_template('addReview.html', titles = titles) 

@app.route('/correlation')
def correlation():
   return render_template('correlation.html')

@app.route('/tf-idf')
def tf_idf():
   return render_template('tf-idf.html')

@app.route('/corr-calculate',methods=['POST'])
def corr():
   #1. extract asin and review text AND CREATE NEW COLUMN REVIEWLENGTH
   reviews_df = spark.read.csv("hdfs://"+masternodeip+':9000'+"/project"+"/kindle_reviews.csv", header=True, sep=",")
   reviews = reviews_df.select("asin","reviewText")
   reviews = reviews.withColumn("reviewText", length(reviews.reviewText))
   reviews_avg = reviews.groupBy("asin").agg(mean("reviewText").alias("average_reviewLength"))

   print(reviews_avg.head(5))
   #2. extract asin and price
   price_df = spark.read.csv("hdfs://"+masternodeip+':9000'+"/project"+"/mongo_price_asin.csv", header=True, sep=",")

#    #3. join based on asin
   combined_table = price_df.join(reviews_avg, price_df.asin == reviews_avg.asin)
   combined_table = combined_table.drop('asin')
   data = combined_table.filter(col("price").isNotNull() & col("average_reviewLength").isNotNull())		# drop None values

   print(data.head(5))

#    #4. preprocess data
   rdd = data.rdd.map(list)
   rdd.take(5)
   n = rdd.count()
   x = rdd.map(lambda x: float(x[0])).sum()
   y = rdd.map(lambda x: x[1]).sum()
   xy = rdd.map(lambda x: float(x[0]) * x[1]).sum()
   xx = rdd.map(lambda x: float(x[0])**2).sum()
   yy = rdd.map(lambda x: x[1]**2).sum()
   #5. corr 
   numerator = xy - (x * y)/n
   denominator = math.sqrt(xx - (x * x)/n) * math.sqrt(yy - (y * y)/n)
   correlation = numerator / denominator
   print("The Pearson Correlation between price and average review length is: ")
   print(correlation)

   return render_template('tfidfresult.html', data="The pearson Correlation between price and average review length is: " + str(correlation))

@app.route('/predict', methods=['POST'])
def searchda():
   #  ,asin,helpful,overall,reviewText,reviewTime,reviewerID,reviewerName,summary,unixReviewTime

    wordR = request.form['tfidfword']
    data = spark.read.csv("hdfs://"+masternodeip+':9000'+"/project"+"/kindle_reviews.csv", header=True, sep=",")
    data = data.na.drop(subset=["reviewText"])
   
    tokenizer = Tokenizer(inputCol="reviewText",outputCol="words")
    wordsData = tokenizer.transform(data)

    cv = CountVectorizer(inputCol="words", outputCol="rawFeatures",vocabSize = 2000)
    model = cv.fit(wordsData)
    featurizedData = model.transform(wordsData)
    vocab = model.vocabulary

    idf = IDF(inputCol= "rawFeatures", outputCol="features")
    idfModel = idf.fit(featurizedData)
    rescaledData = idfModel.transform(featurizedData)
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

    def map_to_word1(row, vocab):
      d = {}
      array = row.toArray()

      for i in range(len(row)):
         if (array[i] != 0):
               tfidf = array[i]
               word = vocab[i]
               d[word] = tfidf
      return str(d)

    def map_to_word(vocab):
      if wordR in vocab:
         return udf(lambda row: searchFunc(row, vocab, wordR))
      else:
         return udf(lambda row: map_to_word1(row, vocab))

    output0 = rescaledData.withColumn("features", map_to_word(vocab)(rescaledData.features))
    output = output0.select("asin","features")
    output.write.format("csv").save("hdfs://"+masternodeip+':9000'+"/project"+"/result2")

    return render_template('tfidfresult.html', data="The tfidf values for each documents are shown in the terminal. If input word does not exist in dictionary, all tf-idf score will be displayed. Else, tf-idf score of input word will be shown for each document. You can find the result in the /result2 directory by typing hdfs dfs -ls /result2 and hdfs dfs -cat [file-name] to read the csv files")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3306)