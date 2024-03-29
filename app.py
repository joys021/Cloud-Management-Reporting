import pdb
from flask import Flask, render_template, flash, request,json
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask import Flask,render_template, jsonify
from flask_bootstrap import Bootstrap
from flask_marshmallow import Marshmallow
import boto3, requests
import pandas as pd
from botocore.client import Config
from config import S3_BUCKET, S3_KEY, S3_SECRET
import logging
from botocore.exceptions import ClientError
import os
from botocore.exceptions import ClientError
from flask import Flask
from flask_restless import APIManager
from flask_cors import CORS
logging.basicConfig(level=logging.INFO)
from flask_cors import CORS, cross_origin
import os, time
import datetime
from collections import Counter
import os.path
from os import path
from datetime import timedelta
from datetime import datetime
from time import gmtime, strftime
from flask import send_file
from flask import Flask, render_template
import logging
import glob
from collections import Counter
import collections
import operator
from operator import itemgetter
from collections import OrderedDict
import pandas as pd

#def add_cors_headers(response):
#    response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5000'
#    response.headers['Access-Control-Allow-Credentials'] = 'true'
#    response.headers['Access-Control-Allow-Methods'] = 'GET', 'POST', 'OPTIONS'
#    response.headers['Access-Control-Allow-Methods'] = 'Origin', 'Content-Type', 'Accept'
#    # Set whatever other headers you like...
#    return response

#app = Flask(__name__)
#manager = APIManager(app)
#blueprint = manager.create_api_blueprint('all', all)
#blueprint.(add_cors_headers)after_request
#app.register_blueprint(blueprint)


s3 = boto3.client('s3', aws_access_key_id=S3_KEY,
                  aws_secret_access_key=S3_SECRET)

app = Flask(__name__)
ma = Marshmallow(app)
app.config.from_object(__name__)

CORS(app)
CORS(app, methods='POST')  
class UserSchema(ma.Schema):
    class Meta:
        fields = ("bucket_name", "key", "last_modified","size")

user_schema = UserSchema()
users_schema = UserSchema(many=True)
CORS(app, resources={r"/*": {"origins": "*","methods" : ['GET','POST','OPTIONS'] }})    
Bootstrap(app)


