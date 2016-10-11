import httplib2
import urllib
import json

from twilio.rest import TwilioRestClient
account_sid = "enter-key-here" # Your Account SID from www.twilio.com/console
auth_token  = "enter-key-here"  # Your Auth Token from www.twilio.com/console
TRANSLATE_URL = "https://www.googleapis.com/language/translate/v2?key="
GOOGLE_API_KEY = "enter-key-here"
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
        from_ = "+1enter-number-here") # Replace with your Twilio number

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
        return "Translation failed with no JSON response."

sendText(translate('it is lit', 'es'), "enter-number-here")
sendText(translate(["here is a word", "another set of words", "here are more words"], 'de'), "enter-number-here")
