#from translate_model import translate_engine
from googletrans import Translator

from linebot import LineBotApi
from linebot.models import TextSendMessage

import os
import json
import boto3

LINE_CHANNEL_ACCESS_TOKEN= os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_BOT_API= LineBotApi(channel_access_token= LINE_CHANNEL_ACCESS_TOKEN)

def translated_function(text):
    translator= Translator()
    return translator.translate(text, dest= "ja", src= "vi")

def handler(event, context):
    try:
        print(event)
        body= json.loads(event["body"])
        if body["events"]:
            if body["events"][0]["type"]== "message" and body["events"][0]["message"]["type"]== "text":

                replyToken= body["events"][0]["replyToken"]
                message= body["events"][0]["message"]["text"]

                translated_message= translated_function(text= message).text

                LINE_BOT_API.reply_message(
                    reply_token= replyToken,
                    messages= TextSendMessage(text= translated_message)
                )
    except Exception as error:
        print(error)
        return {
            "statusCode": 500,
            "body": json.dumps(f"An error occured: {error}")
        }
    
    return {
        "statusCode": 200,
        "body": json.dumps("Reply sent")
    }