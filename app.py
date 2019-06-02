from flask import Flask,render_template, jsonify
from flask_bootstrap import Bootstrap
from flask_marshmallow import Marshmallow
import boto3
from botocore.client import Config
from config import S3_BUCKET, S3_KEY, S3_SECRET
import logging
from botocore.exceptions import ClientError


s3 = boto3.client('s3', aws_access_key_id=S3_KEY,
                  aws_secret_access_key=S3_SECRET)

app = Flask(__name__)
ma = Marshmallow(app)


class UserSchema(ma.Schema):
    class Meta:
        fields = ("bucket_name", "key", "last_modified","size")

user_schema = UserSchema()
users_schema = UserSchema(many=True)

Bootstrap(app)

@app.route('/')

def index():
    return render_template('index.html') 


#display the details of the files in a bucket
@app.route('/files')
def files():
    s3_resource = boto3.resource('s3')
    my_bucket = s3_resource.Bucket(S3_BUCKET)
    summaries = my_bucket.objects.all()
    result = users_schema.dump(summaries)
    return jsonify(result.data)
    #return jsonify({'in':'progress'})
    #return render_template('files.html', my_bucket=my_bucket, files=summaries)
    

class SSeSchema(ma.Schema):
    class Meta:
        fields = ("bucket_name", "key", "last_modified", "server_side_encryption", "sse_customer_algorithm", "sse_customer_key_md5", "ssekms_key_id")

sse_schema = SSeSchema()
sses_schema = SSeSchema(many=True)


#display the details of a file in a particular bucket including encryption details
@app.route('/objectdetails')
def objectdetails():
    s3 = boto3.resource('s3')
    obj = s3.Object(S3_BUCKET,'Hello_flask.py')
    result = sse_schema.dump(obj)
    return jsonify(result.data)


class BucSchema(ma.Schema):
    class Meta:
        fields = ("Buckets","Owner")

buc_schema = BucSchema()
bucc_schema = BucSchema(many=True)

#display the list of buckets 
@app.route('/buckets')
def buckets():
    client = boto3.client('s3')
    buckets = client.list_buckets()
    result = buc_schema.dump(buckets)
    return jsonify(result.data)
    
    
#create new bucket    
@app.route('/createbucket')
def createbucket():
    s3 = boto3.resource('s3')
    bucket = s3.create_bucket(ACL='public-read-write',
    Bucket='botflaskproj',
    CreateBucketConfiguration={
        'LocationConstraint': 'us-west-2'
    })
    

#encrypt single bucket       
@app.route('/encryptsinglebucket')
def encryptsinglebucket():
    cl = boto3.client('s3')
    respo = cl.put_bucket_encryption(
    Bucket='botflaskproj',
    ServerSideEncryptionConfiguration={
    'Rules': [{'ApplyServerSideEncryptionByDefault': {
            'SSEAlgorithm': 'AES256',}},]})
    return render_template('encrypt.html') 


#encrypt all the buckets in an account
@app.route('/encryptallbuckets')
def encryptallbuckets():
    s3_resource = boto3.resource('s3')
    cl = boto3.client('s3')
    for bucket in s3_resource.buckets.all():
        respo = cl.put_bucket_encryption(
        Bucket=bucket.name,
        ServerSideEncryptionConfiguration={
        'Rules': [{'ApplyServerSideEncryptionByDefault': {
        'SSEAlgorithm': 'AES256',}},]})
    return render_template('allencrypt.html') 
        

class ObjSchema(ma.Schema):
    class Meta:
        fields = ("Name","Contents")

obj_schema = ObjSchema()
objj_schema = ObjSchema(many=True)

@app.route('/allfiles')
def allfiles():
    client = boto3.client('s3')
    s3_resource = boto3.resource('s3')
    response = client.list_buckets()
    bucketnames = [bucket['Name'] for bucket in response['Buckets']]
    for x in range(len(bucketnames)):
        b=bucketnames[x]
        response = client.list_objects(Bucket=b)
    result = obj_schema.dump(response)
    return jsonify(result.data)
    

@app.route('/all')
def all():
    client = boto3.client('s3')
    s3_resource = boto3.resource('s3')
    response = client.list_buckets()
    dict = {}
    bucketnames = [bucket['Name'] for bucket in response['Buckets']]
    for x in range(len(bucketnames)):
        b = bucketnames[x]
        dict["BucketName"] = [b] 
        my_bucket = s3_resource.Bucket(b)
        for file in my_bucket.objects.all():
            dict.setdefault("Filename", []).append(file.key)
    return jsonify(dict)
        


if __name__ == '__main__':
    app.run()

    
