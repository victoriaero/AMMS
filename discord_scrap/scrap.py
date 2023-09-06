import requests
import json

def retrieve_messages(channel_id):

    headers = {
        'authorization': 'NDQ0NjY1MDE0NTg3MDk3MDkw.GtDcGu.FteoelXcm8KpF7p3UkDnD4JcnYGu21NMsE7rzI'
    }

    message_request = requests.get(f'https://discord.com/api/v9/channels/{channel_id}/messages?limit=50', headers=headers)

    # messages_json = json.loads(message_request.text)

    with open ('data.json', 'w') as data_json:
        json.dump(message_request.text, data_json)

    
    # for value in messages_json:
    #     print(value, '\n')

retrieve_messages(1148795977730379868)