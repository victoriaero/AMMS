from bs4 import BeautifulSoup
import csv

pagina = 51

# Ler o conteúdo do arquivo HTML
with open('input.html', 'r', encoding='utf-8') as html_file:
    html = html_file.read()

# Crie um objeto BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Conjunto para rastrear servidores já impressos
servidores_impressos = set()

# Encontre todas as tags 'div' com a classe 'server-XXXXXXXXXXXXX'
server_divs = soup.find_all('div', class_=lambda x: x and x.startswith('server-'))

# Inicialize uma contagem
contador = 1 + (pagina - 1) * 24

# Lista para armazenar os servidores
servidores = []

# Itere sobre as tags encontradas e extraia o nome do servidor e o ID
for div in server_divs:
    server_name_div = div.find('div', class_='server-name')
    if server_name_div:
        server_name = server_name_div.text.strip()
        server_id = div.find('a', href=True)['href'].split('/')[-1]
        # Verifique se o servidor já foi impresso antes e não é um link de revisão
        if server_id not in servidores_impressos and not server_id.endswith('#reviews'):
            servidores_impressos.add(server_id)
            nome_com_numero = f"{contador} - {server_name.strip()}, {server_id}"
            servidores.append([nome_com_numero])
            contador += 1

# Escreva os servidores em um arquivo CSV com dois parâmetros
with open(f'servidorespagina{pagina}.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    # csvwriter.writerow(['Nome do servidor', 'ID do servidor'])
    for servidor in servidores:
        nome_com_numero, server_id = servidor[0].split(',', 1)
        csvwriter.writerow([nome_com_numero.strip(), server_id.strip()])

print(f"Os servidores foram armazenados em servidorespagina{pagina}.csv")