import json
import logging
import requests
import config

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
                    logger.info("hCaptcha not validated")
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

    return status