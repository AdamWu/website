import os,datetime,random
import math

from flask import Flask, render_template, request,jsonify, abort

app = Flask(__name__)

ROOT = "static/meizitu"              

# 初始化数据
groups = []
for f in os.listdir(ROOT):
    path = os.path.join(ROOT,f)
    if os.path.isdir(path):
        # find a group
        imgs = []
        for f2 in os.listdir(path):
            imgs.append("/"+os.path.join(path,f2))
        groups.append({'id':len(groups), 'title':f, 'imgs':imgs})

GroupPerPage = 20
PageMax = math.floor(len(groups) / GroupPerPage)    

@app.route('/')
def index():
    return get_page(0)

@app.route('/pages/<int:page>')
def get_page(page):
    if page > PageMax:
        abort(404)
    
    idx = page * GroupPerPage
    _groups = []
    for i in range(idx, min(idx+GroupPerPage,len(groups))):
        _groups.append(groups[i])

    return render_template('meizitu.html', groups=_groups, page=page, page_max=PageMax)

@app.route('/group')
def group():
    id = request.args.get('id', 0, type=int)
    group = groups[id]

    return jsonify(group)



if __name__ == '__main__':
   app.run(host='172.17.0.15', port=1206, debug=True)