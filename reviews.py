import mysql.connector
import string
from flask_restful import Resource, request, reqparse
import html


#no,asin,helpful,overall,reviewText,reviewTime,reviewerID,reviewerName,summary,unixReviewTime

#connection = mysql.connector.connect(host='localhost', database='books', user='root', password='catch223')
connection = mysql.connector.connect(host='34.239.153.54', port = 3306, database='books', user='admin', password='bookreviewer')




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

    def put(self,insert_query,values):
        cursor.execute(insert_query,values)
        return {"inserted"}, 500

#c1 = GetReviewData()
#c1.get('B000F83SZQ')