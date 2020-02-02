from flask import request, render_template, redirect, url_for
from . import main

@main.route('/')
def hello_world():
    return render_template('index.html')
