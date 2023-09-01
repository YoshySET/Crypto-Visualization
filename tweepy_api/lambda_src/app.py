import boto3
from botocore.exceptions import ClientError
import json
import tweepy
import openai


def setup_tw_api():
    try:
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name="ap-northeast-1"
        )
        response = client.get_secret_value(SecretId="TwitterApiKey")
        api_keys_dict = json.loads(response['SecretString'])

        consumer_key = api_keys_dict["CONSUMER_KEY"]
        consumer_secret = api_keys_dict["CONSUMER_SECRET"]
        access_token = api_keys_dict["ACCESS_TOKEN"]
        access_secret = api_keys_dict["ACCESS_SECRET"]

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
        return api, client
    except ClientError as e:
        raise e

def setup_openai_api():
    try:
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name="ap-northeast-1"
        )
        response = client.get_secret_value(SecretId="OpenAI-API")
        api_keys_dict = json.loads(response['SecretString'])

        openai.api_key = api_keys_dict["API_KEY"]
    except ClientError as e:
        raise e



def handler(event, context):
    # Twitter API認証
    tw_api, tw_client = setup_tw_api()

    # OpenAI API認証
    setup_openai_api()

    # GETパラメータ取得
    params = event.get('queryStringParameters')
    param1 = params.get('param1')

    base_content = "以下の文章の感情を分析して、ポジティブ度を0~100pointで評価してください。出力するのはそのpointの数値のみで構いません。\n\n"
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": base_content + param1}
        ]
    )

    # ツイート
    # tw_client.create_tweet(text=param1)

    return {
        'statusCode': 200,
        "headers": {"Content-Type": "application/json"},
        'body': json.dumps(completion.choices[0].message)
    }
