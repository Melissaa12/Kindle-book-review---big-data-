from flask import Flask, render_template, request
from flask_restful import Api, Resource, reqparse
import json
import jinja2
from data import GetBookDetails

#data = {'1603420304':{'description': "In less time and for less money than it takes to order pizza, you can make it yourself!Three harried but heatlh-conscious college students compiled and tested this collection of more than 200 tasty, hearty, inexpensive recipes anyone can cook -- yes, anyone!Whether you're short on cash, fearful of fat, counting your calories, or just miss home cooking, The Healthy College Cookbook offers everything you need to make good food yourself.", 'price': 7.69, 'imUrl': 'http://ecx.images-amazon.com/images/I/51IEqPrF%2B9L._BO2,204,203,200_PIsitb-sticker-v3-big,TopRight,0,-55_SX278_SY278_PIkin4,BottomRight,1,22_AA300_SH20_OU01_.jpg', 'related': {'also_viewed': ['B001OLRKLQ', 'B004J35JIC', 'B00505UP8M', 'B004GTLKEQ', 'B005KWMS8U', 'B00BS03TYU', 'B001MT5NXW', 'B00A86JE3K', 'B00D694Y9U', 'B00DSVUVXY', 'B008EN3W6Y', 'B00BS03W5Q', 'B008161J1O', 'B0089LOJH2', 'B00ENSBJYQ', 'B00C7C040U', 'B00DH410VY', 'B00CMVFW4O', 'B00C89GS1Q', 'B0035FZJ9Y', 'B004GTLFUK', 'B00H24WT2E', 'B00CVS44OW', 'B00C5W32QK', 'B00HY0KTPK', 'B00BJ8IPJU', 'B00JEOMV1E', 'B0041KKLNQ', 'B00CVS2JYY', 'B00CTVOVD0', 'B00ET594CC'], 'buy_after_viewing': ['B004J35JIC', 'B0089LOJH2']}, 'categories': [['Books', 'Cookbooks, Food & Wine', 'Quick & Easy'], ['Books', 'Cookbooks, Food & Wine', 'Special Diet'], ['Books', 'Cookbooks, Food & Wine', 'Vegetarian & Vegan', 'Non-Vegan Vegetarian'], ['Kindle Store', 'Kindle eBooks', 'Cookbooks, Food & Wine', 'Quick & Easy'], ['Kindle Store', 'Kindle eBooks', 'Cookbooks, Food & Wine', 'Special Diet', 'Healthy'], ['Kindle Store', 'Kindle eBooks', 'Cookbooks, Food & Wine', 'Vegetables & Vegetarian']]},
        #'B0002IQ15S':{'categories': [['Kindle Store', 'Kindle Accessories', 'Power Adapters', 'Kindle (1st Generation) Adapters']], 'description': "This universal DC adapter powers/charges portable electronic devices such as mobile phones, handhelds/PDAs, digital cameras and MP3 players.  Utilizing interchangeable itips, iGo AutoPower powers/charges virtually all of your portable electronic devices from any standard auto power outlet eliminating the need to carry multiple power adapters when you're mobile.Main FeaturesManufacturer: Mobility Electronics, IncManufacturer Part Number: PS0221-10Manufacturer Website Address: www.mobilityelectronics.comProduct Type: Power AdapterInput Voltage: 11.5 V DC to 16 V DCOutput Power: 15WWeight: 3.6 ozStandard Warranty: 2 Year(s) Limited", 'title': 'Mobility IGO AUTOPOWER 3000 SERIES ( PS0221-10 )', 'price': 19.99, 'salesRank': {}, 'imUrl': 'http://ecx.images-amazon.com/images/I/21QFJM28NGL.jpg', 'related': {'also_viewed': ['B00511PS3C', 'B000PI17MM', 'B0016L6OWK', 'B006BGZJJ4', 'B005DOKHLK', 'B001W1XT6I', 'B003YLMAC8', 'B00EXIGQFS', 'B000QSPO3Y', 'B001W1TZTS', 'B00115PYGS', 'B001W1XT5O', 'B002GJQ7AU', 'B00EOE6COQ', 'B0012J52OC', 'B001007OUI', 'B00F3HH2HY', 'B00CGIVV5C', 'B00GA567M4', 'B002WCCQQA', 'B006GWO5NE', 'B006GWO5WK', 'B007HCCNJU', 'B00BHJRYYS'], 'buy_after_viewing': ['B006GWO5WK', 'B001N2LHHO', 'B006GWO5NE', 'B0012J52OC']}},
        #'B000F83SZQ':{'price': 0.0, 'imUrl': 'http://ecx.images-amazon.com/images/I/51yLqHe%2BFqL._BO2,204,203,200_PIsitb-sticker-v3-big,TopRight,0,-55_SX278_SY278_PIkin4,BottomRight,1,22_AA300_SH20_OU01_.jpg', 'related': {'also_bought': ['B0080H1C0W', 'B00LK4ZKOG', 'B00JZD2PU6', 'B00JPFAXTY', 'B00LK4ZMYE', 'B00LK30NEY', 'B006LABC8M', 'B00L1HYMJQ', 'B00J7X007E', 'B00LG0HL00', 'B00CEL5530', 'B000FA5PUK', 'B00LNLVQ9Y', 'B00KBGI38E', 'B00LDPMLVM', 'B00KVOC68O', 'B00A3N25HK', 'B00K5V449C', 'B006BE4OUG', 'B00H9WPHXM', 'B00D1CPG5I', 'B0084MZWPO', 'B00KL13WXK', 'B00H9ZM782', 'B00AL2AF8O', 'B00D0IPCCK', 'B00JZDM9CA', 'B000FA5LAO', 'B00DDW57NW', 'B00H876DYU', 'B00EI3E0T2', 'B00FN9G0KM', 'B006LAAUHG', 'B00JX7UVFU', 'B00K6H2D5W', 'B00KCA0I96', 'B00JXRCPNG', 'B00CV9I2J4', 'B00L22GJVO', 'B00EZVS8H2', 'B00IVC9IQG', 'B00KOYAQFG', 'B008AD8TFW', 'B0036B955G', 'B00EH3R7WK', 'B004GXB2DG', 'B005HAWAZG', 'B00KVMWJRY', 'B00K6YZ4CY', 'B008CJ1R5S', 'B00ITNWAVM', 'B009PK83IC', 'B00F1MU458', 'B00KUF0KCI', 'B00DRLACCA', 'B002G1ZY4S', 'B00DXO6HR0', 'B0087KGSNI', 'B00HD5XVY2', 'B00ICXDRCU', 'B003XVYGVC', 'B00FY54N72', 'B00HBGISE6', 'B00KBK4USC', 'B007GG9XEU', 'B00AJ1VLOY', 'B00E6EHFN6', 'B00IOYDAEW', 'B00KFOTI72', 'B008RZQYN2', 'B00JRDGZN2', 'B008R8FPFW', 'B00JL62F48', 'B006GRNYFE', 'B00DVL2CVU', 'B00H92XFA4', 'B00IJKQH96', 'B008GNGKIO', 'B00K39Q7ZK', 'B00K00LEOG', 'B00I9FJJWS', 'B00J9SQW56', 'B00BEOZCJU', 'B00EZGSTD0', 'B003YDXMYG', 'B00GZR2NZC', 'B0045UA6F0', 'B00J16SQFU', 'B00DPBNP2Q', 'B00927CLFY', 'B00H3J4L4M', 'B00ICP5JLK', 'B00H4K59DW', 'B003XVYGWQ', 'B00HF7J1P6'], 'buy_after_viewing': ['B006HCTWVS', 'B009FZPMFO', 'B00F1I0C40', 'B00IVC9IQG']}, 'categories': [['Books', 'Literature & Fiction'], ['Books', 'Mystery, Thriller & Suspense', 'Thrillers & Suspense', 'Suspense'], ['Kindle Store', 'Kindle eBooks', 'Mystery, Thriller & Suspense', 'Suspense']]}}


