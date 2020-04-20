import pymysql
import sys
import json

REGION = 'us-east-1'

rds_host  = "cloud-project.ceciml9cxceh.us-east-1.rds.amazonaws.com"
name = "root"
password = "beto280396"
db_name = "project"

def save_events(event):

    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    
    try:
        httpMethod = event['httpMethod']
        
        if httpMethod == "POST":
            body = json.loads(event['body'])
            with conn.cursor() as cursor:
                sql = "INSERT INTO `book` (`id`, `name`, `author`, `edition`, `value`, `isbn`) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (body['id'], body['name'], body['author'], body['edition'], body['value'], body['isbn']))
                
                conn.commit()
                return {
                    'statusCode': 200,
                    'body': json.dumps("Successfull")
                }

        else:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM `book` WHERE `id`=%s"
                cursor.execute(sql, (event['queryStringParameters']['id']))
                result = cursor.fetchone()
                return {
                    'statusCode': 200,
                    'body': json.dumps(result)
                }
            
    finally:
        conn.close()

def main(event, context):
    return save_events(event)