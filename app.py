from flask import Flask, render_template, flash, request,json
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask import Flask,render_template, jsonify
from flask_bootstrap import Bootstrap
from flask_marshmallow import Marshmallow
import boto3, requests
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
from datetime import timedelta
from datetime import datetime
from time import gmtime, strftime
from flask import send_file
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
            del d["ttt"]
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
            d.update( {'type' : b} )
            my_bucket = s3_resource.Bucket(b)
            mybucs = [file.key for file in my_bucket.objects.all()]
            lengh = len(mybucs)
            #for file in mybucs:
            #    d.setdefault("Filenames", []).append(file)
            d.update( {'buckets' : lengh} )
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
        filestat = os.stat(file_name)
        date_format = "%Y-%m-%d %H:%M:%S"
        d2 = "%Y-%m-%d %H:%M:%S.%f"
        date = time.localtime((filestat.st_mtime))
        modTimesinceEpoc = os.path.getmtime(file_name)
        presenttime = str(datetime.now())
        modificationTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modTimesinceEpoc))
        time1  = datetime.strptime(modificationTime, date_format)
        time2  = datetime.strptime(presenttime, d2)
        diff = time2 - time1
        diffinminutes = (diff.seconds) / 60
        if onehour > diffinminutes:
            return send_file('cache/'+file_name, attachment_filename=file_name)
        else:
            items = requests.get('http://127.0.0.1:5000/'+file_name)
            data = items.json()
            with open(file_name, 'w') as f:
                json.dump(data, f)
        d1 = {}
        d1.update({'message':"200"})
        d1.update({'last modified time':modificationTime})
        d1.update({'present time':presenttime})
        d1.update({'diff in minutes':str(minutes)})
        ll = []
        ll.append(d1)
        return send_file(file_name, attachment_filename=file_name)
    except ClientError as e:
        err.update({'Error':e.response['Error']['Code']})
        return jsonify(err)



@app.route('/savefiles', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True,origin='*', methods = ['GET','POST','OPTIONS'])
@cross_origin(headers=['Content-Type'])
def saveallfiles():
    #location=request.args.get('location')
    s3 = boto3.client("s3")
    err = {}
    err.update({'message':"400"})
    try:
        items = requests.get('http://127.0.0.1:5000/allbuckets') # (your url)
        data = items.json()
        with open('venv/cache/allbuckets.json', 'w') as f:
            json.dump(data, f)
        item2 = requests.get('http://127.0.0.1:5000/allcount') # (your url)
        data = item2.json()
        with open('venv/cache/objectcounts.json', 'w') as f:
            json.dump(data, f)
        d1={}
        d1.update({'message':"200"})
        d1.update({'data':"Saved file Successfully"})
        ll = []
        ll.append(d1)
        return jsonify(ll)
    except ClientError as e:
        err.update({'Error':e.response['Error']['Code']})
        return jsonify(err)






if __name__ == '__main__':
    app.run()

    
