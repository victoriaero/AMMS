import json
import os
import requests
import time

# Defina o nome da pasta de saída
output_base_folder = 'Servidores'

# Tempo limite de 5000 segundos (cerca de 83 minutos) por servidor
server_timeout_seconds = 3600

# Tempo mínimo entre solicitações para respeitar o limite de taxa do Discord (5 solicitações por segundo)
rate_limit_wait_time = 0

def get(url, headers, params):
    return requests.get(url, headers=headers, params=params)

def fetch_messages(channel_id, channel_name, server_name, headers):
    output_folder = os.path.join(output_base_folder, server_name)
    os.makedirs(output_folder, exist_ok=True)

    output_file = os.path.join(output_folder, f'{channel_name}.txt')

    limit = 100
    before = None
    messages_written = False
    start_time = time.time()

    while True:
        params = {
            'limit': limit,
            'before': before
        }

        message_request = get(f'https://discord.com/api/v9/channels/{channel_id}/messages', headers=headers, params=params)

        if message_request.status_code == 200:
            messages_json = json.loads(message_request.text)

            if not messages_json:
                break

            with open(output_file, 'a', encoding='utf-8') as file:
                for message in messages_json:
                    if 'content' in message and message['content'].strip() != '':
                        username = message['author']['username']
                        content = message['content']
                        alo = message['timestamp']
                        message_str = f'{alo},{username},{content}\n'
                        
                        file.write(message_str)
                        messages_written = True

            before = messages_json[-1]['id']
        elif message_request.status_code == 403:
            print(f"Sem acesso ao canal {channel_name}.")
            break
        else:
            print(f"Erro ao recuperar mensagens do canal {channel_name}. Código de status: {message_request.status_code}")
            break

        # Verifique o tempo limite por servidor
        elapsed_time = time.time() - start_time
        if elapsed_time >= server_timeout_seconds:
            print(f"Limite de tempo atingido para o servidor {server_name}.")
            break

        # Respeite o limite de taxa do Discord
        time.sleep(rate_limit_wait_time)

    # Verifique se o arquivo existe antes de tentar removê-lo
    if os.path.exists(output_file) and not messages_written:
        os.remove(output_file)

def process_server(server_info, headers):
    if len(server_info) != 2:
        print(f"Formato inválido na linha do arquivo 'servers.txt': {server_info}")
        return

    server_name, server_id = server_info

    text_channels = retrieve_text_channels(server_id, headers)

    if not text_channels:
        print(f"Não foi possível acessar os canais do servidor {server_id}.")
        return

    for channel in text_channels:
        channel_name = channel['name']
        channel_id = channel['id']

        # Verificar se o canal é de texto (não é de voz, não é privado)
        if 'private' in channel or channel['type'] != 0:
            continue

        fetch_messages(channel_id, channel_name, server_name.strip(), headers)

def retrieve_text_channels(server_id, headers):
    response = requests.get(f'https://discord.com/api/v9/guilds/{server_id}/channels', headers=headers)
    if response.status_code == 200:
        channels_json = json.loads(response.text)
        text_channels = [channel for channel in channels_json if channel['type'] == 0 and not channel.get('private', False)]
        return text_channels
    else:
        print(f"Erro ao recuperar canais do servidor {server_id}. Código de status: {response.status_code}")
        return []

# Token de autenticação
headers = {
    'authorization': ''
}

# Ler a lista de servidores e seus IDs do arquivo 'servers.txt'
with open('servers.txt', 'r', encoding='utf-8') as servers_file:
    servers = [line.strip().split(",") for line in servers_file]

for server_info in servers:
    process_server(server_info, headers)

print("Mineração de todos os servidores concluída.")
