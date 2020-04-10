#Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
from flask import Flask, render_template
import requests
import pandas as pd
from scrape_mars import scrape
import pymongo 
from flask_pymongo import PyMongo

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/scrape')
def mars_webscrape():
    return scrape()

if __name__ == "__main__":
    app.run(debug=True)