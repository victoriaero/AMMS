import logging
import os
import requests
import sys
import time

# Constants and Configuration
AUTHORIZATION_TOKEN = ''
FILES_FOLDER = 'files'
LOGS_FOLDER = 'logs'
OUTPUT_BASE_FOLDER = 'data'
RATE_LIMIT_WAIT_TIME = 0

#create a mined_servers.txt file if it doesn't exist
if not os.path.exists(FILES_FOLDER + '/mined_servers.txt'):
    os.makedirs(FILES_FOLDER, exist_ok=True)
    open(FILES_FOLDER + '/mined_servers.txt', 'w', encoding='utf-8').close()

# Create a logs directory if it doesn't exist
os.makedirs(LOGS_FOLDER, exist_ok=True)

# Create a logger for error messages
error_logger = logging.getLogger('error_logger')
error_logger.setLevel(logging.ERROR)
error_handler = logging.FileHandler(LOGS_FOLDER + '/errors.log', mode='a', encoding='utf-8')
error_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
error_handler.setFormatter(error_formatter)
error_logger.addHandler(error_handler)

# Create a logger for info messages
info_logger = logging.getLogger('info_logger')
info_logger.setLevel(logging.INFO)
info_handler = logging.FileHandler(LOGS_FOLDER + '/info.log', mode='a', encoding='utf-8')
info_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
info_handler.setFormatter(info_formatter)
info_logger.addHandler(info_handler)

# Function to make an API request
def make_request(url, headers, params):
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Raise an exception for bad responses
    return response.json()

# Function to write the server information to a file
def write_mined_server(server_info):
    server_line = f"{server_info[0]},{server_info[1]}\n"

    with open(FILES_FOLDER + '/mined_servers.txt', 'a', encoding='utf-8') as mined_servers_file:
        mined_servers_file.write(server_line)

# Function to retrieve text channels for a server
def retrieve_text_channels(server_id, server_name, headers):
    try:
        response = make_request(f'https://discord.com/api/v9/guilds/{server_id}/channels', headers=headers, params={})

        if isinstance(response, list):
            text_channels = [channel for channel in response if channel.get('type', 0) == 0 and not channel.get('private', False)]
            return text_channels

    except requests.exceptions.HTTPError as e:
        error_logger.error(f"Erro ao recuperar canais. Response: {e.response}. Status code: {e.response.status_code}. Servidor: {server_name}. ID: {server_id}.")
        return []

# Function to fetch and save messages from a channel
def fetch_channel_messages(channel_id, channel_name, server_name, headers):
    output_folder = os.path.join(OUTPUT_BASE_FOLDER, server_name)
    os.makedirs(output_folder, exist_ok=True)

    output_file = os.path.join(output_folder, f'{channel_name}.txt')

    limit = 100
    before = None
    messages_written = False

    while True:
        params = {
            'limit': limit,
            'before': before
        }

        try:
            messages_json = make_request(f'https://discord.com/api/v9/channels/{channel_id}/messages', headers=headers, params=params)
            if not messages_json:
                break

            with open(output_file, 'a', encoding='utf-8') as file:
                for message in messages_json:
                    if 'content' in message and message['content'].strip() != '':
                        username = message['author']['username']
                        user_id = message['author']['id']
                        content = message['content'].replace('\n', ' ')
                        timestamp = message['timestamp']

                        message_str = f'{timestamp},{user_id},{username},{content} $#fim#$\n'

                        # print(message_str)
                        file.write(message_str)

                        messages_written = True

                before = messages_json[-1]['id']

        except requests.exceptions.HTTPError as e:
            error_logger.error(f"Erro ao recuperar mensagens do canal. Response: {e.response}. Status: {e.response.status_code}. Servidor: {server_name}. Canal: {channel_name}.")
            return

        # Respect the Discord rate limit
        time.sleep(RATE_LIMIT_WAIT_TIME)

    # Check if the file exists before attempting to remove it
    if os.path.exists(output_file) and not messages_written:
        os.remove(output_file)

    info_logger.info(f"Mensagens recuperadas com sucesso. Servidor: {server_name}. Canal: {channel_name}.")

# Function to process server information
def process_server_info(server_info, headers):
    if len(server_info) != 2:
        error_logger.error(f"Formato inválido na linha do arquivo 'servers.txt': {server_info}")
        return

    server_name, server_id = server_info

    text_channels = retrieve_text_channels(server_id, server_name, headers)

    if not text_channels:
        error_logger.error(f"Não foi possível acessar os canais do servidor. Servidor: {server_name}. ID: {server_id}.")
        return

    for channel in text_channels:
        channel_name = channel['name']
        channel_id = channel['id']

        # Check if the channel is a text channel (not a voice channel, not private)
        if 'private' in channel or channel['type'] != 0:
            continue

        fetch_channel_messages(channel_id, channel_name, server_name.strip(), headers)

    info_logger.info(f"Servidor minerado com sucesso. Servidor: {server_name}. ID: {server_id}.")
    write_mined_server(server_info)

# Main function
def main():
    # Token of authentication
    headers = {
        'authorization': AUTHORIZATION_TOKEN
    }

    info_logger.info("Iniciando programa.")
    try:
        
        for i in range(1, 32):
            filename = FILES_FOLDER + f'/servidorespagina{i}.txt'

            if not os.path.exists(filename):
                error_logger.error(f"Arquivo não encontrado: {filename}.")
                continue

            with open(filename, 'r', encoding='utf-8') as servers_file:
                servers = [line.strip().split(",") for line in servers_file]

            for server_info in servers:
                if server_info not in [line.strip().split(",") for line in open(FILES_FOLDER + '/mined_servers.txt', 'r', encoding='utf-8')]:
                    process_server_info(server_info, headers)
                else:
                    server_name, server_id = server_info
                    info_logger.info(f"Servidor já minerado. Pulando. Servidor: {server_name}. ID: {server_id}.")

        info_logger.info("Programa finalizado com sucesso.")
        print("Programa finalizado com sucesso.")

    except KeyboardInterrupt:
        error_logger.error("Programa interrompido pelo usuário.")
        return

    except requests.exceptions.ConnectionError as e:
        error_logger.error(f"Erro de conexão. Esperando 10 minutos. Tipo de exceção: {type(e).__name__}. Descrição: {e}") 
        time.sleep(600)
        main()

     except requests.exceptions.ChunkedEncodingError as e:
        error_logger.error(f"ChunkedEncodingError. Esperando 10 minutos. Tipo de exceção: {type(e).__name__}. Descrição: {e}")
        time.sleep(600)
        main()

    except Exception as e:
        error_logger.error(f"Erro inesperado. Tipo de exceção: {type(e).__name__}. Descrição: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
