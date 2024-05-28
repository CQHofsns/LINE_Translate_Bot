#from translate_model import translate_engine
from googletrans import Translator
from langdetect import detect

from linebot import LineBotApi
from linebot.models import TextSendMessage

import os
import json
import boto3
import regex

LINE_CHANNEL_ACCESS_TOKEN= os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_BOT_API= LineBotApi(channel_access_token= LINE_CHANNEL_ACCESS_TOKEN)

def translated_function(text, src, dest):
    translator= Translator()
    return translator.translate(text, dest= dest, src= src)

def message_handling(message):
    lang_dict= {
        "japanese": "ja",
        "vietnamese": "vi",
        "english": "en",
        "chinese": "zh-cn",
        "thai": "th"
    }
    command_regex= fr"->to:((?:[\w\.\?]+,?\s?)+)$"
    message= str(message).strip()

    command_trigger= regex.search(command_regex, message, regex.IGNORECASE)
    if command_trigger:
        message= message.replace(str(command_trigger.group(0)), "")
        srclang_code= detect(text= message)
        destLang= command_trigger.group(1).split(",")
        destLang= [lang.strip(".?").strip().lower() for lang in destLang]
        print(destLang)
        print(len(destLang))
        if len(destLang)> 1:
            message_template= "User request multi-languages translation:\n"
            translated_message_dict= dict()
            for lang in destLang:
                if lang in lang_dict:
                    translated_message_dict[lang]= translated_function(
                        text= message, 
                        src= srclang_code, 
                        dest= lang_dict[lang]
                    ).text
            
            if len(translated_message_dict)== 0:
                return_message= "Sorry, I can not check the language you want to translate, maybe there is a typo in you message?? "
                translated_message= translated_function(
                    text= return_message, 
                    src= "en", 
                    dest= srclang_code
                ).text
                translated_message= translated_message+ " !!(・・ ) ?"

                return translated_message
            
            for lang in translated_message_dict.keys():
                message_template= f"""{message_template}
                ###### {lang} ######
                {translated_message_dict[lang]}
                #####################
                ---------------------
                """
            return message_template
        
        elif len(destLang)== 1:
            destLang= destLang[0].strip().lower()
            if destLang in lang_dict:
                translated_message= translated_function(
                    text= message, 
                    src= srclang_code, 
                    dest= lang_dict[destLang]
                ).text

            else:
                return_message= "Sorry, I can not check the language you want to translate, maybe there is a typo in you message?? "
                translated_message= translated_function(
                    text= return_message, 
                    src= "en", 
                    dest= srclang_code
                ).text
                translated_message= translated_message+ " !!(・・ ) ?"
    
        return translated_message

    return None

def handler(event, context):
    try:
        print(event)
        body= json.loads(event["body"])
        if body["events"]:
            if body["events"][0]["type"]== "message" and body["events"][0]["message"]["type"]== "text":
                replyToken= body["events"][0]["replyToken"]
                message= body["events"][0]["message"]["text"]

                translated_message= message_handling(message= message)
                if translated_message:
                    LINE_BOT_API.reply_message(
                        reply_token= replyToken,
                        messages= TextSendMessage(text= translated_message)
                    )
    
    except Exception as error:
        print(f"Uh, we have the error: {error}")
        return {
            "statusCode": 500,
            "body": json.dumps(f"An error occured: {error}")
        }
    
    print("statusCode: 200")
    return {
        "statusCode": 200,
        "body": json.dumps("Reply sent")
    }