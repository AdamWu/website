import os,datetime,random

from flask import Flask, render_template, request,jsonify

app = Flask(__name__,static_folder="spider")

ROOT = "spider/meizitu"              

@app.route('/')
def index():
    pages = []
    for f in os.listdir(ROOT):
        path = os.path.join(ROOT,f)
        if os.path.isdir(path):
            for f2 in os.listdir(path):
                pages.append({'title':f, 'img':os.path.join(path,f2)})
                break
    
    return render_template('meizitu.html', pages=pages)
 
if __name__ == '__main__':
   app.run(host='172.17.0.15', port=1206, debug=True)