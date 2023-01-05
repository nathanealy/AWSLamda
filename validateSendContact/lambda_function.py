import json
import logging
import urllib3
import config

# log settings
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # TODO implement

    logger.info(event)

    try:
        emailaddress = event['emailaddress']
        messagebody = event['messagebody']
        hcaptcharepsonse = event['hcaptcharepsonse']
        
        logger.info(emailaddress)
        logger.info(messagebody)
        logger.info(hcaptcharepsonse)    
        
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
                    return {
                        'statusCode': 500,
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
    except:
        logger.error("ERROR: Getting parameters")
        return {
            'statusCode': 500,
            'body': json.dumps('Error')
        }                
       
def validatehCaptcha(hrepsonse):
    status = "OK"
    pool = ""
    url = ""
    message = ""
    
    data = {'secret': config.hcaptcha_secret, 'respone': hrepsonse}
    http = urllib3.PoolManager()

    try:
        response = http.request_encode_body('POST', config.hcaptcha_address, headers={'Content-Type':'application/x-www-form-urlencoded'}, body=data)
        logger.info(response)  
        response_json = json.dump(response.content)
        logger.info(response_json)          
    except urllib3.exceptions.ResponseError as ex:
        status = "ERROR"        
        logger.error(ex)
    except urllib3.exceptions.ResponseErrorRequestError(pool, url, message):   
        status = "ERROR"            
        logger.error(pool)
        logger.error(url)
        logger.error(message)
        
    return status

def sendMessage(address, message):
    status = "OK"

    return status