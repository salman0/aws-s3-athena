#!/usr/bin/python3
"""
Delete contents of bucket and then the bucket
"""

import sys
import boto3
from botocore.exceptions import ClientError
import shared as helper


def main():
    config = helper.read_config('.config.yml')
    s3_client = boto3.resource(
        service_name='s3',
        aws_access_key_id=config['AWS_ACCESS'],
        aws_secret_access_key=config['AWS_SECRET']
    )

    try:
        # Connect to bucket
        # http://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.Bucket.objects
        bucket = s3_client.Bucket(config['S3_SOURCE_BUCKET'])

        # Access bucket and delete contents
        bucket.objects.all().delete()

        # Ensure that the objects have been deleted
        assert len(list(bucket.objects.all())) == 0

        # Delete the bucket
        bucket.delete()

    except ClientError as e:
        # Don't throw error if the bucke is already deleted
        if e.response['Error']['Code'] != 'NoSuchBucket':
            print("Unexpected error: %s" % e)
    finally:
        # Ensure that the bucket isn't there in either case
        # http://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.Client.list_buckets
        for current_bucket in s3_client.buckets.all():
            assert current_bucket.name != config['S3_SOURCE_BUCKET']

if __name__ == "__main__":
    sys.exit(main())
