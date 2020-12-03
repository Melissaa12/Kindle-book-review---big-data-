from flask import Flask, render_template, request
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
import sys

print('This is the mongo public IP Address' +  sys.arg[2])
mongopublicip = sys.arg[2]
mongopublicipadd = 'http://' + mongopublicip + '/asin/'

print('This is the sql public IP Address' +  sys.arg[1])
sqlpublicip = sys.arg[1]
# from pyspark.ml.feature import CountVectorizer, IDF, Tokenizer
# from pyspark.sql.functions import udf, col
# from pyspark.sql.types import StringType
# from pyspark.mllib.feature import HashingTF
# from pyspark.mllib.feature import IDF
# conf=SparkConf()
# conf.set("spark.driver.memory", "5g")
# sc = SparkContext.getOrCreate(conf)
# sc.setCheckpointDir("hdfs://0.0.0.0:19000/project")
# spark = SparkSession(sc)

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

@app.route('/predict', methods=['POST'])
def search():
   #  ,asin,helpful,overall,reviewText,reviewTime,reviewerID,reviewerName,summary,unixReviewTime

    word = request.form['tfidfword']
    ## csv stored in hadoop 
    ## use sqoop for data ingestion from sql to csv on hadoop
    data = spark.read.csv("hdfs://0.0.0.0:19000/project/kindle_reviews.csv", header=True, sep=",")
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

    def map_to_word1(row, vocab):
      d = {}
      array = row.toArray()
      for i in range(len(row)):
         #check word is not OOV
         if (array[i] != 0):
               tfidf = array[i]
               word = vocab[i]
               d[word] = tfidf
      return str(d)

    def map_to_word(vocab):
      return udf(lambda row: map_to_word1(row, vocab))

    output0 = rescaledData.withColumn("features", map_to_word(vocab)(rescaledData.features))


    output = output0.select("asin","features")
    print(output)
    output.write.format("csv").save("hdfs://0.0.0.0:19000/result")

    #TO DO find most related review and output front end
    



   #  print(type(review_text))

   #  tf=[]
   #  appearance = 0

   #  for i in range(len(review_text)):
   #      if(review_text[i] is not None and word in review_text[i]):
   #          appearance += 1

   #          result = review_text[i].split()
   #          occurence = result.count(word)
   #          reviewLength = len(str(review_text[i]))
   #          tf.append(occurence/reviewLength)
   #  numDocs = len(review_text)
   #  idf = math.log(numDocs/appearance)
   #  tfidf = [x * idf for x in tf]

   #  tdidf_array = np.array(tfidf)
   #  sortedTfidf = tdidf_array.argsort()[-3:][::-1]
   #  print(sortedTfidf)
   #  bookTitle = []
   #  bookReview = []
   #  for i in range (3):
   #      bookTitle.append(review_title[sortedTfidf[i]])
   #      bookReview.append(review_text[sortedTfidf[i]])
   #  print(bookTitle)
   #  print(bookReview)
    return render_template('tfidfresult.html', data="placeholder")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)