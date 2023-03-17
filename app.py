import function_data as function
import requests

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():

    return render_template("index.html")

