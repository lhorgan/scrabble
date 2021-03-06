
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
    res = {'success': True}

    if request.method=="POST":
        print("POSTED DATA")
        json_data = request.get_json()
        s.board = json_data["board"]
        s.tiles = json_data["tiles"]
        word, row, col, horiz = s.pick_best_move()
        res["word"] = word
        res["row"] = row
        res["col"] = col
        res["horiz"] = horiz

    return json.dumps(res), 200, {'ContentType':'application/json'} 

if __name__ == "__main__":
    app.run()