data2 = {'1603420304': {"helpful":"[0, 0]",'overall':'5','reviewText':"I enjoy vintage books and movies so I enjoyed reading this book.  The plot was unusual.  Don't think killing someone in self-defense but leaving the scene and the body without notifying the police or hitting someone in the jaw to knock them out would wash today.Still it was a good read for me.",'reviewTime': "05 5, 2014",'reviewerID': 'A1F6404F1VG29J',"reviewerName": 'Avidreader,Nice',"summary": "vintage story","unixReviewTime":"1399248000"},
         '1603420304': {"helpful":"[2, 2]",'overall':'4','reviewText':"This book is a reissue of an old one; the author was born in 1910. It's of the era of, say, Nero Wolfe. The introduction was quite interesting, explaining who the author was and why he's been forgotten; I'd never heard of him.The language is a little dated at times, like calling a gun a &#34;heater.&#34;  I also made good use of my Fire's dictionary to look up words like &#34;deshabille&#34; and &#34;Canarsie.&#34; Still, it was well worth a look-see.",'reviewTime':"01 6, 2014",'reviewerID': 'AN0N05A9LIJEQ',"reviewerName":'critters,Different...',"unixReviewTime":'1388966400'}}


app = Flask(__name__)
api = Api(app)

#For testing
#class BookDetail(Resource):
    #def get(self,asin):
        #data = GetBookDetails()
        #print ("data:", data)
        #return data
        #(data[asin]['description'])
    #def put(self,asin):
        #args = book_put_args.parse_args()
        #data[asin] = args 
        #return data[asin], 201

#api.add_resource(GetBookDetails,'/book/<string:asin>')


@app.route('/', methods=['GET'])
def index_page_landing():
    return render_template('index.html')

@app.route('/book/<string:asin>')
def hello_world(asin):
   #api.add_resource(BookDetail,'/book/<string:asin>')
   c = GetBookDetails()
   data = c.get(asin)
   print("data:", data)
   #data = GetBookDetails(asin)
   #print(data[asin]['reviewerID'])
   #data2 = (getlistofbooks(asin)) #returns list
   return render_template('book.html', image = data["imUrl"], description = data["description"])

@app.route('/add-review')
def add_review():
   return render_template('addReview.html')

@app.route('/book')
def book():
   return render_template('book.html')

if __name__ == "__main__":
    app.run(debug=True)