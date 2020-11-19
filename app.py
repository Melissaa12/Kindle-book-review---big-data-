from flask import Flask, render_template
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
