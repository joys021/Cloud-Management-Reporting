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

-get filename

-calculate the recency in minutes

-if less than 60 minutes:

      -send the file from cache
      
-else:
   
   -call the original API

-save data to file

-return the new file

### 13. API URL :[Count of encrypted buckets](http://127.0.0.1:5000/bucketencryptiondetails)
**Purpose:** This API gets the count of encrypted and unencrypted buckets
Following is the sample output
```[
  {
    "count": 2, 
    "type": "encrypted"
  }, 
  {
    "count": 8, 
    "type": "unencrypted"
  }
]
```


### 14. API URL : [Count of objects in each bucket](http://127.0.0.1:5000/allcount)
**Purpose:** This API gets the count of objects in each bucket\
Following is the sample output
```[
  {
    "bucket": "addbucketeu", 
    "objectscount": 0
  }, 
  {
    "bucket": "eighteighthe", 
    "objectscount": 2
  }, 
  {
    "bucket": "fivefifth", 
    "objectscount": 3
  }, 
  {
    "bucket": "fourfourth", 
    "objectscount": 1
  }, 
  {
    "bucket": "nineninth", 
    "objectscount": 1
  }, 
  {
    "bucket": "onefirstone", 
    "objectscount": 0
  }, 
  {
    "bucket": "sevenseventh", 
    "objectscount": 2
  }, 
  {
    "bucket": "sixsixth", 
    "objectscount": 4
  }, 
  {
    "bucket": "tenthone", 
    "objectscount": 5
  }, 
  {
    "bucket": "twosecondtwo", 
    "objectscount": 1
  }
]
```


### 15. API URL : [Size of each bucket](http://127.0.0.1:5000/bucketsize)
**Purpose:** This API gets the size of each bucket in KB
Following is the sample output
```[
  {
    "bucket": "addbucketeu", 
    "size": 0.0
  }, 
  {
    "bucket": "eighteighthe", 
    "size": 19.6953125
  }, 
  {
    "bucket": "fivefifth", 
    "size": 19.783203125
  }, 
  {
    "bucket": "fourfourth", 
    "size": 265.015625
  }, 
  {
    "bucket": "nineninth", 
    "size": 265.015625
  }, 
  {
    "bucket": "onefirstone", 
    "size": 265.015625
  }, 
  {
    "bucket": "sevenseventh", 
    "size": 323.515625
  }, 
  {
    "bucket": "sixsixth", 
    "size": 382.015625
  }, 
  {
    "bucket": "tenthone", 
    "size": 705.53125
  }, 
  {
    "bucket": "twosecondtwo", 
    "size": 705.53125
  }
]
```

### 16. API URL : [Count of intances in different states](http://127.0.0.1:5000/instancestate)
**Purpose:** This API gets the count of instances in differnt states from all regions of an account
Following is the sample output
```[
  {
    "count": 0, 
    "type": "pending"
  }, 
  {
    "count": 1, 
    "type": "running"
  }, 
  {
    "count": 0, 
    "type": "stopping"
  }, 
  {
    "count": 1, 
    "type": "stopped"
  }, 
  {
    "count": 0, 
    "type": "shutting-down"
  }, 
  {
    "count": 0, 
    "type": "terminated"
  }
]
```


