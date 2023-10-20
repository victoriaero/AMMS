import zipfile as zf
from collections import defaultdict
import os


SERVERS_PATH = "C:\\Users\\victo\\OneDrive - Universidade Federal de Minas Gerais\\AMMS\\40.zip"
OUTPUT_FOLDER = ".\\users_servers"

server_texts = defaultdict(list) # as chaves sao os servidores e os itens sao os canais
channels_texts = defaultdict(list) # as chaves sao os canais e os itens sao as mensagens

with zf.ZipFile(SERVERS_PATH, 'r') as servers_zf:
    files_list = servers_zf.namelist()
    # servers_zf.printdir()

    for server_files in files_list:
        if server_files.endswith('/') and server_files != 'Servidores/':
            server_name = server_files.split('/')[1]
            for channels_files in files_list:
                if channels_files.endswith('.txt') and channels_files.split('/')[1] == server_name: # se o nome do arquivo dos canais tiver o mesmo nome 
                    channel_name = channels_files.split('/')[2]
                    server_texts[server_name].append(channels_files)

                    with servers_zf.open(channels_files) as file:
                        text = file.read().decode('utf-8')

                    channels_texts[channel_name].append(text)

# print(server_texts)

for server_name in server_texts.keys():
    print(f"Server: {server_name}")
    registered_names = set()
    for channel in server_texts.get(server_name):
        print(f"Canal: {channel.split('/')[2]}")
        # if channels_texts.get(channel.split('/')[2]):
        for channel_text in channels_texts.get(channel.split('/')[2]):
            for messagem in channel_text:
                parts = channel_text.strip().split(',')
                if len(parts) >= 2:
                    name = parts[1].strip()
                    if name not in registered_names:
                        registered_names.add(name)
                        output_file = os.path.join(OUTPUT_FOLDER, f'{server_name}.txt')
                        with open(output_file, 'a', encoding='utf-8') as names_file:
                            names_file.write(name + '\n')
                    # print(name)
