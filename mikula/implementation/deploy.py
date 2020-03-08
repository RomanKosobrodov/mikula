import os
import json
import boto3
from mikula.implementation.configure import read_credentials, AWS_REGIONS
from mikula.implementation.util import input_yes_no
import mimetypes as mime


def bucket_exists(s3_resource, bucket_name):
    existing_buckets = [bucket.name for bucket in s3_resource.buckets.all()]
    exists = bucket_name in existing_buckets
    return exists


def empty_bucket(s3_resource, bucket_name):
    bucket = s3_resource.Bucket(bucket_name)
    bucket.objects.all().delete()


def create_bucket(s3_resource, bucket_name, region):
    bucket = s3_resource.Bucket(bucket_name)
    configuration = {'LocationConstraint': region}
    bucket.create(CreateBucketConfiguration=configuration)


def configure_website_bucket(s3_resource, bucket_name):
    website_configuration = {'ErrorDocument': {'Key': 'error.html'},
                             'IndexDocument': {'Suffix': 'index.html'}}

    bucket_website = s3_resource.BucketWebsite(bucket_name)
    bucket_website.put(WebsiteConfiguration=website_configuration)

    cors_configuration = {
        'CORSRules': [{
            'AllowedHeaders': ['Authorization'],
            'AllowedMethods': ['GET'],
            'AllowedOrigins': ['*'],
            'ExposeHeaders': ['GET'],
            'MaxAgeSeconds': 3000
        }]
    }

    bucket_cors = s3_resource.BucketCors(bucket_name)
    bucket_cors.put(CORSConfiguration=cors_configuration)

    policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Sid": "PublicReadForGetBucketObjects",
            "Effect": "Allow",
            "Principal": "*",
            "Action": ["s3:GetObject"],
            "Resource": [f"arn:aws:s3:::{bucket_name}/*"]
        }
        ]
    }
    policy_string = json.dumps(policy)

    bucket_policy = s3_resource.BucketPolicy(bucket_name)
    bucket_policy.put(Policy=policy_string)


def upload_gallery(gallery, s3_resource, bucket_name):
    s3_bucket_object = s3_resource.Bucket(bucket_name)
    print(f'Uploading files to "{bucket_name}"')
    for subdir, dirs, files in os.walk(gallery):
        for file in files:
            full_path = os.path.join(subdir, file)
            mime_type = mime.guess_type(full_path)
            with open(full_path, 'rb') as data:
                key = full_path[len(gallery) + 1:]
                print(f'"{key}" - "{mime_type[0]}"')
                s3_bucket_object.put_object(Key=key,
                                            Body=data,
                                            ACL="public-read",
                                            ContentType=mime_type[0])


def deploy(bucket, region):
    gallery = os.path.join(os.getcwd(), "build")
    if not os.path.isdir(gallery):
        print("The gallery has not been built yet.")
        print("Use 'mikula build' to generate your gallery and `mikula serve` to test it locally.")
        return

    credentials = read_credentials()
    s3 = boto3.resource('s3',
                        aws_access_key_id=credentials["aws_access_key_id"],
                        aws_secret_access_key=credentials["aws_secret_access_key"])

    if bucket_exists(s3, bucket_name=bucket):
        confirmed = input_yes_no(f"Bucket '{bucket}' already exists. All content in this bucket will be deleted. "
                                 f"Is this OK?")
        if not confirmed:
            return
        empty_bucket(s3, bucket_name=bucket)
    else:
        create_bucket(s3, bucket, region)

    configure_website_bucket(s3, bucket_name=bucket)
    upload_gallery(gallery, s3, bucket_name=bucket)
    url = f"http://{bucket}.s3-website-{region}.amazonaws.com"
    print("\nWebsite deployed successfully")
    print(f"It is available at {url}")
