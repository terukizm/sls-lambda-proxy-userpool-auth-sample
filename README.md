sls-lambda-proxy-userpool-auth-sample
====

Serverless Framework + Cognito UserPool Authorization Sample
(Use Lambda Proxy Integration and get Cognito identityID)

# Usage

```
$ export AWS_SDK_LOAD_CONFIG=1
$ cp ./env/dev.yml.example ./env/dev.yml
$ vi ./env/dev.yml
---
AWS_PROFILE: default
AWS_REGION: ap-northeast-1
COGNITO_IDENTITY_POOL_ID: ap-northeast-1:38535a48-8569-4f7f-9de3-123456789012
COGNITO_USER_POOL_ARN: arn:aws:cognito-idp:ap-northeast-1:XXXXXXXXXXXX:userpool/ap-northeast-1_XXXXXXXXX
---

$ serverless deploy -v
...
ServiceEndpoint: https://xxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/dev

$ ENDPOINT=https://xxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/dev

# get from webapp(WARN: THIS IS NOT "accessToken")
$ idToken=eyJraWxxxxx..........xxxxxzU-zA

$ curl -sS -X GET -H "Authorization: ${idToken}"  "${ENDPOINT}/hello" | jq .

{
  "message": "Go Serverless v1.0! Your function executed successfully!",
  "input": {
    "resource": "/hello",
    "path": "/hello",
    "httpMethod": "GET",
    "headers": {
      "Accept": "*/*",
      "Authorization": "eyJraWxxxxx..........xxxxxzU-zA",
      "CloudFront-Forwarded-Proto": "https",
      ...
    },
    ...
    "requestContext": {
      "resourceId": "zlum7d",
      "authorizer": {
        "claims": {
          "sub": "12345678-37a3-4c53-a3e0-123456789012",
          "aud": "xxxxx6kjvok1phfn8rusbxxxxx",
          "email_verified": "true",
          "event_id": "00065806-ead1-4aac-98a5-11f78d2af000",
          "token_use": "id",
          "auth_time": "1562947993",
          "iss": "https://cognito-idp.ap-northeast-1.amazonaws.com/ap-northeast-1_XXXXXXXXX",
          "cognito:username": "12345678-37a3-4c53-a3e0-123456789012",
          "exp": "Mon Jul 15 05:58:22 UTC 2019",
          "iat": "Mon Jul 15 04:58:22 UTC 2019",
          "email": "cognito-test@exapmle.com"
        }
      },
      ...
      "identity": {
        "cognitoIdentityPoolId": null,
        "accountId": null,
        "cognitoIdentityId": null,
        "caller": null,
        "sourceIp": "xxx.xxx.xxx.xxx",
        "principalOrgId": null,
        "accessKey": null,
        "cognitoAuthenticationType": null,
        "cognitoAuthenticationProvider": null,
        "userArn": null,
        "userAgent": "curl/7.58.0",
        "user": null
      },
      "domainName": "xxxxxxxx.execute-api.ap-northeast-1.amazonaws.com",
      "apiId": "xxxxxxxx"
    },
    "body": null,
    "isBase64Encoded": false
  },
  "identity_id": "ap-northeast-1:2ac6c5a4-5f4d-4bb4-83c3-123456789012"
}
```
