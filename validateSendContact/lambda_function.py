import json
import logging
import requests
import config
import boto3
from botocore.exceptions import ClientError

# log settings
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # TODO implement

    try:
        emailaddress = event['emailaddress']
        messagebody = event['messagebody']
        hcaptcharepsonse = event['hcaptcharepsonse']

        if len(emailaddress) > 0 and len(messagebody) > 0 and len(hcaptcharepsonse) > 0:

            if validatehCaptcha(hcaptcharepsonse) == "OK":
                logger.info("hCaptcha validated")
                if sendMessage(emailaddress, messagebody) == "OK":
                    logger.info("Message sent")
                    return {
                        'statusCode': 200,
                        'body': json.dumps('OK')
                    }      
                else:
                    logger.info("Message not sent")
                    return {
                        'statusCode': 2,
                        'body': json.dumps('ERROR')
                    }  
            else:
                return {
                    'statusCode': 500,
                    'body': json.dumps('ERROR')
                }                         
        else:
            return {
                'statusCode': 204,
                'body': json.dumps('NULL parameter(s)')
            }             
    except Exception as e:
        logger.error(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error')
        }                
       
def validatehCaptcha(hrepsonse):
    status = "OK"

    try:
        logger.info('A ' + config.hcaptcha_address) 
        logger.info('R ' + hrepsonse) 
        logger.info('S ' + config.hcaptcha_secret) 
         
        response = requests.post(config.hcaptcha_address,data={'secret': config.hcaptcha_secret, 'response': hrepsonse},headers={'Content-Type':'application/x-www-form-urlencoded'})

        logger.info(response.content)  
        data = json.loads(response.content)
        success = data['success']
        logger.info(success)     
        
        if success == False:
            status = "ERROR"
        
    except Exception as e:
        status = "ERROR" 
        logger.error(e)
        
    return status

def sendMessage(address, message):
    status = "OK"
    
    logger.info(address)
    logger.info(message)
    
    full_message_text = (address + '\r\n' + message)
    
    full_message_html = ("<html><head></head><body><h1>Message From a Site</h1><p>{b1}</p><p>{b2}</p></body></html>".format(b1=address, b2=message))
    
    destination = {
        'ToAddresses': [
            config.ses_to_email,
        ],
    }
    
    smtpmessage = {
        'Body' : { 
            'Html': {
                'Charset': 'UTF-8',
                'Data': full_message_html,
            },
            'Text': {
                'Charset': 'UTF-8',
                'Data': full_message_text,                
            },
        },
        'Subject': {
            'Charset': 'UTF-8',
            'Data': 'Message From a Site',
        }
    }
    
    client = boto3.client('ses', region_name=config.aws_region)
    
    try:
        response = client.send_email(Destination=destination, Message=smtpmessage, Source=config.ses_from_email)
    except ClientError as e:
        status = "ERROR" 
        logger.error(e)          
    except Exception as e:
        status = "ERROR" 
        logger.error(e)       
    
    return status