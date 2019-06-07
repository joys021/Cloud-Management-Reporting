from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask import Flask,render_template, jsonify,request
from flask_bootstrap import Bootstrap
from flask_marshmallow import Marshmallow
import boto3
from botocore.client import Config
from config import S3_BUCKET, S3_KEY, S3_SECRET
import logging
from botocore.exceptions import ClientError
import os
from botocore.exceptions import ClientError



s3 = boto3.client('s3', aws_access_key_id=S3_KEY,
                  aws_secret_access_key=S3_SECRET)

app = Flask(__name__)
ma = Marshmallow(app)
app.config.from_object(__name__)


    
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
@app.route('/files', methods=['GET'])
def files():
    bucket_name_m=request.args.get('bucket')
    s3_resource = boto3.resource('s3')
    err = {}
    err.update({'message':"400"})
    try:
        my_bucket = s3_resource.Bucket(bucket_name_m)
        summaries = my_bucket.objects.all()
        result = users_schema.dump(summaries)
        d1={}
        d1.update({'message':"200"})
        d1.update({'data':result.data})
        return jsonify(d1)
    except ClientError as e:
        err.update({'Error':e.response['Error']['Code']})
        return jsonify(err)
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
    err = {}
    err.update({'message':"400"})
    try:
        obj = s3.Object(S3_BUCKET,'Hello_flask.py')
        result = sse_schema.dump(obj)
        d1={}
        d1.update({'message':"200"})
        d1.update({'data':result.data})
        return jsonify(d1)
    except ClientError as e:
        err.update({'Error':e.response['Error']['Code']})
        return jsonify(err)

class BucSchema(ma.Schema):
    class Meta:
        fields = ("Buckets","Owner")

buc_schema = BucSchema()
bucc_schema = BucSchema(many=True)

#display the list of buckets 
@app.route('/buckets')  
def buckets():
    client = boto3.client('s3')
    err = {}
    err.update({'message':"400"})
    try:
        buckets = client.list_buckets()
        result = buc_schema.dump(buckets)
        d1={}
        d1.update({'message':"200"})
        d1.update({'data':result.data})
        return jsonify(d1)
    except ClientError as e:
        err.update({'Error':e.response['Error']['Code']})
        return jsonify(err)
    
    
#create new bucket    
@app.route('/createbucket')
def createbucket():
    s3 = boto3.resource('s3')
    err = {}
    err.update({'message':"400"})
    try:
        bucket = s3.create_bucket(ACL='public-read-write',
        Bucket='botflas',
        CreateBucketConfiguration={
            'LocationConstraint': 'us-west-2'
        })
        d1={}
        d1.update({'message':"200"})
        d1.update({'data':"Bucket Created Successfully"})
        return jsonify(d1)
    except ClientError as e:
        err.update({'Error':e.response['Error']['Code']})
        return jsonify(err)

#encrypt single bucket       
@app.route('/encryptsinglebucket')
def encryptsinglebucket():
    cl = boto3.client('s3')
    err = {}
    err.update({'message':"400"})
    try:
        respo = cl.put_bucket_encryption(
           Bucket='botflaskproj',
           ServerSideEncryptionConfiguration={
            'Rules': [{'ApplyServerSideEncryptionByDefault': {
                'SSEAlgorithm': 'AES256',}},]})
        d1={}
        d1.update({'message':"200"})
        d1.update({'data':"Bucket encrypted Successfully"})
        return jsonify(d1)
    except ClientError as e:
        err.update({'Error':e.response['Error']['Code']})
        return jsonify(err)


#encrypt all the buckets in an account
@app.route('/encryptallbuckets')
def encryptallbuckets():
    s3_resource = boto3.resource('s3')
    cl = boto3.client('s3')
    err = {}
    err.update({'message':"400"})
    try:
        for bucket in s3_resource.buckets.all():
            respo = cl.put_bucket_encryption(
                Bucket=bucket.name,
                ServerSideEncryptionConfiguration={
                'Rules': [{'ApplyServerSideEncryptionByDefault': {
                'SSEAlgorithm': 'AES256',}},]})
        d1={}
        d1.update({'message':"200"})
        d1.update({'data':"All the Buckets are encrypted Successfully"})
        return jsonify(d1)
    except ClientError as e:
        err.update({'Error':e.response['Error']['Code']})
        return jsonify(err)
        

class ObjSchema(ma.Schema):
    class Meta:
        fields = ("Name","Contents")

obj_schema = ObjSchema()
objj_schema = ObjSchema(many=True)


        
#display all the buckets and the files in it.
@app.route('/all')
def all():
    client = boto3.client('s3')
    s3_resource = boto3.resource('s3')
    err = {}
    err.update({'message':"400"})
    try:
        response = client.list_buckets()
        allobjects = []
        #dict = {}
        bucketnames = [bucket['Name'] for bucket in response['Buckets']]
        for x in range(len(bucketnames)):
            b = bucketnames[x]
            d={}
            d.update( {'Bucket' : b} )
            my_bucket = s3_resource.Bucket(b)
            for file in my_bucket.objects.all():
                d.setdefault("Filenames", []).append(file.key)
            allobjects.append(d)
        d1={}
        d1.update({'message':"200"})
        d1.update({'data':allobjects})
        return jsonify(d1)
    except ClientError as e:
        err.update({'Error':e.response['Error']['Code']})
        return jsonify(err)
        
        
        
        
