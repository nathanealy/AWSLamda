import sys
import json
import rds_config
import pymysql
import logging
import base64
from datetime import datetime

# rds settings
rds_host = rds_config.db_host
rds_dbname = rds_config.db_name
rds_password = rds_config.db_password
rds_username = rds_config.db_username
rds_port = rds_config.db_port

# log settings
logger = logging.getLogger()
logger.setLevel(logging.INFO)
    
# connect to database    

try:
    connection = pymysql.connect(host=rds_host, user=rds_username, passwd=rds_password, db=rds_dbname, connect_timeout=5, port=rds_port)
    logger.info("SUCCESS: Database connection succeeded")    
except pymysql.MySQLError as e:
    logger.error(e)

def lambda_handler(event, context):
    # TODO implement

    try:
        with connection.cursor() as cursor:
  
            cursor.execute("SELECT biography, picture, name FROM tsr_schema.performers where active = 1;")
            performer_list = list(cursor.fetchall())
            converted_list = list()
         
            if len(performer_list) > 0:      
                for pt in performer_list:
                    pl = list(pt)
                    pl_bytes =  base64.b64encode(pt[1])
                    
                    base64_string = pl_bytes.decode()
                    pl[1] = base64_string
                    
                    logger.info(pl)
                    converted_list.append(pl)
                    
                logger.info(converted_list)
                    
                return {
                    'statusCode': 200,
                    'body': json.dumps(converted_list, default=str)
                }
            else: 
                return {
                    'statusCode': 204,
                    'body': json.dumps('No data')
                }            
    except pymysql.MySQLError as e:
        logger.error("ERROR: fetching")
        logger.error(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error')
        } 
        
