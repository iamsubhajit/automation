from flask import Flask, request, render_template_string
import boto3
from datetime import datetime

app = Flask(__name__)

#bucket_name = f"uploadbucket{timpestamp}"
bucket_name = "uploadbucket20250616175143"
s3boto = boto3.resource("s3")
#bucket = s3boto.Bucket(bucket_name)
timestamp=datetime.now().strftime("%Y%m%d%H%M%S")


html_form = """
<!doctype html>
<title>Upload Image to S3</title>
<h1>Upload an Image</h1>
<form method=post action=/ enctype=multipart/form-data>
    <input type=file name=image>
    <input type=submit value=Upload>
</form>
"""

@app.route('/', methods=['GET','POST'])
def upload_image():
    if request.method == 'POST':
        if 'image' not in request.files:
            return "No File Part", 400
        file = request.files['image']
        if file.filename == '':
            return "No selected file", 400

        #filename = str(file.filename)
        filename = f"{timestamp}_{file.filename}"
        
        s3boto.Bucket(bucket_name).upload_fileobj(file, filename)
        
        return f"File uploaded successfully to S3 as {filename}"

    return render_template_string(html_form)

if __name__ == '__main__':
    app.run(debug=True)
