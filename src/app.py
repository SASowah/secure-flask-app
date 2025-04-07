# Module-level docstring
"""
This is the main module of the Flask application. It connects to a local MongoDB
instance, retrieves messages from the 'securedb' database, and displays them
on the homepage.
"""
#import os
from flask import Flask, render_template
from pymongo import MongoClient


# template_dir = os.path.abspath('roles/app_server/templates')  # update path if needed
#app = Flask(__name__)
app = Flask(__name__, template_folder='templates')  # <-- Add template_folder

# Establishing connection to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.securedb
collection = db.messages

@app.route("/")
def index():
    """
    This function handles requests to the root URL ('/'). It retrieves all the messages 
    from the 'messages' collection in the 'securedb' database and renders them 
    in the 'index.html' template.

    Returns:
        Rendered HTML page with messages from the database.
    """
    # Convert the cursor to a list
    messages = list(collection.find())
    return render_template("index.html", messages=messages)

if __name__ == "__main__":
    # Starting the Flask application
    app.run(host="0.0.0.0", port=5000)
