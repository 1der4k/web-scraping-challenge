# dependencies
from flask import Flask,jsonify,render_template
from flask pymongo import PyMongo
from scrape_mars import scrape

# create flask app
app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_scraper")
db = mongo.db

@app.route('/')
def home():
    post = mars_data_dict
    return render_template('index.html', post = post)

@app.route('/scrape')
def scrape():