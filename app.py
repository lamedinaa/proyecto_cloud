from re import template
from flask import Flask, render_template


app = Flask(__name__,template_folder="Templates")

@app.route("/")
def login():
    return render_template("Front/login.html")



if __name__=='__main__':
    app.run(debug=True)
