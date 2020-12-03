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

from pyspark.ml.feature import CountVectorizer, IDF, Tokenizer
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StringType
from pyspark.mllib.feature import HashingTF
from pyspark.sql.functions import *
from pyspark.sql.functions import length
conf=SparkConf()
conf.set("spark.driver.memory", "5g")
sc = SparkContext.getOrCreate(conf)
sc.setCheckpointDir("hdfs://0.0.0.0:19000/project")
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
# @app.route('/corr-calculate',methods=['POST'])
# def corr():
#    #1. extract asin and review text AND CREATE NEW COLUMN REVIEWLENGTH
#    reviews_df = spark.read.csv("hdfs://0.0.0.0:19000/project/kindle_reviews.csv", header=True, sep=",")
#    reviews = reviews_df.select("asin","reviewText")
#    reviews = reviews.withColumn("reviewText", length(reviews.reviewText))
#    reviews_avg = reviews.groupBy("asin").agg(mean("reviewText").alias("average_reviewLength"))

#    print(reviews_avg.head(5))

#    #2. extract asin and price
#    price_df = spark.read.csv("hdfs://0.0.0.0:19000/project/kindle_reviews.csv", header=True, sep=",")
#    price = price_df.select("asin","overall")
   
#    #3. join based on asin
#    combined_table = price.join(reviews, price.asin == reviews.asin)
#    combined_table = combined_table.drop('asin')

#    print(combined_table.head(5))

#    #4. preprocess data
#    rdd = combined_table.rdd.map(list)
#    rdd.take(5)
#    n = rdd.count()
#    x_sum = rdd.map(lambda x: x[1]).sum()
#    y_sum = rdd.map(lambda x: x[2]).sum()
#    xy_sum = rdd.map(lambda x: x[1] * x[2]).sum()
#    x_sq_sum = rdd.map(lambda x: x[1]**2).sum()
#    y_sq_sum = rdd.map(lambda x: x[2]**2).sum()
#    #5. corr 
#    numerator = xy_sum - (x_sum * y_sum)/n
#    denominator = math.sqrt(x_sq_sum - (x_sum * x_sum)/n) * math.sqrt(y_sq_sum - (y_sum * y_sum)/n)
#    correlation = numerator / denominator
#    print("The Pearson Correlation between average review length and price is: ")
#    print(correlation)


#    return render_template('tfidfresult.html', data="placeholder")

@app.route('/predict', methods=['POST'])
def search():
   #  ,asin,helpful,overall,reviewText,reviewTime,reviewerID,reviewerName,summary,unixReviewTime

    wordR = request.form['tfidfword']
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
    output.write.format("csv").save("hdfs://0.0.0.0:19000/result2")

    return render_template('tfidfresult.html', data="placeholder")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)