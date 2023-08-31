import boto3
from botocore.exceptions import ClientError
import os
import json
import tweepy


def get_secret():
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name="ap-northeast-1"
    )
    try:
        response = client.get_secret_value(SecretId="TwitterApiKey")
        return json.loads(response['SecretString'])
    except ClientError as e:
        raise e


def handler(event, context):
    api_keys = get_secret()
    consumer_key = api_keys["CONSUMER_KEY"]
    consumer_secret = api_keys["CONSUMER_SECRET"]
    access_token = api_keys["ACCESS_TOKEN"]
    access_secret = api_keys["ACCESS_SECRET"]

    # tweepy api認証
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    # tweepy client認証
    client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_secret
    )

    client.create_tweet(text='ttt')

    return {
        'statusCode': 200,
        'body': 'Hello, world!'
    }