@app.route('/', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
def index():
    return render_template('index.html') 


#display the details of the files in a bucket


@app.route('/files', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
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


@app.route('/objectdetails', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
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

@app.route('/buckets', methods = ['GET', 'POST'])  
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
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
   
@app.route('/createbucket', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type']) 
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
     
@app.route('/encryptsinglebucket', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type']) 
def encryptsinglebucket():
    cl = boto3.client('s3')
    err = {}
    bucket_name=request.args.get('bucket')
    err.update({'message':"400"})
    try:
        respo = cl.put_bucket_encryption(
           Bucket=bucket_name,
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

@app.route('/encryptallbuckets', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type']) 
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

cors = CORS(app, resources={r"/*": {"origins": "*","methods" : ['GET','POST','OPTIONS'] }})    
    
#display all the buckets and the files in it.
@app.route('/all', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
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
        #d2={}
        d1.update({'message':"200"})
        d1.update({'data':  allobjects})
        ll = []
        ll.append(d1)
        #ll.append(d2)
        return jsonify(allobjects)
    except ClientError as e:
        err.update({'Error':e.response['Error']['Code']})
        return jsonify(err)
        
        
        
        
#display the list of buckets
 
@app.route('/allbuckets', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type']) 
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
        ll = []
        ll.append(d1)
        return jsonify(ll)
    except ClientError as e:
        err.update({'Error':e.response['Error']['Code']})
        return jsonify(err)

#display the bucket details when name of the bucket is given

@app.route('/listfilesinabucket', methods = ['POST'])   
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
def my_form():
    return render_template('form.html')

#input the bucket name and display the list of files in it

@app.route('/listfilesinabucket', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
def my_form_post():
    text = request.form['text']
    s3_resource = boto3.resource('s3')
    my_bucket = s3_resource.Bucket(text)
    summaries = my_bucket.objects.all()
    result = users_schema.dump(summaries)
    return jsonify(result.data)



@app.route('/listfilesparam', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
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

@app.route('/filteronlocation', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
def my_for():
    return render_template('for.html')


@app.route('/filteronlocation', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
def my():
    l = request.form['loc']
    s3 = boto3.client("s3")
    d = {}
    for bucket in s3.list_buckets()["Buckets"]:
        if s3.get_bucket_location(Bucket=bucket['Name'])['LocationConstraint'] == l:
            d.update( {'Bucket' : bucket["Name"]} )          
    return jsonify(d)


#filter on location , location is passed as parameter

@app.route('/filteronlocationparam', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
def mylocparam():
    location=request.args.get('location')
    s3 = boto3.client("s3")
    d = {}
    err = {}
    err.update({'message':"400"})
    try:
        d={}
        for bucket in s3.list_buckets()["Buckets"]:
            if s3.get_bucket_location(Bucket=bucket['Name'])['LocationConstraint'] == location:
                #d.update( {'Bucket' : bucket["Name"]} ) 
                d.setdefault("Buckets", []).append(bucket['Name'])
        d1={}
        d1.update({'message':"200"})
        d1.update({'data':d})
        ll = []
        ll.append(d1)
        return jsonify(ll)
        d1={}
        d1.update({'message':"200"})
        d1.update({'data':d})
        ll = []
        ll.append(d1)
        return jsonify(ll)
    except ClientError as e:
        err.update({'Error':e.response['Error']['Code']})
        return jsonify(err)


#create new bucket based on user's choice of location   

@app.route('/inputbucketname', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
def inputbucket():
    return render_template('create.html')


@app.route('/inputbucketname', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
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

@app.route('/copyinputbucketname', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
def copyinputbucket():
    return render_template('create.html')



@app.route('/copyinputbucketname', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
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

@app.route('/createbucketparam', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
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




@app.route('/regionsofbuckets', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
def myregion():
    #location=request.args.get('location')
    s3 = boto3.client("s3")
    client = boto3.client('s3')
    err = {}
    #allobjects = {}
    err.update({'message':"400"})
    try:
        d={}
        response = client.list_buckets()
        bucketnames = [bucket['Name'] for bucket in response['Buckets']]
        regionnames = []
        allobjects = []
        for bucket in bucketnames:
            regionnames.append((s3.get_bucket_location(Bucket = bucket))['LocationConstraint'])
        regionnames = list(set(regionnames))    
        for x in range(len(regionnames)):
            b = regionnames[x]
            d={}
            d.update( {'region' : b} )
            
            #my_bucket = s3_resource.Bucket(b)
            for bucket in bucketnames:
                if s3.get_bucket_location(Bucket=bucket)['LocationConstraint'] == b:
                    d.setdefault("ttt", []).append(bucket)
            leng = len(d['ttt'])
            d.update( {'buckets' : leng} )
            del d["ttt"],
            allobjects.append(d)
            #d.setdefault("Buckets", []).append(bucket['Name'])
        d1={}
        d1.update({'message':"200"})
        d1.update({'data':allobjects})
        ll = []
        ll.append(d1)
        return jsonify(allobjects)
    except ClientError as e:
        err.update({'Error':e.response['Error']['Code']})
        return jsonify(err)


    
#display all the buckets and the files in it.
@app.route('/allcount', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
def allcount():
    client = boto3.client('s3')
    s3_resource = boto3.resource('s3')
    err = {}
    err.update({'message':"400"})
    try:
        response = client.list_buckets()
        allobjects = []
        d = {}
        #dict = {}
        bucketnames = [bucket['Name'] for bucket in response['Buckets']]
        for x in range(len(bucketnames)):
            b = bucketnames[x]
            d={}
            d.update( {'bucket' : b} )
            my_bucket = s3_resource.Bucket(b)
            mybucs = [file.key for file in my_bucket.objects.all()]
            lengh = len(mybucs)
            #for file in mybucs:
            #    d.setdefault("Filenames", []).append(file)
            d.update( {'objectscount' : lengh} )
            allobjects.append(d)
        d1={}
        #d2={}
        d1.update({'message':"200"})
        d1.update({'data':  allobjects})
        ll = []
        ll.append(d1)
        #ll.append(d2)
        return jsonify(allobjects)
    except ClientError as e:
        err.update({'Error':e.response['Error']['Code']})
        return jsonify(err)
        
        


@app.route('/getfile', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
def getfilefunc():
    file_name=request.args.get('filename')
    err = {}
    err.update({'message':"400"})
    try:
        onehour = 60
        filepath = 'venv/cache/'+file_name
        if ((path.exists(filepath)) == False):
            api = file_name[-len(file_name):-5]
            items = requests.get('http://127.0.0.1:5000/'+api)
            data = items.json()
            with open('venv/cache/'+file_name, 'w') as f:
                json.dump(data, f) 
        filestat = os.stat('venv/cache/'+file_name)
        date_format = "%Y-%m-%d %H:%M:%S"
        d2 = "%Y-%m-%d %H:%M:%S.%f"
        #date = time.localtime((filestat.st_mtime))
        modTimesinceEpoc = os.path.getmtime('venv/cache/'+file_name)
        presenttime = str(datetime.now())
        modificationTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modTimesinceEpoc))
        time1  = datetime.strptime(modificationTime, date_format)
        time2  = datetime.strptime(presenttime, d2)
        diff = time2 - time1
        diffinminutes = (diff.seconds) / 60
        if onehour > diffinminutes:
            return send_file('cache/'+file_name, attachment_filename=file_name)
            #return send_file(file_name, attachment_filename=file_name)
        else:
            api = file_name[-len(file_name):-5]
            items = requests.get('http://127.0.0.1:5000/'+api)
            data = items.json()
            with open('venv/cache/'+file_name, 'w') as f:
                json.dump(data, f)
        d1 = {} 
        d1.update({'message':"200"})
        d1.update({'last modified time':modificationTime})
        d1.update({'present time':presenttime})
        d1.update({'diff in minutes':str(diffinminutes)})
        ll = []
        ll.append(d1)
        return send_file('cache/'+file_name, attachment_filename=file_name)
    except ClientError as e:
        err.update({'Error':e.response['Error']['Code']})
        return jsonify(err)




#this will save the files for the first time in the cache
@app.route('/savefiles', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
def saveallfiles():
    #location=request.args.get('location')
    s3 = boto3.client("s3")
    err = {}
    err.update({'message':"400"})
    try:
        file_name = 'allbuckets.json'
        api = file_name[-len(file_name):-5]
        url = ('http://127.0.0.1:5000/'+api)
        items = requests.get(url) # (your url)
        data = items.json()
        with open('venv/cache/allbuckets.json', 'w') as f:
            json.dump(data, f)
        item2 = requests.get('http://127.0.0.1:5000/allcount') # (your url)
        data = item2.json()
        with open('venv/cache/allcount.json', 'w') as f:
            json.dump(data, f)
        d1={}
        d1.update({'message':url})
        d1.update({'data':"Saved file Successfully"})
        ll = []
        ll.append(d1)
        return jsonify(ll)
    except ClientError as e:
        err.update({'Error':e.response['Error']['Code']})
        return jsonify(err)


#get the number of encrypted and unencrypted buckets
@app.route('/bucketencryptiondetails', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
def bucketencryptiondetails():
    #location=request.args.get('location')
    s3 = boto3.client("s3")
    client = boto3.client('s3')
    err = {}
    #allobjects = {}
    err.update({'message':"400"})
    try:
        d={}
        response = client.list_buckets()
        bucketnames = [bucket['Name'] for bucket in response['Buckets']]
        encbuckets = []
        unencbuckets = []
        for bucket in bucketnames:
            try:
                if((s3.get_bucket_encryption(Bucket = bucket)['ServerSideEncryptionConfiguration']['Rules'][0]['ApplyServerSideEncryptionByDefault']['SSEAlgorithm'])=='AES256'):
                    encbuckets.append(bucket)
            except ClientError as e:
                unencbuckets.append(bucket)
            #raise ClientError("Can't calculate log")
        encleng = len(encbuckets)
        unencleng = len(unencbuckets)
        d1={}
        d2 = {}
        d1.update({'type':"encrypted", "count":encleng})
        d2.update({'type':"unencrypted", "count":unencleng})
        ll = []
        ll.append(d1)
        ll.append(d2)        
        return jsonify(ll)
    except ClientError as e:
        err.update({'Error':e.response['Error']['Code']})
        return jsonify(err)


#get the size of the buckets in bytes
@app.route('/bucketsize', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
def bucketsize():
    #location=request.args.get('location')
    s3 = boto3.client("s3")
    client = boto3.client('s3')
    err = {}
    bucketsizes = []
    total_size = 0
    allobjects = []
    err.update({'message':"400"})
    try:
        response = client.list_buckets()
        bucketnames = [bucket['Name'] for bucket in response['Buckets']]
        for mybucket in bucketnames:
            bucket = boto3.resource('s3').Bucket(mybucket)
            for file in bucket.objects.all():
                total_size += file.size
            bucketsizes.append(total_size)
        for x in range(len(bucketsizes)):
            b = bucketsizes[x]
            ss = b/1024
            d={}
            d.update( {'bucket' : bucketnames[x]} )
            d.update( {'size' : ss} )  
            allobjects.append(d)
        return jsonify(allobjects)
    except ClientError as e:
        err.update({'Error':e.response['Error']['Code']})
        return jsonify(err)

@app.route('/filesfrompath')
def content():
    text = open('venv/cache/geo.json', 'r+')
    content = text.read()
    text.close()
    return(content)




@app.route('/getgeo', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
def contentss():
    client = boto3.client('s3')
    err = {}
    #allobjects = {}
    err.update({'message':"400"})
    try:
        d={}
        regionnames = []
        response = client.list_buckets()
        bucketnames = [bucket['Name'] for bucket in response['Buckets']]
        for bucket in bucketnames:
            regionnames.append((client.get_bucket_location(Bucket = bucket))['LocationConstraint'])
        regionnames = list(set(regionnames))
        allobjects =[]
        item2 = requests.get('http://127.0.0.1:5000/filesfrompath') # (your url)
        data = item2.json()
        with open('venv/cache/geo2.json', 'w') as f:
            json.dump(data, f)
        for x in range(len(regionnames)):
            b = regionnames[x]
            for item in data:
                if item['region'] == b:
                    lat = item['lat']
                    lon = item['lon']
                    regionname = item['regionname']
                    d={}
                    d.update( {'lat' : lat} )
                    d.update( {'lon' : lon} )
                    d.update( {'regionname' : regionname} )
                    break
            allobjects.append(d)
        return jsonify(allobjects)
    except ClientError as e:
        err.update({'Error':e.response['Error']})
        return jsonify(err)
        
        
@app.route('/regionsofinstances', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
def instanceregion():
    #location=request.args.get('location')
    ec2 = boto3.client('ec2', region_name='us-east-1')
    err = {}
    #RunningInstances = []
    allobjects = []
    err.update({'message':"400"})
    try:
        val = []
        d = {}
        response = ec2.describe_regions()
        jj = list(response['Regions'])
        for i in jj:
            val.append(i.get('RegionName'))
        #kk = list(set(val))
        for x in range(len(val)):
            b = val[x]
            d = {}
            d.update( {'region' : b} )
            d.update( {'countofreg' : val} )
            #d.update( {'length of the list' : len(jj)} )
            #del d["ttt"]
            allobjects.append(d)
        return jsonify(allobjects)
        #return jsonify(len(jj))
    except ClientError as e:
        err.update({'Error':e.response['Error']['Code']})
        return jsonify(err)

@app.route('/instances', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
def instance():
    #location=request.args.get('location')
    client = boto3.client('ec2', region_name='us-west-1')
    err = {}
    RunningInstances = []
    regionnames =[]
    #allobjects = {}
    err.update({'message':"400"})
    try:
        d ={}
        allobjects = []
        val = []
        #leng = []
        #client = boto3.client('ec2')
        response = client.describe_regions()
        jj = list(response['Regions'])
        for i in jj:
            val.append(i.get('RegionName'))
        #regionnames = list(regions)
        for x in range(len(val)):
            b = val[x]
            d = {}
            d.update( {'region' : b} )
            ec2 = boto3.resource('ec2',region_name=b)
            running_instances = ec2.instances.all()
            
            if (len(list(set(running_instances)))>0):
                for instance in running_instances:
                    d.setdefault("ttt", []).append(instance.id)
                    leng = len(d["ttt"])
                    d.update( {'instancescount' : leng} )
                    del d["ttt"]
            else:
                d.update({'instancescount' : 0})
            allobjects.append(d)
        return jsonify(allobjects)
    except ClientError as e:
        err.update({'Error':e.response['Error']['Code']})
        return jsonify(err)


@app.route('/instancestate', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
def instancestate():
    #location=request.args.get('location')
    client = boto3.client('ec2', region_name='us-west-1')
    err = {}
    #RunningInstances = []
    regionnames =[]
    #allobjects = {}
    err.update({'message':"400"})
    try:
        val = []
        allstate = []
        response = client.describe_regions()
        jj = list(response['Regions'])
        for i in jj:
            val.append(i.get('RegionName'))
        #regionnames = list(regions)
        for x in range(len(val)):
            b = val[x]
            d = {}
            ec2 = boto3.resource('ec2',region_name=b)
            running_instances = ec2.instances.all()
            for instance in running_instances:
                allstate.append(instance.state['Name'])
        d1={}
        d2 = {}
        d3={}
        d4 = {}
        d5={}
        d6 = {}
        d1.update({'type':"pending", "count":allstate.count('pending')})
        d2.update({'type':"running", "count":allstate.count('running')})
        d3.update({'type':"stopping", "count":allstate.count('stopping')})
        d4.update({'type':"stopped", "count":allstate.count('stopped')})
        d5.update({'type':"shutting-down", "count":allstate.count('shutting-down')})
        d6.update({'type':"terminated", "count":allstate.count('terminated')})
        ll = []
        ll.append(d1)
        ll.append(d2)
        ll.append(d3)
        ll.append(d4) 
        ll.append(d5)
        ll.append(d6) 
        return jsonify(ll)
    except ClientError as e:
        err.update({'Error':e.response['Error']['Code']})
        return jsonify(err)



# to get total security groups in all regions in an account
@app.route('/totalsecuritygroups', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
def totalsecuritygroups():
    #location=request.args.get('location')
    client = boto3.client('ec2', region_name='us-east-1')
    err = {}
    #RunningInstances = []
    regionnames =[]
    #allobjects = {}
    err.update({'message':"400"})
    try:
        val = []
        allstate = []
        response = client.describe_regions()
        jj = list(response['Regions'])
        for i in jj:
            val.append(i.get('RegionName'))
        #regionnames = list(regions)
        for x in range(len(val)):
            b = val[x]
            d = {}
            ec2 = boto3.client('ec2', region_name=b)
            sec_groups = ec2.describe_security_groups()['SecurityGroups']
            allstate.append(len(sec_groups))
        d1={}
        d1.update({"totalsecuritygroups":sum(allstate)})
        ll = []
        ll.append(d1)
        return jsonify(ll)
    except ClientError as e:    
        err.update({'Error':e.response['Error']['Code']})
        return jsonify(err)

#get details from multiple log files - 1 day
@app.route('/readcloudtraillogs')
def readcloudtraillogs():
    path = 'venv/cache/2015_cloudtrail/2015/01/01'
    path_to_json = 'venv/cache/2015_cloudtrail/2015/01/01'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    files = []
    events = []
    eventtime = []
    username = []
    src = []
    arn = []
    d = {}
    overall = []
    for r, d, f in os.walk(path):
        for file in f:
            if '.json' in file:
                files.append(os.path.join(r, file))         
    for index, js in enumerate(files):
        with open(js, 'r') as f:
            datastore = json.load(f)
            for x in range(len(datastore['Records'])):
                events.append(datastore['Records'][x]['eventName'])
                eventtime.append(datastore['Records'][x]['eventTime'])
                username.append(datastore['Records'][x]['userIdentity']['userName'])
                arn.append(datastore['Records'][x]['userIdentity']['arn'])
                src.append(datastore['Records'][x]['sourceIPAddress'])
        d = {}
        d.update({'Events' : events})
        d.update({'EventNames':events })
        d.update({'Eventtime':eventtime })
        d.update({'Username':username})
        d.update({'ARN':arn})
        d.update({'SourceIPAddress':src})
        overall = []
    overall = []
    overall.append(d)
    return jsonify(overall)
           

    
#get details from single log file
@app.route('/readsinglelog')
def readsinglelog():
    path = 'venv/cache/2015_cloudtrail/2015/01'
    files = []
    events = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.json' in file:
                files.append(os.path.join(r, file))       
    with open("venv/cache/log.json", "wb") as outfile:
        for f in files:
            with open(f, "rb") as infile:
                outfile.write(infile.read())
    #text = open("venv/cache/2015_cloudtrail/2015/01/01/361166629815_CloudTrail_us-east-1_20150101T0000Z_nqSzxQ623cykwe1r.json", 'r+')
    #content = text.read()
    with open("venv/cache/2015_cloudtrail/2015/01/01/361166629815_CloudTrail_us-east-1_20150101T0000Z_nqSzxQ623cykwe1r.json", 'r') as f:
        datastore = json.load(f)    
    #cont.update({'data' : content})
    #text.close()
    eventtime = []
    username = []
    src = []
    arn = []
    for x in range(len(datastore['Records'])):
        events.append(datastore['Records'][x]['eventName'])
        eventtime.append(datastore['Records'][x]['eventTime'])
        username.append(datastore['Records'][x]['userIdentity']['userName'])
        arn.append(datastore['Records'][x]['userIdentity']['arn'])
        src.append(datastore['Records'][x]['sourceIPAddress'])
    d = {}
    d.update({'EventNames':events })
    d.update({'Eventtime':eventtime })
    d.update({'Username':username})
    d.update({'ARN':arn})
    d.update({'SourceIPAddress':src})
    overall = []
    overall.append(d)
    return jsonify(overall)



# to get total rules in all security groups in all regions in an account
@app.route('/totalrules', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
def totalrules():
    #location=request.args.get('location')
    client = boto3.client('ec2', region_name='us-east-1')
    err = {}
    #RunningInstances = []
    regionnames =[]
    #allobjects = {}
    err.update({'message':"400"})
    try:
        val = []
        allstate = []
        rules = []
        response = client.describe_regions()
        jj = list(response['Regions'])
        for i in jj:
            val.append(i.get('RegionName'))
        #regionnames = list(regions)
        for x in range(len(val)):
            b = val[x]
            d = {}
            ec2 = boto3.client('ec2', region_name=b)
            sec_groups = ec2.describe_security_groups()['SecurityGroups']
            for y in range(len(sec_groups)):
                rules.append(sec_groups[y]['IpPermissions'])
                rules.append(sec_groups[y]['IpPermissionsEgress'])
                #a = val[y]
                #rules =                 
            allstate.append(len(rules))
        d1={}
        d1.update({"totalrules":len(rules)})
        ll = []
        ll.append(d1)
        return jsonify(ll)
    except ClientError as e:    
        err.update({'Error':e.response['Error']['Code']})
        return jsonify(err)


#get top ten events performed in a day
@app.route('/toptenevents')
def toptenevents():
    path = 'venv/cache/2015_cloudtrail/2015/01/04'
    path_to_json = 'venv/cache/2015_cloudtrail/2015/01/26'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    files = []
    events = []
    d = {}
    overall = []
    for r, d, f in os.walk(path):
        for file in f:
            if file.endswith('.json'):
                files.append(os.path.join(r, file))         
    for index, js in enumerate(files):
        with open(js, 'r') as f:
            datastore = json.load(f)
            for x in range(len(datastore['Records'])):
                events.append(datastore['Records'][x]['eventName'])
        d = {}
        dd = []
        newevent = {}
        newevent = Counter(events) 
        d.update({'EventNames' : Counter(events) })
        sorted_dict = sorted(newevent.items(), key=operator.itemgetter(1),reverse=True)
        dd = OrderedDict(sorted(newevent.items(), key=lambda x: x[1]))
        d.update({'EventNames' : sorted_dict[:10] })
    overall = []
    overall.append(d)
    return jsonify(overall)
           


#get top ten events performed in a month
@app.route('/topteneventsinamonth')
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
def topteneventsinamonth():
    month=request.args.get('month')
    all1 = []
    all2 = []
    add = {}
    d = {}
    ff = {}
    mon = []
    orig = collections.Counter()
    llist = ['start','jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
    mon = [i for i, j in enumerate(llist) if j == month]
    mo = mon[0]
    m = ("{:02d}".format(mo))
    for uu in range(1,32):
        if uu < 10:
            path = 'venv/cache/2015_cloudtrail/2015/'+str(m)+'/0'+ str(uu)
        else:
            path = 'venv/cache/2015_cloudtrail/2015/'+str(m)+'/'+ str(uu)
        files = []
        #path = 'venv/cache/2015_cloudtrail/2015/01/08'
        events = []
        d = {}
        #all1 = []
        overall = []
        for r, d, f in os.walk(path):
            for file in f:
                if file.endswith('.json'):
                    files.append(os.path.join(r, file))  
        for index, js in enumerate(files):
            with open(js, 'r') as f:
                datastore = json.load(f)
                for x in range(len(datastore['Records'])):
                    events.append(datastore['Records'][x]['eventName'])
        newevent = {}
        newevent = Counter(events)
        #dd = OrderedDict(sorted(newevent.items(), key=lambda x: x[1]))
        #all1 = []
        all1.append(newevent)
    overall.append(all1)
    orig = collections.Counter()
    for ele in range(0, len(all1)):
        #vv.append(all1[ele])
        orig = orig + all1[ele]
    #for i in all1:
     #   add = orig + i
    nn = {}
    d = {}
    nn = Counter(orig)
    ff = OrderedDict(sorted(nn.items(), key=lambda x: x[1]))
    sorted_dict = sorted(nn.items(), key=operator.itemgetter(1),reverse=True)
    d.update({'EventNames' : sorted_dict[:10] })
    all2.append(d)
    return jsonify(all2)



#get top ten events performed in a month
@app.route('/totalcreate_update_delete_events')
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
def totalcreateevents():
    all1 = []
    all2 = []
    add = {}
    d = {}
    ff = {}
    orig = collections.Counter()
    for uu in range(1,32):
        if uu < 10:
            path = 'venv/cache/2015_cloudtrail/2015/01/0'+ str(uu)
        else:
            path = 'venv/cache/2015_cloudtrail/2015/01/'+ str(uu)
        files = []
        #path = 'venv/cache/2015_cloudtrail/2015/01/08'
        events = []
        d = {}
        #all1 = []
        overall = []
        for r, d, f in os.walk(path):
            for file in f:
                if file.endswith('.json'):
                    files.append(os.path.join(r, file))  
        for index, js in enumerate(files):
            with open(js, 'r') as f:
                datastore = json.load(f)
                for x in range(len(datastore['Records'])):
                    events.append(datastore['Records'][x]['eventName'])
        newevent = {}
        newevent = Counter(events)
        #dd = OrderedDict(sorted(newevent.items(), key=lambda x: x[1]))
        #all1 = []
        all1.append(newevent)
    overall.append(all1)
    orig = collections.Counter()
    for ele in range(0, len(all1)):
        #vv.append(all1[ele])
        orig = orig + all1[ele]
    #for i in all1:
     #   add = orig + i
    nn = {}
    d = {}
    up = []
    dl = []
    h = []
    nn = Counter(orig)
    ff = OrderedDict(sorted(nn.items(), key=lambda x: x[1]))
    hh = [value for key,value in ff.items() if key.startswith("Create")]
    up = [value for key,value in ff.items() if key.startswith("Update")]
    dl = [value for key,value in ff.items() if key.startswith("Delete")]
    d.update({'total_creates' : sum(hh) })
    d.update({'total_updates' : sum(up) })
    d.update({'total_deletes' : sum(dl) })
    all2.append(d)
    return jsonify(all2)



# get the top destination addresses
@app.route('/topdestinationaddresses', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
def topdestinationaddresses():
    #location=request.args.get('location')
    client = boto3.client('ec2', region_name='us-east-1')
    err = {}
    #RunningInstances = []
    regionnames =[]
    #allobjects = {}
    err.update({'message':"400"})
    try:
        val = []
        allstate = []
        rules = []
        response = client.describe_regions()
        jj = list(response['Regions'])
        for i in jj:
            val.append(i.get('RegionName'))
        #regionnames = list(regions)
        for x in range(len(val)):
            b = val[x]
            d = {}
            ec2 = boto3.client('ec2', region_name=b)
            sec_groups = ec2.describe_route_tables()['RouteTables']
            for y in range(len(sec_groups)):
                rul = sec_groups[y]['Routes']
                for i in range(len(rul)):
                    rules.append(rul[i]['DestinationCidrBlock'])                    
                #rules.append(sec_groups[y]['IpPermissionsEgress'])
                #a = val[y]
                #rules =
            nn = {}
            nn = Counter(rules)
            allstate.append(len(rules))
        d1={}
        d1.update({"totaldestinations": nn})
        ll = []
        ll.append(nn)
        return jsonify(ll)
    except ClientError as e:    
        err.update({'Error':e.response['Error']['Code']})
        return jsonify(err)





#get the errors occured in any given month
@app.route('/errors')
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
def errors():
    month=request.args.get('month')
    all1 = []
    all2 = []
    add = {}
    d = {}
    ff = {}
    mon = []
    orig = collections.Counter()
    llist = ['start','jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
    mon = [i for i, j in enumerate(llist) if j == month]
    mo = mon[0]
    m = ("{:02d}".format(mo))
    for uu in range(1,32):
        if uu < 10:
            path = 'venv/cache/2015_cloudtrail/2015/'+str(m)+'/0'+ str(uu)
        else:
            path = 'venv/cache/2015_cloudtrail/2015/'+str(m)+'/'+ str(uu)
        files = []
        #path = 'venv/cache/2015_cloudtrail/2015/01/08'
        events = []
        d = {}
        d1={}
        #all1 = []
        overall = []
        for r, d, f in os.walk(path):
            for file in f:
                if file.endswith('.json'):
                    files.append(os.path.join(r, file))  
        for index, js in enumerate(files):
            with open(js, 'r') as f:
                datastore = json.load(f)
                for x in range(len(datastore['Records'])):
                    if 'errorCode' in (datastore['Records'][x]):
                        d1={}
                        events.append(datastore['Records'][x]['errorCode'])
                        d1.update({"Error Code":datastore['Records'][x]['errorCode'] })
                        d1.update({"Error Message":datastore['Records'][x]['errorMessage'] })
                        overall.append(d1)
        return jsonify(overall)



# to get total rules in all security groups in all regions in an account
@app.route('/totalvolumes', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
def totalvolumes():
    #location=request.args.get('location')
    client = boto3.client('ec2', region_name='us-east-1')
    err = {}
    regionnames =[]
    err.update({'message':"400"})
    try:
        ec2 = boto3.resource('ec2', region_name='us-west-2')
        volumes = ec2.volumes.all() # If you want to list out all volumes
        #volumes = ec2.volumes.filter(Filters=[{'Name': 'status', 'Values': ['in-use']}]) # if you want to list out only attached volumes
        print ([volume for volume in volumes])
        f = []
        f = [volume for volume in volumes]
        return jsonify(len(f))
    except ClientError as e:    
        err.update({'Error':e.response['Error']['Code']})
        return jsonify(err)


# to get total rules in all security groups in all regions in an account
@app.route('/totalprotocols', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
def totalprotocols():
    err = {}
    err.update({'message':"400"})
    try:
        oprotocols = []
        iprotocols = []
        overall = []
        ec2 = boto3.client('ec2',region_name='ap-south-1')
        response = ec2.describe_security_groups()
        #bucketnames = [bucket['Name'] for bucket in response['Buckets']]
        for i in response['SecurityGroups']:
            #d1={}
            #d1.update({"Error Code":datastore['Records'][x]['errorCode'] })
            #d1.update({"Error Message":datastore['Records'][x]['errorMessage'] })
            #overall.append(d1)
            oprotocols = [j['IpProtocol'] for j in i['IpPermissionsEgress']]
            #ocidrips = [k['CidrIp'] for k in j['IpRanges']]
            iprotocols = [j['IpProtocol'] for j in i['IpPermissions']]
            #protocols = oprotocols + iprotocols
            #len(list(set(protocols)))
        return jsonify(iprotocols)
    except ClientError as e:    
        err.update({'Error':e.response['Error']['Code']})
        return jsonify(err)




    
@app.route('/paths')
def contentpaths():
    ec2 = boto3.client('ec2',region_name='ap-south-1')
    ll = []
    response = ec2.describe_security_groups()
    for i in response['SecurityGroups']:
        print ("Security Group Name: "+i['GroupName'])
        print ("the Egress rules are as follows:")
        for j in i['IpPermissionsEgress']:
            print ("IP Protocol: "+j['IpProtocol'])
            for k in j['IpRanges']:
                print ("IP Ranges: "+k['CidrIp'])
                ll.append(j['IpProtocol'])
        print ("The Ingress rules are as follows: ")
        for j in i['IpPermissions']:
            print ("IP Protocol: "+j['IpProtocol'])
            try:
                print ("PORT: "+str(j['FromPort']))
                for k in j['IpRanges']:
                    print ("IP Ranges: "+k['CidrIp'])
            except Exception:
                print ("No value for ports and ip ranges available for this security group")
                continue
        return jsonify(ll)




#get total events in a month
@app.route('/totaleventsinmonth')
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
def totaleventsinmonth():
    all1 = []
    all2 = []
    add = {}
    d = {}
    ff = {}
    orig = collections.Counter()
    for uu in range(1,32):
        if uu < 10:
            path = 'venv/cache/2015_cloudtrail/2015/01/0'+ str(uu)
        else:
            path = 'venv/cache/2015_cloudtrail/2015/01/'+ str(uu)
        files = []
        #path = 'venv/cache/2015_cloudtrail/2015/01/08'
        events = []
        d = {}
        #all1 = []
        overall = []
        for r, d, f in os.walk(path):
            for file in f:
                if file.endswith('.json'):
                    files.append(os.path.join(r, file))  
        for index, js in enumerate(files):
            with open(js, 'r') as f:
                datastore = json.load(f)
                for x in range(len(datastore['Records'])):
                    events.append(datastore['Records'][x]['eventName'])
        newevent = {}
        newevent = Counter(events)
        #dd = OrderedDict(sorted(newevent.items(), key=lambda x: x[1]))
        #all1 = []
        all1.append(newevent)
    overall.append(all1)
    orig = collections.Counter()
    for ele in range(0, len(all1)):
        #vv.append(all1[ele])
        orig = orig + all1[ele]
    #for i in all1:
     #   add = orig + i
    nn = {}
    d = {}
    up = []
    dl = []
    h = []
    nn = Counter(orig)
    ff = OrderedDict(sorted(nn.items(), key=lambda x: x[1]))
    hh = [value for key,value in ff.items()]
    d.update({'total_events' : sum(hh) })
    all2.append(d)
    return jsonify(all2)



# to get total vpcs in all regions in an account
@app.route('/totalvpcs', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
def totalvpcs():
    #location=request.args.get('location')
    client = boto3.client('ec2', region_name='us-east-1')
    err = {}
    #RunningInstances = []
    regionnames =[]
    nacl=[]
    subnet=[]
    #allobjects = {}
    err.update({'message':"400"})
    try:
        val = []
        filters = [{'Name': 'tag:Name', 'Values': ['*'] }]
        allstate = []
        response = client.describe_regions()
        jj = list(response['Regions'])
        for i in jj:
            val.append(i.get('RegionName'))
        #regionnames = list(regions)
        for x in range(len(val)):
            b = val[x]
            d = {}
            ec2 = boto3.client('ec2', region_name=b)
            vpcs = ec2.describe_vpcs()
            nacls = ec2.describe_network_acls()
            subnets = ec2.describe_subnets()
            allstate.append(len(vpcs))
            nacl.append(len(nacls))
            subnet.append(len(subnets))
        d1={}
        d1.update({"totalvpcs":sum(allstate)})
        d1.update({"totalsubnets":sum(subnet)})
        d1.update({"totalnacls":sum(nacl)})
        ll = []
        ll.append(d1)
        return jsonify(ll)
    except ClientError as e:    
        err.update({'Error':e.response['Error']['Code']})
        return jsonify(err)



# to get total subnets in all regions in an account
@app.route('/totalsubnets', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
def totalsubnets():
    #location=request.args.get('location')
    client = boto3.client('ec2', region_name='us-east-1')
    err = {}
    #RunningInstances = []
    regionnames =[]
    #allobjects = {}
    err.update({'message':"400"})
    try:
        val = []
        allstate = []
        response = client.describe_regions()
        jj = list(response['Regions'])
        for i in jj:
            val.append(i.get('RegionName'))
        #regionnames = list(regions)
        for x in range(len(val)):
            b = val[x]
            d = {}
            ec2 = boto3.client('ec2', region_name=b)
            subnets = ec2.describe_subnets()
            allstate.append(len(subnets))
        d1={}
        d1.update({"totalsubnets":sum(allstate)})
        ll = []
        ll.append(d1)
        return jsonify(ll)
    except ClientError as e:    
        err.update({'Error':e.response['Error']['Code']})
        return jsonify(err)



# to get total subnets in all regions in an account
@app.route('/totalnacl', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
def totalnacl():
    #location=request.args.get('location')
    client = boto3.client('ec2', region_name='us-east-1')
    err = {}
    #RunningInstances = []
    regionnames =[]
    #allobjects = {}
    err.update({'message':"400"})
    try:
        val = []
        allstate = []
        response = client.describe_regions()
        jj = list(response['Regions'])
        for i in jj:
            val.append(i.get('RegionName'))
        #regionnames = list(regions)
        for x in range(len(val)):
            b = val[x]
            d = {}
            ec2 = boto3.client('ec2', region_name=b)
            nacls = ec2.describe_network_acls()
            allstate.append(len(nacls))
        d1={}
        d1.update({"totalnacl":sum(allstate)})
        ll = []
        ll.append(d1)
        return jsonify(ll)
    except ClientError as e:    
        err.update({'Error':e.response['Error']['Code']})
        return jsonify(err)



#get total events occured in a day
@app.route('/eventscount')
def eventscount():
    path = 'venv/cache/2015_cloudtrail/2015/01/01'
    path_to_json = 'venv/cache/2015_cloudtrail/2015/01/01'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    files = []
    events = []
    eventtime = []
    username = []
    src = []
    arn = []
    d = {}
    overall = []
    for r, d, f in os.walk(path):
        for file in f:
            if '.json' in file:
                files.append(os.path.join(r, file))         
    for index, js in enumerate(files):
        with open(js, 'r') as f:
            datastore = json.load(f)
            for x in range(len(datastore['Records'])):
                events.append(datastore['Records'][x]['eventName'])
                eventtime.append(datastore['Records'][x]['eventTime'])
                username.append(datastore['Records'][x]['userIdentity']['userName'])
                arn.append(datastore['Records'][x]['userIdentity']['arn'])
                src.append(datastore['Records'][x]['sourceIPAddress'])
        d = {}
        d.update({'TotalEvents' : len(events)})
        overall = []
    overall = []
    overall.append(d)
    return jsonify(overall)
   







#get the errors occured in any given month
@app.route('/totaleventsinaday')
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
def totaleventsinaday():
    month=request.args.get('month')
    day=request.args.get('day')
    all1 = []
    all2 = []
    add = {}    
    d = {}
    ff = {}
    mon = []
    orig = collections.Counter()
    llist = ['start','jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
    mon = [i for i, j in enumerate(llist) if j == month]
    mo = mon[0]
    print(type(day))
    m = ("{:02d}".format(mo))
    da = int(day)
    print(da)
    if da < 10:
        path = 'venv/cache/2015_cloudtrail/2015/'+str(m)+'/0'+ str(da)
    else:
        path = 'venv/cache/2015_cloudtrail/2015/'+str(m)+'/'+ str(da)
    print(path)
    files = []
    events = []
    d = {}
    overall = []
    for r, d, f in os.walk(path):
        for file in f:
            if '.json' in file:
                files.append(os.path.join(r, file))
    for index, js in enumerate(files):
        with open(js, 'r') as f:
            datastore = json.load(f)
            for x in range(len(datastore['Records'])):
                events.append(datastore['Records'][x]['eventName'])
        d = {}
        d.update({'TotalEvents' : len(events)})
    overall = []
    overall.append(d)
    return jsonify(overall)

from smart_open import smart_open

   
    
    
    
@app.route('/readfiless', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
def readfiless():
    #bucket_name_m=request.args.get('bucket')
    #s3_resource = boto3.resource('s3')
    err = {}
    err.update({'message':"400"})
    try:
        with smart_open('s3://bucketsummer/361166629815_CloudTrail_us-east-1_20150101T0000Z_nqSzxQ623cykwe1r.json', 'rb') as s3_source:
            for line in s3_source:
                print(line.decode('utf8'))
                dataa = line.decode('utf8')
        #my_bucket = s3_resource.Bucket('bucketsummer')
        #summaries = my_bucket.objects.all()
        #result = users_schema.dump(summaries)
        #dataa = summaries.get()['Body'].read()
        d1={}
        d1.update({'message':"200"})
        d1.update({'data':dataa})
        return jsonify(d1)
    except ClientError as e:
        err.update({'Error':e.response['Error']['Code']})
        return jsonify(err)
    



#what's the average number of fields across all the .csv files?
@app.route('/csv_quest1')
def csv_quest1():
    path = 'venv/csv_assessment'
    files = []
    num_cols=[]
    for r, d, f in os.walk(path):
        for file in f:
            if '.csv' in file:
                files.append(os.path.join(r, file)) 
    for filename in files:
        df = pd.read_csv(filename, index_col=None, header=0)
        num_cols.append(len(df.columns))
    average_columns= sum(num_cols)/len(num_cols)
    return ' %f' % average_columns

         
#what's the total number or rows for the all the .csv files?
@app.route('/csv_quest2')
def csv_quest2():
    path = 'venv/csv_assessment'
    files = []
    num_rows=[]
    for r, d, f in os.walk(path):
        for file in f:
            if '.csv' in file:
                files.append(os.path.join(r, file)) 
    for filename in files:
        df = pd.read_csv(filename, index_col=None, header=0)
        num_rows.append(df.shape[0] + 1)
    print(num_rows)
    total_rows= sum(num_rows)
    return ' %f' % total_rows
    
    
#what's the total number or rows for the all the .csv files?
@app.route('/csv_quest3')
def csv_quest3():
    path = 'venv/csv_assessment'
    files = []
    num_rows=[]
    for r, d, f in os.walk(path):
        for file in f:
            if '.csv' in file:
                files.append(os.path.join(r, file)) 
    for filename in files:
        df = pd.read_csv(filename, index_col=None, header=0)
        num_rows.append(df.shape[0] + 1)
    print(num_rows)
    total_rows= sum(num_rows)
    return ' %f' % total_rows


if __name__ == '__main__':
    app.run()
