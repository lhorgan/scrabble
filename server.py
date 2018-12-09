
from flask import render_template
from flask import Flask
from flask import request

import json

import scrabble

app = Flask(__name__)
s = scrabble.Scrabble()

@app.route("/")
def home():
    return render_template("./scrabble.html")

@app.route("/requestmove", methods=['GET', 'POST'])
def getmove():
    print("GET MOVE CALLED")

    if request.method=="POST":
        print("POSTED DATA")
        print(request.get_json())

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

if __name__ == "__main__":
    app.run()