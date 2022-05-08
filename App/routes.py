from App import application as app
from App import db
from flask import jsonify, request, render_template, redirect, flash, url_for

@app.route('/')
def home():
    R = jsonify("Hello World!")
    R.status_code = 200
    return R