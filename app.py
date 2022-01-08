from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import mtm_scrape 

# Create an instance of Flask app
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route('/')
def index():
	
	mars_info = mongo.db.collection.find_one()
	return render_template("index.html", mars=mars_info)

@app.route('/scrape')
def scrape():
	mars_info = mongo.db.mars_app
	mars_data = mtm_scrape.scrape_info()
	mars_info.update({}, mars_data, upsert=True)
	
	return redirect("/", code=302)

if __name__ == "__main__":
	app.run(debug=True)