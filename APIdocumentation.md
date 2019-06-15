### 1. API URL:[Home Page](http://127.0.0.1:5000/)

**Purpose:** This acts like a home page

Following is the sample output:
```
Hello, Bootstrap
```

### 2. API URL: [All buckets in an account](http://127.0.0.1:5000/buckets)
**Purpose:** This API will list all buckets in an account. This will not show the files within a bucket. 

Following is the sample output.

```{
  "data": {
    "Buckets": [
      {
        "CreationDate": "Thu, 06 Jun 2019 22:24:04 GMT", 
        "Name": "botflas"
      }, 
      {
        "CreationDate": "Sun, 19 May 2019 20:55:34 GMT", 
        "Name": "botflaskproj"
      }, 
      {
        "CreationDate": "Wed, 15 May 2019 13:09:24 GMT", 
        "Name": "flasksummerproj"
      }, 
      {
        "CreationDate": "Thu, 06 Jun 2019 21:45:09 GMT", 
        "Name": "iinnppuutloc"
      }, 
      {
        "CreationDate": "Wed, 05 Jun 2019 14:53:46 GMT", 
        "Name": "inputloc"
      }
    ], 
    "Owner": {
      "DisplayName": "joys021", 
      "ID": "3d1ece2b6f62d28d74b805dc7a17d70c325e04d12bb6e066ca01a0a4c8c15877"
    }
  }, 
  "message": "200"
}
```

### 3. API URL : [Details of an object](http://127.0.0.1:5000/objectdetails)
**Purpose:** This API displays the details of an object that is given in a given bucket including encryption details. That is, when a bucket name and file name is given, it would display the detials of the file.

Following is the sample output:
```{
  "data": {
    "bucket_name": "flasksummerproj", 
    "key": "Hello_flask.py", 
    "last_modified": "2019-05-15T13:11:08+00:00", 
    "server_side_encryption": null, 
    "sse_customer_algorithm": null, 
    "sse_customer_key_md5": null, 
    "ssekms_key_id": null
  }, 
  "message": "200"
}
```

### 4. API URL : [List details of all files in a bucket](http://127.0.0.1:5000/listfilesinabucket)
**Purpose :** This API displays the details of all the files in a bucket that is given
**Bucket name passed as parameter** - http://127.0.0.1:5000/listfilesparam?bucket=flasksummerproj
Following is the sample output:
```
{
  "data": [
    {
      "bucket_name": "flasksummerproj", 
      "key": "Hello_flask.py", 
      "last_modified": "2019-05-15T13:11:08+00:00", 
      "size": 547
    }, 
    {
      "bucket_name": "flasksummerproj", 
      "key": "bull.png", 
      "last_modified": "2019-06-02T22:00:07+00:00", 
      "size": 20168
    }
  ], 
  "message": "200"
}
```

### 5. API URL : [List all buckets and files](http://127.0.0.1:5000/all)
**Purpose :** This API displays all the buckets and files in it

Following is the sample output:
```
{
  "data": [
    {
      "Bucket": "botflas"
    }, 
    {
      "Bucket": "botflaskproj", 
      "Filenames": [
        "Sample.txt"
      ]
    }, 
    {
      "Bucket": "flasksummerproj", 
      "Filenames": [
        "Hello_flask.py", 
        "bull.png"
      ]
    }, 
    {
      "Bucket": "iinnppuutloc"
    }, 
    {
      "Bucket": "inputloc"
    }
  ], 
  "message": "200"
}
```

### 6. API URL : [Create Bucket](http://127.0.0.1:5000/copyinputbucketname)
**Purpose :** This API creates the bucket when bucket name and location is given
**Bucket name and location passed as parameters in url ** - http://127.0.0.1:5000/createbucketparam?bucket=uutloc&location=us-west-1

Following is the sample output:

```
{
  "data": "Created Bucket Successfully", 
  "message": "200"
}
```
Error Response:
```
{
  "Error": "BucketAlreadyOwnedByYou", 
  "message": "400"
}
```

### 7. API URL : [Encrypt Single Bucket](http://127.0.0.1:5000/encryptsinglebucket)
Purpose: This API encrypts the object in a bucket using "AES256" whose details are given to the encryption function

Following is the sample output:

```
{
  "data": "Bucket encrypted Successfully", 
  "message": "200"
}
```

### 8. API URL : [Encrypt All buckets](http://127.0.0.1:5000/encryptallbuckets)
**Purpose:** This API encrypts all the buckets in an account using AES256 algorithm.

Following is the sample output:
```
{
  "data": "All the Buckets are encrypted Successfully", 
  "message": "200"
}
```


### 9. API URL : [Filter buckets based on location](http://127.0.0.1:5000/filteronlocation)
**Purpose:** This API displays the buckets in any particular region
**Location passed as parameter in the url ** - http://127.0.0.1:5000/filteronlocationparam?location=us-west-2
Following is the sample output:
```
{
  "data": {
    "Bucket": "inputloc"
  }, 
  "message": "200"
}
```

### 10. API URL : [Count of files in all buckets](http://127.0.0.1:5000/allcount)
**Purpose:** This API displays the number of files stored in each bucket of an account
Following is the sample output:
```[
  {
    "buckets": 2, 
    "bucketname": "eighteighthe"
  }, 
  {
    "buckets": 3, 
    "bucketname": "fivefifth"
  }, 
  {
    "buckets": 1, 
    "bucketname": "fourfourth"
  }, 
  {
    "buckets": 1, 
    "bucketname": "nineninth"
  }, 
  {
    "buckets": 0, 
    "bucketname": "onefirstone"
  }, 
  {
    "buckets": 2, 
    "bucketname": "sevenseventh"
  }, 
  {
    "buckets": 4, 
    "bucketname": "sixsixth"
  }, 
  {
    "buckets": 5, 
    "bucketname": "tenthone"
  }, 
  {
    "buckets": 1, 
    "bucketname": "twosecondtwo"
  }
]
```
### 11. API URL : [Count of buckets in each region](http://127.0.0.1:5000/regionsofbuckets)
**Purpose:** This API displays the number of buckets stored in each region
Following is the sample output
```[
  {
    "buckets": 1, 
    "region": "eu-west-1"
  }, 
  {
    "buckets": 3, 
    "region": "ap-northeast-2"
  }, 
  {
    "buckets": 2, 
    "region": "sa-east-1"
  }, 
  {
    "buckets": 3, 
    "region": "us-west-2"
  }
]
```
### 12. API URL : [Get Files from Cache](http://127.0.0.1:5000/getfile?filename=allcount.json)
**Purpose:** This API does the following steps

get filename

calculate the recency in minutes

if less than 60 minutes:

send the file from cache

else:

call the original API

save data to file

return the new file


### [HTML Code for Dashboard](https://github.com/joys021/Flask/blob/master/Dashboard.html)



# Few APIs that would perform basic functions

### * API URL: http://127.0.0.1:5000/files?bucket=flasksummerproj 
**Purpose:** This display the details of the files in a particular bucket that is passed in the url

Following is the sample output:
```[
  {
    "bucket_name": "flasksummerproj", 
    "key": "Hello_flask.py", 
    "last_modified": "2019-05-15T13:11:08+00:00", 
    "size": 547
  }
]
```

### * API URL : http://127.0.0.1:5000/createbucket
**Purpose:** This API creates a new bucket with the details given

### * API URL : http://127.0.0.1:5000/allbuckets
**Purpose :** This API displays the list of bucket names in an account

Following is the sample output:
```
{
  "Buckets": [
    "botflaskproj", 
    "flasksummerproj"
  ]
}
```
