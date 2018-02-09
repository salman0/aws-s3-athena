"""
Uploads mock data to S3 Bucket
"""
import sys
import boto3
import shared as helper

def main():
        # Get configuration from yaml file.
        config = helper.read_config('.config.yml')
        target_bucket = config['S3_SOURCE_BUCKET']

        # Connect to S3 client 
        # http://boto3.readthedocs.io/en/latest/reference/core/session.html#boto3.session.Session.client
        s3_client = boto3.client(
            service_name='s3',
            aws_access_key_id=config['AWS_ACCESS'],
            aws_secret_access_key=config['AWS_SECRET']
        )

        # Create s3 bucket
        # https://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.Client.create_bucket
        s3_client.create_bucket(Bucket=target_bucket)
        
        # Upload data files to s3
        # http://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.Client.upload_file
        s3_client.upload_file('./data/MOCK_DATA.json', target_bucket, 'MOCK_DATA.json')
        s3_client.upload_file('./data/MOCK_DATA.csv', target_bucket, 'MOCK_DATA.csv')
        s3_client.upload_file('./data/MOCK_DATA.tsv', target_bucket, 'MOCK_DATA.tsv')

        # Validate that each object is successfully uploaded into the bucket
        # https://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.Client.list_objects
        for obj in s3_client.list_objects(Bucket=target_bucket)['Contents']:
            assert obj['Key'] in ['MOCK_DATA.json', 'MOCK_DATA.csv', 'MOCK_DATA.tsv']

if __name__ == "__main__":
    sys.exit(main())