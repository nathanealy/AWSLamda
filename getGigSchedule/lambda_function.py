import sys
import json
import rds_config
import pymysql
import logging
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
    logger.error("ERROR: Could not connect to database")
    logger.error(e)

def lambda_handler(event, context):
    # TODO implement

    try:
        with connection.cursor() as cursor:
  
            cursor.execute("select gig_date, gig_title, gig_description, gig_link, gig_location, gig_price from gigs where gig_date > '% s' order by gig_date asc" % datetime.now())
            event_list = list(cursor.fetchall())

        if len(event_list) > 0:         
            return {
                'statusCode': 200,
                'body': json.dumps(event_list, default=str)
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
        
