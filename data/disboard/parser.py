from bs4 import BeautifulSoup
import csv
import os

# Number of pages you have
num_pages = 50

# File for storing all servers
all_servers_file = 'csvs/1-50.csv'

# Initialize a list to store all servers
all_servers = []

# Conjunto para rastrear servidores já impressos
servidores_impressos = set()

for pagina in range(1, num_pages + 1):
    # Construct the file name
    input_filename = f'raw_html/page_{pagina}_content.html'

    # Check if the file exists
    if not os.path.exists(input_filename):
        print(f"File {input_filename} does not exist. Skipping.")
        continue

    # Read HTML content
    with open(input_filename, 'r', encoding='utf-8') as html_file:
        html = html_file.read()

    # Create a BeautifulSoup object
    soup = BeautifulSoup(html, 'html.parser')
    

    # Find all server divs
    server_divs = soup.find_all('div', class_=lambda x: x and x.startswith('server-'))

    # List to store servers from this page
    servidores = []

    # Extract server name and ID
    for div in server_divs:
        server_name_div = div.find('div', class_='server-name')
        if server_name_div:
            server_name = server_name_div.text.strip().replace(',', '')
            server_id = div.find('a', href=True)['href'].split('/')[-1]
            if server_id not in servidores_impressos and not server_id.endswith('#reviews'):
                servidores_impressos.add(server_id)
                nome_com_numero = f"{server_name.strip()}, {server_id}"
                servidores.append([nome_com_numero])
                all_servers.append([nome_com_numero])

    # Write servers to a file for this page
    with open(f'csvs/servidorespagina{pagina}.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        for servidor in servidores:
            nome_com_numero, server_id = servidor[0].split(',', 1)
            csvwriter.writerow([nome_com_numero.strip(), server_id.strip()])

    print(f"Os servidores foram armazenados em servidorespagina{pagina}.csv")

# Write all servers to a consolidated file
with open(all_servers_file, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    for servidor in all_servers:
        nome_com_numero, server_id = servidor[0].split(',', 1)
        csvwriter.writerow([nome_com_numero.strip(), server_id.strip()])

print(f"Todos os servidores foram armazenados em {all_servers_file}")
