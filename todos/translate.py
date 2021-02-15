import os
import json

from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')
translate = boto3.client('translate')
comprehend = boto3.client('comprehend')

def whichlang(job):
    response = comprehend.detect_dominant_language(TEXT='string')

    return response

def translatejob(job, code, target):
    response = translate.translate_text(TEXT=job, SourceLanguageCode = code, TargetLanguageCode = target)

    return response

def get(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    job = result['Item']['text']

    target = event['pathParameters']['lang']

    resultcode = whichlang(job)
    
    code = resultcode['Languages'][0].get['LanguageCode']
    
    joblang = translatejob(job, code, target)
    result['Item']['text'] = joblang['TranslatedText']

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
