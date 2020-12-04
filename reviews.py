#no,asin,helpful,overall,reviewText,reviewTime,reviewerID,reviewerName,summary,unixReviewTime
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import string
from flask_restful import Resource, request, reqparse
import html
#from data import getValues
import csv
from app import returnIPs

mongopublicip, sqlpublicip, port = returnIPs()
#connection = mysql.connector.connect(host='localhost', database='books', user='root', password='catch223')
connection = mysql.connector.connect(host=sqlpublicip, port = port, database='books', user='admin', password='bookreviewer')
connection.autocommit = False

class GetReviewData(Resource):

    def dictfetchall(self,cursor):        #helper function - Returns all rows from a cursor as a list of dicts
 
        desc = cursor.description

        return [dict(zip([col[0] for col in desc], row)) 
                for row in cursor.fetchall()]

    def get(self, asin):

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
        cursor = connection.cursor()
        query = "SELECT asin, reviewText FROM kindle WHERE reviewerID = '%s'" % (r_id)
        cursor.execute(query)
        results = dictfetchall(cursor)
        all_review_data = []
        #for i in results:
           # asin = i.get('asin')
            #reviewText = i.get('reviewText')
            #imgUrl, overview, ab = getValues(asin)
            #all_review_data.append((reviewText))
        #print(all_review_data)
        cursor.close()
        #connection.close()
        return all_review_data

    def totalReviews(self):
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

def create_query(title, summary, genre, rating, review):
    query = ''
    query = "INSERT INTO kindle (idx, asin, overall, reviewText, summary, reviewerID) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (None ,'ABC45678', rating, review, summary, 'A1F6404F1VG29J')
    return query,values    
    

#c1 = GetReviewData()
#c1.put("INSERT INTO kindle (idx, asin, overall, reviewText, summary, reviewerID) VALUES (%s, %s, %s, %s, %s, %s)",(999999, 'ABC45678', '5', 'review', 'summary', 'A1F6404F1VG29J'))
#print(c1.get('ABC45678'))
#print(c1.get('B00E8JE8DE'))
#c1.getAllReviews('A1F6404F1VG29J')
insert_query, values = create_query('titletest', 'summartesty', 'genre', '5', 'testreview')
#print(insert_query,values)
r = GetReviewData()
#print('hello')
#r.put(insert_query,values)
#print("inserted")
#print(r.get('ABC45678'))
#print("retrieved")
r.totalReviews()