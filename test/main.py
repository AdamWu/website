import os,datetime,random

from flask import Flask, render_template, request,jsonify
from werkzeug import secure_filename

app = Flask(__name__)

DIR_ROOT = os.path.dirname(__file__)
DIR_UPLOAD = os.path.join(DIR_ROOT, 'upload')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])

def uuid():
    # unique name
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    num = random.randint(0, 100)
    if num < 10:
        num = str(0) + str(num)
    return str(now) + str(num)

@app.route('/')
def hello_world():
   return 'Hello World'
 
@app.route('/upload', methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        fname = secure_filename(f.filename)

        print (fname)

        # check format
        if '.' in fname and fname.rsplit('.',1)[1] in ALLOWED_EXTENSIONS:
            # save file
            ext = fname.rsplit('.',1)[1]
            filename = uuid() + '.' + ext
            f.save(os.path.join(DIR_UPLOAD, filename))
            return jsonify({"msg":"upload successful!"})
        else:
            return jsonify({"msg":"wrong format!"})
    
    return render_template('upload.html')

if __name__ == '__main__':
   app.run(host='172.17.0.15', port=8080, debug=True)