import os
from flask import Flask, render_template
from pymongo import MongoClient

template_dir = os.path.abspath('roles/app_server/templates')  # update path if needed
app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client.securedb
collection = db.messages

@app.route("/")
def index():
    # Convert the cursor to a list
    messages = list(collection.find())
    return render_template("index.html", messages=messages)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
