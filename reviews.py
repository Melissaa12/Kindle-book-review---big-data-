import mysql.connector
import string
from flask_restful import Resource, request, reqparse
import html
from data import getValues
import csv


#no,asin,helpful,overall,reviewText,reviewTime,reviewerID,reviewerName,summary,unixReviewTime

#connection = mysql.connector.connect(host='localhost', database='books', user='root', password='catch223')
connection = mysql.connector.connect(host='3.238.96.79', port = 3306, database='books', user='admin', password='bookreviewer')




cursor = connection.cursor()

def dictfetchall(cursor):        #helper function to get query results in dictionary
    """Returns all rows from a cursor as a list of dicts"""
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall()]


class GetReviewData(Resource):
    def get(self, asin):

        cursor = connection.cursor()

        try:
            query = "SELECT * FROM kindle WHERE asin = '%s'" % (asin)
            cursor.execute(query)
            results = dictfetchall(cursor)
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

        #finally:
            #cursor.close()
            #connection.close()

    def put(self, insert_query, values):
        cursor.execute(insert_query,values)
        return {"inserted"}, 500

    def getAllReviews(self,r_id):
        query = "SELECT asin, reviewText FROM kindle WHERE reviewerID = '%s'" % (r_id)
        cursor.execute(query)
        results = dictfetchall(cursor)
        all_review_data = []
        for i in results:
            asin = i.get('asin')
            reviewText = i.get('reviewText')
            imgUrl, overview, ab = getValues(asin)
            all_review_data.append((reviewText))
        #print(all_review_data)
        return all_review_data
    
    

c1 = GetReviewData()
c1.put("INSERT INTO kindle (idx, asin, overall, reviewText, summary, reviewerID) VALUES (%s, %s, %s, %s, %s, %s)",(999999,'ABC45678', '5', 'review', 'summary', 'A1F6404F1VG29J'))
print(c1.get('ABC45678'))
#print(c1.get('B00E8JE8DE'))
#c1.getAllReviews('A1F6404F1VG29J')


def totalReviews():
        cursor = connection.cursor()
        query = "SELECT asin, reviewText FROM kindle"
        cursor.execute(query)
        results = cursor.fetchall()
        
        fp = open('/Users/varsha/Downloads/DBProject-main-2/asin_review.csv', 'w')
        myFile = csv.writer(fp)
        myFile.writerows(results)
        fp.close()
        cursor.close()
        connection.close()
        
        return ("Completed")

#totalReviews()