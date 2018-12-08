
from flask import render_template
from flask import Flask
app = Flask(__name__)
 
@app.route("/")
def scrabble():
    return render_template("./scrabble.html")
 
if __name__ == "__main__":
    app.run()