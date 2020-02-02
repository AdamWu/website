import os,datetime,random

from flask import request, render_template,jsonify,current_app
from werkzeug import secure_filename

from . import upload

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])

def uuid():
    # unique name
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    num = random.randint(0, 100)
    if num < 10:
        num = str(0) + str(num)
    return str(now) + str(num)
 
@upload.route('/upload', methods=['POST','GET'])
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
            f.save(os.path.join(current_app.config.get('UPLOAD_FOLDER'), filename))
            return jsonify({"msg":"upload successful!"})
        else:
            return jsonify({"msg":"wrong format!"})
    
    return render_template('upload.html')