#display the list of buckets
@app.route('/allbuckets')
def allbucs():
    s3 = boto3.client('s3')
    err = {}
    err.update({'message':"400"})
    try:
        response = s3.list_buckets()
        d = {}
        for bucket in response['Buckets']:
            d.setdefault("Buckets", []).append(bucket['Name'])
        d1={}
        d1.update({'message':"200"})
        d1.update({'data':d})
        return jsonify(d1)
    except ClientError as e:
        err.update({'Error':e.response['Error']['Code']})
        return jsonify(err)

#display the bucket details when name of the bucket is given

@app.route('/listfilesinabucket')
def my_form():
    return render_template('form.html')

#input the bucket name and display the list of files in it
@app.route('/listfilesinabucket', methods=['POST'])
def my_form_post():
    text = request.form['text']
    s3_resource = boto3.resource('s3')
    my_bucket = s3_resource.Bucket(text)
    summaries = my_bucket.objects.all()
    result = users_schema.dump(summaries)
    return jsonify(result.data)


@app.route('/listfilesparam', methods=['GET'])
def listfilesparam():
    bucket_name=request.args.get('bucket')
    s3_resource = boto3.resource('s3')
    err = {}
    err.update({'message':"400"})
    try:
        my_bucket = s3_resource.Bucket(bucket_name)
        summaries = my_bucket.objects.all()
        result = users_schema.dump(summaries)
        d1={}
        d1.update({'message':"200"})
        d1.update({'data':result.data})
        return jsonify(d1)
    except ClientError as e:
        err.update({'Error':e.response['Error']['Code']})
        return jsonify(err)
    


#display the buckets in a particular region

@app.route('/filteronlocation')
def my_for():
    return render_template('for.html')


@app.route('/filteronlocation', methods=['POST'])
def my():
    l = request.form['loc']
    s3 = boto3.client("s3")
    d = {}
    for bucket in s3.list_buckets()["Buckets"]:
        if s3.get_bucket_location(Bucket=bucket['Name'])['LocationConstraint'] == l:
            d.update( {'Bucket' : bucket["Name"]} )          
    return jsonify(d)


#filter on location , location is passed as parameter

@app.route('/filteronlocationparam', methods=['GET'])
def mylocparam():
    location=request.args.get('location')
    s3 = boto3.client("s3")
    d = {}
    err = {}
    err.update({'message':"400"})
    try:
        for bucket in s3.list_buckets()["Buckets"]:
            if s3.get_bucket_location(Bucket=bucket['Name'])['LocationConstraint'] == location:
                d.update( {'Bucket' : bucket["Name"]} )          
        d1={}
        d1.update({'message':"200"})
        d1.update({'data':d})
        return jsonify(d1)
    except ClientError as e:
        err.update({'Error':e.response['Error']['Code']})
        return jsonify(err)


#create new bucket based on user's choice of location   

@app.route('/inputbucketname')
def inputbucket():
    return render_template('create.html')


@app.route('/inputbucketname', methods=['POST'])

def createbucketinput():
    name = request.form['name']
    location = request.form['loc']
    s3 = boto3.resource('s3')
    bucket = s3.create_bucket(ACL='public-read-write',
    Bucket=name,
    CreateBucketConfiguration={
        'LocationConstraint': location
    })
    return render_template('index.html')

#create new bucket with the inputs given by the user
@app.route('/copyinputbucketname')
def copyinputbucket():
    return render_template('create.html')


@app.route('/copyinputbucketname', methods=['POST'])

def copycreatebucketinput():
    name = request.form['name']
    location = request.form['loc']
    s3 = boto3.resource('s3')
    try:
        bucket = s3.create_bucket(ACL='public-read-write',
        Bucket=name,
        CreateBucketConfiguration={
          'LocationConstraint': location
        })
        return render_template('createbucket.html')
    except ClientError as e:
        return jsonify(e.response)
 

#create new bucket with the values passed as parameters
#http://127.0.0.1:5000/createbucketparam?bucket=iinnppuutloc&location=us-west-1
@app.route('/createbucketparam', methods=['GET'])
def createbucketparam():
    bucket_name=request.args.get('bucket')
    location=request.args.get('location')
    s3 = boto3.resource('s3')
    err = {}
    err.update({'message':"400"})
    try:
        bucket = s3.create_bucket(ACL='public-read-write',
        Bucket=bucket_name,
        CreateBucketConfiguration={
          'LocationConstraint': location
        })
        d1={}
        d1.update({'message':"200"})
        d1.update({'data':"Created Bucket Successfully"})
        return jsonify(d1)
    except ClientError as e:
        err.update({'Error':e.response['Error']['Code']})
        return jsonify(err)
        
       

if __name__ == '__main__':
    app.run()

    
