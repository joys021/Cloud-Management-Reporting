
from flask import Flask,render_template, jsonify
from flask_bootstrap import Bootstrap
from flask_marshmallow import Marshmallow
import boto3
from botocore.client import Config
from config import S3_BUCKET, S3_KEY, S3_SECRET

s3 = boto3.client('s3', aws_access_key_id=S3_KEY,
                  aws_secret_access_key=S3_SECRET)

app = Flask(__name__)
ma = Marshmallow(app)


class UserSchema(ma.Schema):
    class Meta:
        fields = ("bucket_name", "key", "last_modified")

user_schema = UserSchema()
users_schema = UserSchema(many=True)

Bootstrap(app)

@app.route('/')

def index():
    return render_template('index.html') 

@app.route('/files')
def files():
    s3_resource = boto3.resource('s3')
    my_bucket = s3_resource.Bucket(S3_BUCKET)
    summaries = my_bucket.objects.all()
    result = users_schema.dump(summaries)
    return jsonify(result.data)
    #return render_template('files.html', my_bucket=my_bucket, files=summaries)
    

if __name__ == '__main__':
    app.run()
