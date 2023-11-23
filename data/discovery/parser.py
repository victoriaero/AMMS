from bs4 import BeautifulSoup
import re

# Load the HTML content
with open('raw1001-1086.html', 'r') as file:
    html_content = file.read()

# Create a BeautifulSoup object
soup = BeautifulSoup(html_content, 'html.parser')

# Prepare a list to hold server information
servers_info = []

# Find all server cards
server_cards = soup.find_all('div', class_='card__33bd0')

for card in server_cards:
    # Find server name
    server_name = card.find('h2', class_='defaultColor__77578 heading-md-semibold__574c7 defaultColor__87d87 headerTitle_deb2f4').get_text(strip=True).replace(',', '')

    # Find server ID (Extracted from the image source URL)
    img_src = card.find('img', class_='avatar_c551f0')['src']
    server_id = re.search(r'/icons/(\d+)/', img_src).group(1)

    # Find all occurrences of the member count and select the second one
    member_counts = card.find_all('div', class_='text-xs-normal__56c35')
    if len(member_counts) >= 2:
        members = member_counts[1].get_text(strip=True).replace(' membros', '').replace('.', '')
    else:
        members = 'Not available'

    # Append the server info to the list
    servers_info.append(f"{server_name}, {server_id}, {members}")

# Write results to a text file
with open('1-1000.txt', 'w') as file:
    for info in servers_info:
        file.write(info + '\n')

print("Information extracted and saved to servers_info.txt.")
