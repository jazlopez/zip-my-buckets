# zip-my-buckets | S3 backup tool

--

S3 Backup and restore utility

##### 1.1 GENERAL USAGE

```
usage: s3.backup.restore.py [-h] --run {backup,restore} --table-name
                                  TABLE_NAME [--archive ARCHIVE] --profile
                                  PROFILE [--timeout TIMEOUT]
                                  [--region-name REGION_NAME]
                                  [--with-endpoint WITH_ENDPOINT]

s3 Backup Restore Tool

optional arguments:
  -h, --help            show this help message and exit
  --run {backup,restore}
                        Specify the operation to perform
  --table-name TABLE_NAME
                        Provide table name to backup/restore
  --archive ARCHIVE     When operating in restore mode: absolute path to zip
                        file to restore
  --profile PROFILE     AWS profile authorization
  --timeout TIMEOUT     Timeout
  --region-name REGION_NAME
                        AWS region name
  --with-endpoint WITH_ENDPOINT
                        Optional: Dynamodb URL endpoint

```

#####  1.1.1 Create a zip file from given bucket name
```
python s3.backup.restore.py --run backup --bucket-name 001 --profile default 

```

#####  1.1.2 Create a zip file from given bucket name (s3 localhost instance)
```
python s3.backup.restore.py --run backup --bucket-name 001 --with-endpoint http://localhost:4572 --profile default
```

#####  1.1.3 Restore a zip file into given bucket name
```
python s3.backup.restore.py --run restore --archive foo.zip --bucket-name 001 --profile default 

```
