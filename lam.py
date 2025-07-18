import json
import boto3
import csv
import os
from io import StringIO

# Initialize RDS client
rds_client = boto3.client('rds-data')

# Environment variables
DATABASE_ARN = os.environ['DATABASE_ARN']
SECRET_ARN = os.environ['SECRET_ARN']
DATABASE_NAME = os.environ['DATABASE_NAME']

def lambda_handler(event, context):
    # Get the CSV file from the event
    csv_file = event['body']
    
    # Parse CSV
    csv_data = StringIO(csv_file)
    reader = csv.DictReader(csv_data)
    
    # Prepare SQL statement
    sql = "INSERT INTO users (user_id, email, monthly_income, credit_score, employment_status, age) VALUES (:user_id, :email, :monthly_income, :credit_score, :employment_status, :age)"
    
    for row in reader:
        # Execute SQL statement
        response = rds_client.execute_statement(
            resourceArn=DATABASE_ARN,
            secretArn=SECRET_ARN,
            database=DATABASE_NAME,
            sql=sql,
            parameters=[
                {'name': 'user_id', 'value': {'longValue': int(row['user_id'])}},
                {'name': 'email', 'value': {'stringValue': row['email']}},
                {'name': 'monthly_income', 'value': {'doubleValue': float(row['monthly_income'])}},
                {'name': 'credit_score', 'value': {'longValue': int(row['credit_score'])}},
                {'name': 'employment_status', 'value': {'stringValue': row['employment_status']}},
                {'name': 'age', 'value': {'longValue': int(row['age'])}}
            ]
        )
    
    return {
        'statusCode': 200,
        'body': json.dumps('CSV data ingested successfully!')
    }
