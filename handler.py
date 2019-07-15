import os
import re
import json
import boto3

COGNITO_USER_POOL_ARN = os.environ.get('COGNITO_USER_POOL_ARN')
COGNITO_IDENTITY_POOL_ID = os.environ.get('COGNITO_IDENTITY_POOL_ID')

def _get_identity_id_from_cognito_idToken(idToken):
    pattern = 'arn:aws:cognito-idp:(?P<aws_region>.*):(?P<aws_account_id>[0-9]{12}):userpool/(?P<user_pool_id>.*)'
    m = re.match(pattern, COGNITO_USER_POOL_ARN)

    region = m.group('aws_region')
    account_id = m.group('aws_account_id')
    user_pool_id = m.group('user_pool_id')
    cognito_user_pool_keyname = f"cognito-idp.{region}.amazonaws.com/{user_pool_id}"

    # @see https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client.get_id
    response = boto3.client('cognito-identity', region).get_id(
        AccountId=account_id,
        IdentityPoolId=COGNITO_IDENTITY_POOL_ID,
        Logins={
            # Amazon Cognito user pool Example:
            #   "cognito-idp.us-east-1.amazonaws.com/us-east-1_123456789": "${idToken}"
            cognito_user_pool_keyname: idToken,
        }
    )
    return response['IdentityId']

def hello(event, context):
    idToken = event['headers']['Authorization']
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event,
        "identity_id": _get_identity_id_from_cognito_idToken(idToken)
    }

    response = {
        # CORS settings for Lambda Proxy Integration
        "headers": {
            "Access-Control-Allow-Origin": '*'
        },
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
