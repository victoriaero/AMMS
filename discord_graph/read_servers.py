import zipfile as zf
from collections import defaultdict

SERVERS_PATH = "C:\\Users\\victo\\OneDrive - Universidade Federal de Minas Gerais\\AMMS\\40.zip"

servers = defaultdict(list)
server_channels = defaultdict(list)


with zf.ZipFile(SERVERS_PATH, 'r') as servers_zp:
    file_list = servers_zp.namelist()
    # servers.printdir()

    for file_name in file_list:
        # Check if the file is a text file (you can use any desired condition)
        if file_name.endswith('.txt'):
            # Extract the server name from the file path
            server_name = file_name.split('/')[1]
            channel_name = file_name.split('/')[2]

            # Read the content of the text file within the archive
            with servers_zp.open(file_name) as file:
                text = file.read().decode('utf-8')  # Decode the bytes to a string

            # Append the text to the corresponding server's list
            servers[server_name].append(channel_name)
            server_channels[channel_name].append(text)

for server_name in servers.items():
    print("Server: ", server_name[0])
    for channel in server_channels.items():
        # Process the texts for this server
        print(f"Channel: ", channel[0])
        for text in channel[1]:
                parts = text.strip().split(',')
                
                # Verifique se a linha tem pelo menos duas partes (timestamp e nome)
                if len(parts) >= 2:
                    # O nome geralmente está na segunda posição (índice 1)
                    name = parts[1].strip()
                    print(name)