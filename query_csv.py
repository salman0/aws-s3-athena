#!/usr/bin/env python3
"""
Execute queries against csv files
"""
import sys
import time
import boto3
import shared as helper

def execute_query(query, database, s3_output):
    """Execute the Athena query"""
    print("Executing query: %s" % (query))
    client = boto3.client('athena')
    response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': database
            },
        ResultConfiguration={
            'OutputLocation': s3_output,
            }
        )
    print('Execution ID: ' + response['QueryExecutionId'])
    return response

def create_database(database_name, s3_output):
  """Create database"""
  query = "CREATE DATABASE IF NOT EXISTS %s;" % (database_name)
  execute_query(query=query, database=database_name, s3_output=s3_output)

def create_table(database_name, table_name, s3_input, s3_output):
  """Create table for database based on MOCK_DATA.csv schema"""
  query = \
  """CREATE EXTERNAL TABLE `%s`(
      `id` bigint, 
      `first_name` string, 
      `last_name` string, 
      `email` string, 
      `gender` string, 
      `is_active` boolean, 
      `joined_date` string)
    ROW FORMAT DELIMITED 
      FIELDS TERMINATED BY ',' 
    STORED AS INPUTFORMAT 
      'org.apache.hadoop.mapred.TextInputFormat' 
    OUTPUTFORMAT 
      'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
    LOCATION
      '%s'
    TBLPROPERTIES (
      'classification'='csv', 
      'delimiter'=',', 
      'skip.header.line.count'='1');
  """ % ( table_name, s3_input )
  execute_query(query=query, database=database_name, s3_output=s3_output)

def main():
  database_name = "default"
  table_name = "test_csv_table"

  config = helper.read_config('.config.yml')
  bucket_name = config['S3_SOURCE_BUCKET']
  s3_input = f's3://{bucket_name}/data/'
  s3_output = f's3://{bucket_name}/results/'

  # Setup database and tables
  create_database(database_name=database_name, s3_output=s3_output)
  create_table(database_name=database_name, table_name=table_name, s3_input=s3_input, s3_output=s3_output)
  time.sleep(1)

  # Execute example query
  query = "SELECT gender, COUNT(1) FROM %s.%s GROUP BY gender;" % (database_name, table_name)
  execute_query(query=query, database=database_name, s3_output=s3_output)

if __name__ == "__main__":
    sys.exit(main())

