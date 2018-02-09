# aws-s3-athena
Example scripts for working with AWS S3 and Athena

## Usage

### Install requirements

```bash
pip install -r requirements.txt
```

### Update .config.yml

```yaml
AWS_ACCESS: AWS_ACCESS_KEY
AWS_SECRET: AWS_SECRET_KEY
BUCKET_NAME: athena-test-bucket
```

### Create bucket and upload data to S3

```bash
python setup.py
```

### Remove files loaded into S3 and delete bucket

```bash
python teardown.py
``` 

## References

- Generating Mock Data - Mockaroo
  - https://www.mockaroo.com/
- Boto3 Documentation
  - http://boto3.readthedocs.io/en/latest/guide/quickstart.html#configuration 
- AWS Big Data Blog: Analyzing Data in S3 using Amazon Athena 
  - https://aws.amazon.com/blogs/big-data/analyzing-data-in-s3-using-amazon-athena/
- Medium Article: Automating AWS Athena batch jobs with Python 3
  - https://medium.com/@devopsglobaleli/introduction-17b4d0c592b6

