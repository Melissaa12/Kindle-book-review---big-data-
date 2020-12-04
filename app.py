from flask import Flask, render_template, request, redirect,url_for, flash
from flask_restful import Api, Resource, reqparse
import json
import jinja2

import sys


def returnIPs():
    #print('This is the mongo public IP Address' +  sys.argv[2])
    #mongopublicip = sys.argv[1]
    #mongopublicipadd = 'http://' + mongopublicip + '/asin/'

    #print('This is the sql public IP Address' +  sys.argv[1])
    #sqlpublicip = sys.argv[2]

    mongopublicip = '54.198.27.228'
    sqlpublicip = '34.230.26.152'
    port=3306

    return mongopublicip, sqlpublicip, port



app = Flask(__name__)
api = Api(app)

from data import GetBookDetails
from reviews import GetReviewData

@app.route('/', methods=['GET'])
def index_page_landing():
    r = GetReviewData()
    reviews = r.getAllReviews(r_id = 'A1F6404F1VG29J')
    return render_template('index.html',reviews=reviews)
    #return render_template('index3.html')


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
    values = (999999,'ABC45678', rating, review, summary, 'A1F6404F1VG29J')
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
    app.run(debug=True)