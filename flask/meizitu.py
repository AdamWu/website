import os,datetime,random
import math

from flask import Flask, render_template, request,jsonify, abort

app = Flask(__name__,static_folder="spider")

ROOT = "spider/meizitu"              

# 初始化数据
groups = []
for f in os.listdir(ROOT):
    path = os.path.join(ROOT,f)
    if os.path.isdir(path):
        for f2 in os.listdir(path):
            groups.append({'title':f, 'img':"/"+os.path.join(path,f2)})
            break

GroupPerPage = 10
PageMax = math.floor(len(groups) / 10)    

@app.route('/')
def index():
    return get_page(0)

@app.route('/pages/<int:page>')
def get_page(page):
    if page > PageMax:
        abort(404)
    
    idx = page * 10
    _groups = []
    for i in range(idx, min(idx+10,len(groups))):
        _groups.append(groups[i])

    return render_template('meizitu.html', groups=_groups, page=page, page_max=PageMax)



if __name__ == '__main__':
   app.run(host='172.17.0.15', port=1206, debug=True)