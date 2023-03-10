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

            cursor.execute("select feature_type, feature_geometry_type, feature_geometry_longitude, feature_geometry_latitude, feature_properties_title, feature_properties_description from conflicts")
            records = cursor.fetchall()
            
            features = []
            
            for row in records:
                feature = {
                    "type": row[0],
                    "geometry": {
                        "type": row[1],
                        "coordinates": [row[1], row[2]]
                    },
                    "properties": {
                        "title": row[3],
                        "description": row[4]
                    }
                }
            
                features.append(feature)
            
            geojson = {
                "type": "FeatureCollection",
                "features" : features
            }
            
            
            cursor.close()

        if len(features) > 0:         
            return {
                'statusCode': 200,
                'body': json.dumps(geojson, default=str)
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
        
