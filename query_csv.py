#!/usr/bin/env python3
"""
Execute queries against csv files
"""
import boto3

def execute_query(query, database, s3_output):
    """Execute the Athena query"""
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

#Athena configuration
s3_input = 's3://athena-test-bucket-1234242/data/'
s3_ouput = 's3://athena-test-bucket-1234242/results/'
database = 'default'
table = 'csvtable'

#Athena database and table definition
create_database = """
    CREATE DATABASE IF NOT EXISTS %s;
""" % (database)

#create_database = "CREATE DATABASE IF NOT EXISTS %s;" % (database)
create_table = \
"""
CREATE EXTERNAL TABLE IF NOT EXISTS %s.%s(
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
  %s
""" % ( database, table, s3_input )
#Query definitions
query_1 = "SELECT * FROM %s.%s where gender='Female';" % (database, table)

#Execute all queries
queries = [ create_database, create_table, query_1 ]
for q in queries:
   print("Executing query: %s" % (q))
   result = execute_query(q, database, s3_ouput)

