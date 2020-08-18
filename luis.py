import requests
from QnA import callQnAservice
import json

def luisservice(utterance,service):
    try:
        # APP-ID: The App ID GUID found on the www.luis.ai Application Settings page.
        if service=='QnA':
            appId = 'xxxxxxxxxxxxxxxxxxxxxxxxx'
        elif service == 'document':
            appId = 'xxxxxxxxxxxxxxxxxxxxxxxxxx'
        else:
            return 'ERROR ARISE'

        # PREDICTION-KEY: Your LUIS authoring key, 32 character value.= primary key
        prediction_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxx'

        # PREDICTION-ENDPOINT: Replace with your authoring key endpoint.
        # For example, "https://westus.api.cognitive.microsoft.com/"
        prediction_endpoint = 'https://xxxxxxxxxxxxxxxxxxxxxxxxx.cognitiveservices.azure.com/'

        # The utterance you want to use.
        #utterance = utterance

        ##########

        # The headers to use in this REST call.
        headers = {
        }
        # The URL parameters to use in this REST call.
        params ={
            'query': utterance,
            'timezoneOffset': '0',
            'verbose': 'true',
            'show-all-intents': 'true',
            'spellCheck': 'false',
            'staging': 'false',
            'subscription-key': prediction_key
        }

        # Make the REST call.
        response = requests.get(f'{prediction_endpoint}luis/prediction/v3.0/apps/{appId}/slots/production/predict', headers=headers, params=params)

        # Display the results on CLI.
        print(response.json())

    except Exception as e:
        # Display the error string.
        print(f'{e}')

    return response.json()