### 17. API URL : [Count of Instances in each region](http://127.0.0.1:5000/instancestate)
**Purpose:** This API gets count of instances present in each region of an account
Following is the sample output
```[
  {
    "instancescount": 0, 
    "region": "eu-north-1"
  }, 
  {
    "instancescount": 0, 
    "region": "ap-south-1"
  }, 
  {
    "instancescount": 0, 
    "region": "eu-west-3"
  }, 
  {
    "instancescount": 0, 
    "region": "eu-west-2"
  }, 
  {
    "instancescount": 0, 
    "region": "eu-west-1"
  }, 
  {
    "instancescount": 0, 
    "region": "ap-northeast-2"
  }, 
  {
    "instancescount": 0, 
    "region": "ap-northeast-1"
  }, 
  {
    "instancescount": 0, 
    "region": "sa-east-1"
  }, 
  {
    "instancescount": 0, 
    "region": "ca-central-1"
  }, 
  {
    "instancescount": 0, 
    "region": "ap-southeast-1"
  }, 
  {
    "instancescount": 0, 
    "region": "ap-southeast-2"
  }, 
  {
    "instancescount": 0, 
    "region": "eu-central-1"
  }, 
  {
    "instancescount": 1, 
    "region": "us-east-1"
  }, 
  {
    "instancescount": 0, 
    "region": "us-east-2"
  }, 
  {
    "instancescount": 0, 
    "region": "us-west-1"
  }, 
  {
    "instancescount": 0, 
    "region": "us-west-2"
  }
]
```
### 18. API URL : [Event details recorded in Cloud trial for a day](http://127.0.0.1:5000/instancestate)
**Purpose:** This API gives the details of the events recorded in a day.
Following is the sample output
```[
  {
    "ARN": [
      "arn:aws:iam::361166629815:root", 
      "arn:aws:iam::361166629815:root", 
      "arn:aws:iam::361166629815:root", 
      "arn:aws:iam::361166629815:root", 
      "arn:aws:iam::361166629815:root", 
      "arn:aws:iam::361166629815:root", 
      "arn:aws:iam::361166629815:root", 
      "arn:aws:iam::361166629815:root", 
      "arn:aws:iam::361166629815:root"
    ], 
    "EventNames": [
      "DescribeScalingActivities", 
      "DescribeAutoScalingGroups", 
      "DescribeScalingActivities", 
      "DescribeInstanceHealth", 
      "DescribeScalingActivities", 
      "DescribeAutoScalingGroups", 
      "DescribeScalingActivities", 
      "DescribeInstanceHealth", 
      "DescribeScalingActivities"
    ], 
    "Eventtime": [
      "2014-12-31T23:57:26Z", 
      "2014-12-31T23:56:25Z", 
      "2014-12-31T23:55:24Z", 
      "2014-12-31T23:57:26Z", 
      "2014-12-31T23:56:25Z", 
      "2014-12-31T23:57:26Z", 
      "2014-12-31T23:57:26Z", 
      "2014-12-31T23:56:25Z", 
      "2014-12-31T23:56:25Z"
    ], 
    "SourceIPAddress": [
      "elasticbeanstalk.amazonaws.com", 
      "elasticbeanstalk.amazonaws.com", 
      "elasticbeanstalk.amazonaws.com", 
      "elasticbeanstalk.amazonaws.com", 
      "elasticbeanstalk.amazonaws.com", 
      "elasticbeanstalk.amazonaws.com", 
      "elasticbeanstalk.amazonaws.com", 
      "elasticbeanstalk.amazonaws.com", 
      "elasticbeanstalk.amazonaws.com"
    ], 
    "Username": [
      "mw-internal", 
      "mw-internal", 
      "mw-internal", 
      "mw-internal", 
      "mw-internal", 
      "mw-internal", 
      "mw-internal", 
      "mw-internal", 
      "mw-internal"
    ]
  }
]
```


### 19. API URL : [Total rules](http://127.0.0.1:5000/totalrules)
**Purpose:** This API gives the total number of rules in all security groups in all regions.
Following is the sample output
```[
  {
    "totalrules": 44
  }
]
```

### 20. API URL : [Total security groups](http://127.0.0.1:5000/totalsecuritygroups)
**Purpose:** This API gives the total number of security groups in all regions.
Following is the sample output
```[
  {
    "totalsecuritygroups": 22
  }
]
```


### 21. API URL : [Top ten events in a day](http://127.0.0.1:5000/toptenevents)
**Purpose:** This API gives the top ten events happened in a day.
Following is the sample output
```[
  {
    "EventNames": [
      [
        "DescribeScalingActivities", 
        224
      ], 
      [
        "DescribeInstanceHealth", 
        122
      ], 
      [
        "DescribeAutoScalingGroups", 
        121
      ], 
      [
        "DescribeReservedInstances", 
        4
      ], 
      [
        "DescribeTags", 
        3
      ], 
      [
        "DescribeInstances", 
        3
      ], 
      [
        "DescribeVolumes", 
        1
      ]
    ]
  }
]
```



### 22. API URL : [Top ten events in a month](http://127.0.0.1:5000/topteneventsinamonth)
**Purpose:** This API gives the top ten events happened in a month.
Following is the sample output
```[
  {
    "EventNames": [
      [
        "DescribeScalingActivities", 
        7801
      ], 
      [
        "DescribeAutoScalingGroups", 
        4327
      ], 
      [
        "DescribeInstanceHealth", 
        4000
      ], 
      [
        "DescribeAlarms", 
        2362
      ], 
      [
        "DescribeVolumes", 
        1393
      ], 
      [
        "DescribeLoggingStatus", 
        1245
      ], 
      [
        "DescribeVolumeStatus", 
        1179
      ], 
      [
        "DescribeClusters", 
        1153
      ], 
      [
        "DescribeTags", 
        644
      ], 
      [
        "DescribeEvents", 
        633
      ]
    ]
  }
]
```


### 23. API URL : [Total create, update and delete events](http://127.0.0.1:5000/totalcreate_update_delete_events)
**Purpose:** This API gives the total number of screate, update and delete events happened in a month.
Following is the sample output
```[
  {
    "total_creates": 154, 
    "total_deletes": 168, 
    "total_updates": 2
  }
]
```


### [HTML Code for Dashboard](https://github.com/joys021/Flask/blob/master/s3Dashboard.html)


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


