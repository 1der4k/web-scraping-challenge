# dependencies
from flask import Flask,jsonify,render_template
from flask_pymongo import PyMongo
from scrape_mars import mars_scraper

# create flask app
app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_scraper")
db = mongo.db

@app.route('/')
def home():
    post = db.post.find_one()
    return render_template('index.html', post = post)

@app.route('/scrape')
def scrape():
    post = mars_scraper()
    db.post.update({}, post, upsert=True)

    return jsonify(post)

if __name__ == "__main__":
    app.run(debug=True)