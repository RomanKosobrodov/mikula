import os
import json
import boto3
from mikula.implementation.configure import read_credentials, AWS_REGIONS
from mikula.implementation.util import input_yes_no


def bucket_exists(client, bucket_name):
    response = client.list_buckets()
    return bucket_name in response["Buckets"]


def delete_bucket(client, bucket_name):
    bucket = client.Bucket(bucket_name)
    for key in bucket.objects.all():
        key.delete()
    bucket.delete()


def create_website_bucket(client, bucket_name, region):
    bucket_configuration = {'LocationConstraint': region}
    client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=bucket_configuration)

    website_configuration = {'ErrorDocument': {'Key': 'error.html'},
                             'IndexDocument': {'Suffix': 'index.html'}}
    client.put_bucket_website(Bucket=bucket_name,
                              WebsiteConfiguration=website_configuration)

    cors_configuration = {
        'CORSRules': [{
            'AllowedHeaders': ['Authorization'],
            'AllowedMethods': ['GET'],
            'AllowedOrigins': ['*'],
            'ExposeHeaders': ['GET'],
            'MaxAgeSeconds': 3000
        }]
    }
    client.put_bucket_cors(Bucket=bucket_name,
                           CORSConfiguration=cors_configuration)

    bucket_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Sid": "AddPerm",
            "Effect": "Allow",
            "Principal": "*",
            "Action": ["s3:GetObject"],
            "Resource": f"arn:aws:s3:::{bucket_name}/*"
        }]
    }
    bucket_policy = json.dumps(bucket_policy)
    client.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)

    return client.Bucket(bucket_name)


def upload_gallery(gallery, s3_bucket_object):
    for subdir, dirs, files in os.walk(gallery):
        for file in files:
            full_path = os.path.join(subdir, file)
            with open(full_path, 'rb') as data:
                s3_bucket_object.put_object(Key=full_path[len(gallery) + 1:], Body=data)


def deploy(gallery, bucket, region):
    if bucket is None:
        bucket = os.path.basename(gallery)

    credentials = read_credentials()
    if region in AWS_REGIONS:
        credentials["region"] = region

    s3 = boto3.client('s3',
                      aws_access_key_id=credentials["aws_access_key_id"],
                      aws_secret_access_key=credentials["aws_secret_access_key"])

    if bucket_exists(s3, bucket):
        confirmed = input_yes_no(f"Bucket {bucket} already exists and will be deleted with all its content. "
                                 f"Is this OK?")
        if not confirmed:
            return
        delete_bucket(s3, bucket)

    gallery_bucket = create_website_bucket(s3, bucket, credentials.get("region", "us-east-1"))
    upload_gallery(gallery, gallery_bucket)


if __name__ == "__main__":
    deploy("sample", "target.bucket", "unknown")
