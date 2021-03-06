from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mission_to_mars



app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_to_mars")

@app.route('/')
def home():
    mars_data = mongo.db.collection.find_one()
    return render_template("index.html", dict=mars_data)

@app.route('/scrape')
def scrape():    
    # Run the scrape function
    mars_data = mission_to_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")

#-------------------------
if __name__ == "__main__":
    app.run(debug=True)


