# Caracterização do uso do Discord no Brasil

O presente repositório é referente ao projeto da disciplina de Análise e Mineração de Mídias Socias. O nosso objetivo é realizar uma coleta e caracterização de mensagens compartilhadas em servidores públicos do Discord no Brasil. Discentes:
* Arthur Buzelin Galery                  2022043230
* Pedro Augusto Torres Bento             2022104352
* Victoria Estanislau Ramos de Oliveira  2021037490

### Trabalho Prático 1: Coleta de Dados

Em nosso repositório, a pasta ```discord_scrap``` possui os códigos utilizados para a realização da coleta.

* O arquivo ```servers_scrap.py``` foi utilizado para realizar a coleta dos nomes e ids dos servidores, armazenando estas informações em um arquivo csv. Para isso, é preciso realizar a instalação da biblioteca *BeautifulSoup*, ```$ apt-get install python3-bs4```. Antes de rodar o arquivo, é preciso copiar o html da página que deseja coletar os servidores e inserir o código no arquivo ```input.html```. Lá já se encontra um html de exemplo para verificação.
* O arquivo ```messages_scrap.py``` foi utilizado para acessar os servidores e coletar as mensagens de todos os canais disponíveis. Para isso, é preciso inserir o *Authorization Key* na linha 110, que é referente a autorização de uma conta do Discord.
