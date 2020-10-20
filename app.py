from flask import Flask, render_template
app = Flask(__name__)
@app.route('/', methods=['GET'])
def index_page_landing():
    return render_template('index.html')
@app.route('/book')
def hello_world():
   return render_template('book.html')

if __name__ == "__main__":
    app.run()