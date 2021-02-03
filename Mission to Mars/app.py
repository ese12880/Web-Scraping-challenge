from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    nasa = mongo.db.nasa_details.find_one()
    mars = mongo.db.mars_details.find_one()
    hemispshere_Cerberus = mongo.db.hemisphere_details.find_one({'title': 'Cerberus Hemisphere Enhanced'})
    hemispshere_Schiaparelli = mongo.db.hemisphere_details.find_one({'title': 'Schiaparelli Hemisphere Enhanced'})
    hemispshere_Syrtis = mongo.db.hemisphere_details.find_one({'title': 'Syrtis Major Hemisphere Enhanced'})
    hemispshere_Valles = mongo.db.hemisphere_details.find_one({'title': 'Valles Marineris Hemisphere Enhanced'})
    # Return template and data
    return render_template("index.html", nasa=nasa, mars=mars,hemispshere_Cerberus=hemispshere_Cerberus,hemispshere_Schiaparelli=hemispshere_Schiaparelli,hemispshere_Syrtis=hemispshere_Syrtis,hemispshere_Valles=hemispshere_Valles)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    nasa_data,mars_data,hemispheres_data = scrape_mars.scrape_info()
    mongo.db.nasa_details.update({}, nasa_data, upsert=True)
    mongo.db.mars_details.update({}, mars_data, upsert=True)
    mongo.db.hemisphere_details.drop()
    mongo.db.hemisphere_details.insert_many(hemispheres_data)
   

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)