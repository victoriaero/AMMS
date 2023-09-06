import requests
import json

#lalal
def retrieve_messages(channel_id, output_file):
    headers = {
        'authorization': 'NjE5Njg1OTI1MzI4Mzg4MTE3.GA1otH.KMCFFmhcY6yRRoLbsXBcvKU_wJ4hqLQTXqa__s'
    }

    limit = 100
    before = None

    with open(output_file, 'w', encoding='utf-8') as file:
        while True:
            params = {
                'limit': limit,
                'before': before
            }

            message_request = requests.get(f'https://discord.com/api/v9/channels/150074202727251969/messages?limit=100', headers=headers, params=params)

            if message_request.status_code == 200:
                messages_json = json.loads(message_request.text)

                if not messages_json:
                    break

                for message in messages_json:
                    username = message['author']['username']
                    content = message['content']
                    alo = message['timestamp']
                    id = message['id']
                    message_str = f'{username}, {content}, {alo}, {id}\n'
                    if(content != ''):
                        print(message_str)
                        file.write(message_str)

                before = messages_json[-1]['id']  # ID da última mensagem na resposta
            else:
                print(f"Erro ao recuperar mensagens. Código de status: {message_request.status_code}")
                break

retrieve_messages('150074202727251969', 'mensagens.txt')