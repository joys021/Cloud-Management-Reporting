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
  "Buckets": [
    {
      "CreationDate": "Sun, 19 May 2019 20:55:34 GMT", 
      "Name": "botflaskproj"
    }, 
    {
      "CreationDate": "Wed, 15 May 2019 13:09:24 GMT", 
      "Name": "flasksummerproj"
    }
  ], 
  "Owner": {
    "DisplayName": "joys021", 
    "ID": "3d1ece2b6f62d28d74b805dc7a17d70c325e04d12bb6e066ca01a0a4c8c15877"
  }
}
```

### 3. API URL : [Details of an object](http://127.0.0.1:5000/objectdetails)
**Purpose:** This API displays the details of an object that is given in a given bucket including encryption details. That is, when a bucket name and file name is given, it would display the detials of the file.

Following is the sample output:
```{
  "bucket_name": "flasksummerproj", 
  "key": "Hello_flask.py", 
  "last_modified": "2019-05-15T13:11:08+00:00", 
  "server_side_encryption": null, 
  "sse_customer_algorithm": null, 
  "sse_customer_key_md5": null, 
  "ssekms_key_id": null
}
```

### 4. API URL : [List details of all files in a bucket](http://127.0.0.1:5000/listfilesinabucket)
**Purpose :** This API displays the details of all the files in a bucket that is given

Following is the sample output:
```
[
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
]
```

### 5. API URL : [List all buckets and files](http://127.0.0.1:5000/all)
**Purpose :** This API displays all the buckets and files in it

Following is the sample output:
```
[
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
  }
]
```

### 6. API URL : [Create Bucket](http://127.0.0.1:5000/copyinputbucketname)
**Purpose :** This API creates the bucket when bucket name and location is given

Following is the sample output:

```
Created the Bucket Successfully
```
Error Response:
```
{
  "Error": {
    "BucketName": "inputloc", 
    "Code": "BucketAlreadyOwnedByYou", 
    "Message": "Your previous request to create the named bucket succeeded and you already own it."
    
  }, 
  "ResponseMetadata": {
    "HTTPHeaders": {
      "content-type": "application/xml", 
      "date": "Wed, 05 Jun 2019 14:53:51 GMT", 
      "server": "AmazonS3", 
      "transfer-encoding": "chunked", 
      "x-amz-bucket-region": "us-west-2", 
      "x-amz-id-2": "ENe7yjdKHRyhCAcIsFOmnWjhfUYIjQ0LY7K+jSKE5LwHhE08eWZeflcT0goazcsW7Fzci4BJVCs=", 
      "x-amz-request-id": "99D1349CDEBC081C"
    }, 
    "HTTPStatusCode": 409, 
    "HostId": "ENe7yjdKHRyhCAcIsFOmnWjhfUYIjQ0LY7K+jSKE5LwHhE08eWZeflcT0goazcsW7Fzci4BJVCs=", 
    "RequestId": "99D1349CDEBC081C", 
    "RetryAttempts": 1
  }
}
```

### 7. API URL : [Encrypt Single Bucket](http://127.0.0.1:5000/encryptsinglebucket)
Purpose: This API encrypts the object in a bucket using "AES256" whose details are given to the encryption function

Following is the sample output:

```
Encrypted the bucket Successfully
```

### 8. API URL : [Encrypt All buckets](http://127.0.0.1:5000/encryptallbuckets)
**Purpose:** This API encrypts all the buckets in an account using AES256 algorithm.

Following is the sample output:
```
All the buckets are encrypted Sucessfully
```


### 9. API URL : [Filter buckets based on location](http://127.0.0.1:5000/filteronlocation)
**Purpose:** This API displays the buckets in any particular region

Following is the sample output:
```
{
  "Bucket": "botflaskproj"
}
```



# Few APIs that would perform basic functions

### * API URL: http://127.0.0.1:5000/files 
**Purpose:** This display the details of the files in a particular bucket

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
