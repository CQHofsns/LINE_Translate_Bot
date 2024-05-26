#from translate_model import translate_engine
from googletrans import Translator

import json
import boto3

def translate_message(text):
    translator= Translator()
    return translator.translate(text, dest= "ja", src= "vi")

def handler(event, context):
    body= json.loads(event["body"])
    message= body["events"][0]["message"]["text"]

    translated_message= translated_message(text= message)

    response= {
        "statusCode": 200,
        "body": json.dumps(
            {
                "replyToken": body["events"][0]["replyToken"],
                "messages": [
                    {
                        "type": "text",
                        "text": translated_message
                    }
                ]
            }
        )
    }

    return response