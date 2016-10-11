import httplib2
import json
try:  # Python 2
    import urllib
except:  # Python 3
    import urllib.parse as urllib
from twilio.rest import TwilioRestClient

# Google Translate
base_url = 'https://www.googleapis.com/language/translate/v2'
google_api_key = '?key=enter-key-here'
source = "&source=en"
target = "&target="

# Twilio
account = "enter-key-here"
token = "enter-key-here"
client = TwilioRestClient(account, token)
phone_number_from = "+1enter-number-here"


def translateAndSend(text, language, number):
    """
    # This function translates any text into any language.
    # You have to input 3 parameters:
        1. The 'text' input is the text you want to translate
        2. The 'language' input is the langauge you want to translate 'text' into
        3. The number you want to send the translated 'text' to

    # All 3 parameters should be passed as strings
    # The 'text' parameter can be passed as an array of strings
    # The 'language' input must be two characters. Example: 'es' stands for spanish
    # More language codes can be found in the following url:
        https://sites.google.com/site/tomihasa/google-language-codes
    """

    language_encoded = urllib.quote_plus(language)
    phone_number_to = "+1" + number

    if (type(text) is list):

        translatedArray = []

        for i in text:
            translatedText = translateText(i, language_encoded)
            print(translatedText)
            message = client.messages.create(
                to=phone_number_to,
                from_=phone_number_from,
                body=translatedText
            )
            translatedArray.append(translatedText)
        return translatedArray
    else:
        translatedText = translateText(text, language_encoded)
        print(translatedText)

        message = client.messages.create(
            to=phone_number_to,
            from_=phone_number_from,
            body=translatedText
        )
        return translatedText


def translateText(text, language):
    text_encoded = urllib.quote_plus(text)
    url = base_url + google_api_key + source + target + language + "&q=" + text_encoded
    http = httplib2.Http()
    response, body = http.request(url, "GET")

    try:
        parsed_body = json.loads(body)
        return parsed_body['data']['translations'][0]['translatedText']
    except Exception as e:
        print('Translation failed with no JSON response from Google')
