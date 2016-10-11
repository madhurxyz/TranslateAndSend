import httplib2
import urllib
import json

from twilio.rest import TwilioRestClient
account_sid = "AC31f69e42c332863b928d3f36cb879962" # Your Account SID from www.twilio.com/console
auth_token  = "381b9823f3e445a9343488ef9a5e0c14"  # Your Auth Token from www.twilio.com/console

TRANSLATE_URL = "https://www.googleapis.com/language/translate/v2?key="
GOOGLE_API_KEY = "AIzaSyCV2x3FzeEIMa0T4HWjWIBKv8r-T1ZhZCk"
TRANSLATE_SOURCE = "&source=en"
TRANSLATE_TARGET = "&target="
TRANSLATE_TEXT = "&q="

def sendText(text, number):
    if type(text) is list:
        # TODO Delegation
        textToSend = ""
        for item in text:
            textToSend += item + ", "
    elif type(text) is unicode or str:
        textToSend = text
    else:
        raise Exception("Not expected type")
    client = TwilioRestClient(account_sid, auth_token)
    message = client.messages.create(
        body = textToSend,
        to = "+1" + number,    # Replace with your phone number
        from_ = "+12052367720") # Replace with your Twilio number
        # print(message.sid)

def translate(text, language):
    if type(text) is list:
        return translateArray(text, language)
    elif type(text) is unicode or str:
        return translateString(text, language)
    else:
        raise Exception("Not expected type")

def translateArray(iterable, language):
    return translateString(', '.join(iterable), language)

def translateString(text, language):
    text_encoded = urllib.quote_plus(text)
    url = TRANSLATE_URL + GOOGLE_API_KEY + TRANSLATE_SOURCE + TRANSLATE_TARGET + language + TRANSLATE_TEXT + text_encoded
    http = httplib2.Http()
    response, body = http.request(url, "GET")
    try:
        parsed_body = json.loads(body)
        return parsed_body['data']["translations"][0]['translatedText']
    except Exception as e:
        return "translation failed with no JSON response"

sendText(translate('it is lit', 'es'), "2242467230")
sendText(translate(["here is a word", "another set of words", "here are more words"], 'de'), "2242467230")
