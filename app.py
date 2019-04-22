# Import Dependencies 
from flask_pymongo import PyMongo
from flask import Flask, render_template, redirect 
import scrape_mars
import os

# Create an instance of Flask app
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Create route that renders index.html template and finds documents from mongo
@app.route("/")
def home(): 

    # Find one record of data from the mongo database
    mars_info = mongo.db.collection.find_one()
    # print(mars_info)
    
    # Return template and data
    return render_template("index.html", mars_final_info=mars_info)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape(): 

    # Run scrapped functions
    mars_data = mongo.db.mars_final_info
    mars_data = scrape_mars.scrape_mars_news()
    mars_data = scrape_mars.jpl_mars_space_images()
    mars_data = scrape_mars.scrape_mars_facts()
    mars_data = scrape_mars.scrape_mars_weather()
    mars_data = scrape_mars.scrape_mars_hemispheres()
    
    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__": 
    app.run(debug= True)
