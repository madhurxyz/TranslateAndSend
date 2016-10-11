import httplib2
import json
try:  # Python 2
    import urllib
except:  # Python 3
    import urllib.parse as urllib
from twilio.rest import TwilioRestClient
account = "enter-key-here"
token = "enter-key-here"

# Google Translate
BASE_URL = 'https://www.googleapis.com/language/translate/v2'
ATTACH_KEY = '?key='
GOOGLE_API_KEY = 'enter-key-here'
URL_SOURCE = '&source=en'
ATTACH_TARGET = '&target='
ATTACH_QUERY = '&q='

def translate(text, language):
    if text isinstance list:
        translatedArray = []
        for item in text:
            translatedText = encodeTranslate(item, language)
            print(translatedText)
            translatedArray.append(translatedText)
        return translatedArray
    elif text isinstance str:
        translatedText = encodeTranslate(text, language)
        print(translatedText)
        return translatedText
    else:
        raise Exception('Not expected type')

def encodeTranslate(text, language):
    text_encoded = urllib.quote_plus(text)
    language_encoded = urllib.quote_plus(language)
    url = BASE_URL + ATTACH_KEY + GOOGLE_API_KEY + URL_SOURCE + ATTACH_TARGET + language_encoded + ATTACH_QUERY + text_encoded
    http = httplib2.Http()
    response, body = http.request(url, 'GET')

    try:
        parsed_body = json.loads(body)
        return parsed_body['data']['translations'][0]['translatedText']
    except Exception as e:
        print('Translation failed with no JSON response from Google')

def sendText(text, number):
    client = TwilioRestClient(account, token)
    stringToReturn = ""
    if text isinstance list:
        for item in text:
            stringToReturn += item + ', '
    elif text :
        stringToReturn = text
    message = client.messages.create(
        to='+1' + number,
        from_='+1enter-number-here',
        body=stringToReturn
    )

sendText(translate(['hi how are you','it is lit','come through'], 'es'), 'enter-number-here')
