import os,datetime,random
from flask import request, render_template,jsonify, current_app, redirect, url_for
import pymysql
import traceback
from db import DB

from . import user

# 注册
@user.route('/register', methods=['GET','POST'])
def register():
    uname = request.values['username']
    password = request.values['password']
    if not uname or not password:
        return jsonify({'code':-1, 'msg':'无效用户名'})
    
    with DB() as db:
        try:
            db.execute("INSERT INTO user(name, password) VALUES ('%s', '%s')" % (uname, password))
            return jsonify({'code':0, 'data':{}})
        except Exception as e:
            return jsonify({'code':-1, 'msg':'操作异常！'})

# 登录
@user.route('/login', methods=['POST'])
def login():
    uname = request.values['username']
    password = request.values['password']
    if not uname or not password:
        return jsonify({'code':-1, 'msg':'无效用户名'})

    with DB() as db:
        try:
            db.execute("select * from user where name='%s' and password='%s'" % (uname, password))
            results = db.fetchall()
            if len(results) > 0:
                return jsonify({'code':0, 'data':{}})
            else:
                return jsonify({'code':-1, 'msg':'用户名或密码不正确'})
        except Exception as e:
            return jsonify({'code':-1, 'msg':'操作异常！'})


# 注销
@user.route('/logout', methods=['POST'])
def logout():
    uname = request.values['username']
    
    return jsonify({'code':0, 'data':{}})