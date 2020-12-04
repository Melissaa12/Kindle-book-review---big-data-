from flask import Flask, render_template, request, redirect,url_for, flash
from flask_restful import Api, Resource, reqparse
import json
import jinja2
from data import GetBookDetails
from reviews import GetReviewData
import numpy as np
import pandas as pd
import math 
import sys
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql.session import SparkSession
from pyspark.ml.feature import CountVectorizer, IDF, Tokenizer
from pyspark.sql.functions import udf
from pyspark.mllib.feature import HashingTF

print('This is the mongo public IP Address' +  sys.argv[2])
mongopublicip = sys.argv[1]
mongopublicipadd = 'http://' + mongopublicip + '/asin/'
from pyspark.ml.feature import CountVectorizer, IDF, Tokenizer
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StringType
from pyspark.mllib.feature import HashingTF
from pyspark.sql.functions import *
from pyspark.sql.functions import length
conf=SparkConf()
conf.set("spark.driver.memory", "5g")
sc = SparkContext.getOrCreate(conf)
masternodeip = sys.argv[3]

sc.setCheckpointDir("hdfs://"+masternodeip+':9000:'+"/project")
spark = SparkSession(sc)

app = Flask(__name__)
@app.route('/', methods=['GET'])
def index_page_landing():
    return render_template('index.html')
@app.route('/book')
def hello_world():
   return render_template('book.html')
@app.route('/add-review')
def add_review():
   return render_template('addReview.html')
@app.route('/correlation')
def correlation():
   return render_template('correlation.html')
@app.route('/tf-idf')
def tf_idf():
   return render_template('tf-idf.html')
def string_length(reviewText):
    x = len(reviewText)
    return x
print('This is the sql public IP Address' +  sys.argv[1])
sqlpublicip = sys.argv[2]


app = Flask(__name__)
api = Api(app)



@app.route('/', methods=['GET'])
def index_page_landing():
    r = GetReviewData()
    reviews = r.getAllReviews(r_id = 'A1F6404F1VG29J')
    return render_template('index.html',reviews=reviews)
    #return render_template('index3.html')

@app.route('/predict', methods=['POST'])
def search():
   #  ,asin,helpful,overall,reviewText,reviewTime,reviewerID,reviewerName,summary,unixReviewTime

    wordR = request.form['tfidfword']
    data = spark.read.csv("hdfs://"+masternodeip+':9000'+"/project/kindle_reviews.csv", header=True, sep=",")
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
      # return udf(lambda row: map_to_word1(row, vocab))
      return udf(lambda row: searchFunc(row, vocab, wordR))
    output0 = rescaledData.withColumn("features", map_to_word(vocab)(rescaledData.features))
    output = output0.select("asin","features")
    output.write.format("csv").save("hdfs://"+masternodeip+':9000'+"/result2")
    return render_template('tfidfresult.html', data="placeholder")
@app.route('/book/<string:asin>')
def hello_world(asin):
   #api.add_resource(BookDetail,'/book/<string:asin>')
   reviews = []
   c = GetBookDetails()
   image, overview, recommended = c.get(asin)
   r = GetReviewData()
   rating, reviews = r.get(asin)
   print(reviews)
   return render_template('book.html', img = image, overview = overview, recommended = recommended, avg_rating = rating, reviews = reviews)
   #overview = data["description"]

def create_query(title, summary, genre, rating, review):
    query = ''
    query = "INSERT INTO kindle (idx, asin, overall, reviewText, summary, reviewerID) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (999999,0000000, rating, review, summary, 'A1F6404F1VG29J')
    return query,values

@app.route('/add-review',methods =["GET","POST"])
def add_review():

    default_title = "NO TITLE"
    default_summary = "NO SUMMARY"
    default_genre = "NO GENRE"
    defult_rating = "0"
    default_review = "NO REVIEW"

    title = request.args.get('booktitle') or default_title
    summary = request.args.get('summary') or default_summary
    genre = request.args.get('genre') or default_genre
    rating = request.args.get('inlineRadioOptions') or defult_rating
    review = request.args.get('review') or default_review

    #review = request.args.get('review')
    #print(title,genre,image,rating,review)
    insert_query, values = create_query(title, summary, genre, rating, review)
    print(insert_query)
    r = GetReviewData()
    r.put(insert_query,values)
    print("inserted \n")
    print(r.get(0000000))
    return redirect('/')

    return render_template('addReview.html') 

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)