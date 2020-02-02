from flask import Flask, render_template, request, jsonify
from flask import Blueprint
import pymysql

from main import main as main_blueprint
from upload import upload as upload_blueprint
from user import user as user_blueprint

#app = Flask(__name__)
app = Flask(__name__, static_url_path='', static_folder ='static', template_folder='static')
app.config['UPLOAD_FOLDER'] = './static/upload/'

app.register_blueprint(main_blueprint)
app.register_blueprint(upload_blueprint)
app.register_blueprint(user_blueprint)


db = pymysql.connect("localhost","root","120688wuyunze","test" )
try:
    db.cursor().execute('create table if not exists user(id int PRIMARY KEY AUTO_INCREMENT,name varchar(100) unique NOT NULL,password varchar(100))')
    db.commit()
except:
    db.rollback()
db.close()

#app.run(host='172.17.0.15', port=8080, debug=True)
app.run(host='127.0.0.1', port=8080, debug=True)