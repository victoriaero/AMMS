import os
import csv
from collections import defaultdict
from datetime import datetime

def obter_primeiro_ultimo_datetime(caminho_servidor):
    primeiro_datetime = None
    ultimo_datetime = None
    for arquivo in os.listdir(caminho_servidor):
        if arquivo.endswith(".txt"):
            caminho_arquivo = os.path.join(caminho_servidor, arquivo)
            with open(caminho_arquivo, 'r', encoding='utf-8') as file:
                for linha in file:
                    if '$#fim#$' in linha:
                        parts = linha.strip().split(',')
                        if len(parts) >= 1:
                            timestamp = parts[0].strip()
                            try:
                                timestamp_datetime = datetime.fromisoformat(timestamp)
                                if primeiro_datetime is None or timestamp_datetime < primeiro_datetime:
                                    primeiro_datetime = timestamp_datetime
                                if ultimo_datetime is None or timestamp_datetime > ultimo_datetime:
                                    ultimo_datetime = timestamp_datetime
                            except ValueError:
                                pass
    return primeiro_datetime, ultimo_datetime

def gerar_csv_dados(diretorio_principal, arquivo_saida):
    contagem_deleted_users_servidor = {}
    contagem_total_mensagens_servidor = {}
    razao_deleted_users_mensagens_servidor = {}
    server_users = defaultdict(set)
    qtd_canais_texto_servidor = {}

    with open(arquivo_saida, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['server', 'qtt_users', 'tot_msg', 'msg_deleted_users', 'qtt_cha', 'rat_dlt_tot_msg', 'first_datetime', 'last_datetime']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for servidor in os.listdir(diretorio_principal):
            caminho_servidor = os.path.join(diretorio_principal, servidor)
            if os.path.isdir(caminho_servidor):
                contagem_servidor = 0
                total_mensagens_servidor = 0
                primeiro_datetime, ultimo_datetime = obter_primeiro_ultimo_datetime(caminho_servidor)
                qtd_canais_texto = sum(1 for arquivo in os.listdir(caminho_servidor) if arquivo.endswith(".txt"))
                qtd_canais_texto_servidor[servidor] = qtd_canais_texto
                for arquivo in os.listdir(caminho_servidor):
                    if arquivo.endswith(".txt"):
                        caminho_arquivo = os.path.join(caminho_servidor, arquivo)
                        with open(caminho_arquivo, 'r', encoding='utf-8') as file:
                            for linha in file:
                                total_mensagens_servidor += 1
                                if 'Deleted User' in linha:
                                    contagem_servidor += 1
                                parts = linha.strip().split(',')
                                if len(parts) >= 2:
                                    user_id = parts[1].strip()
                                    server_users[servidor].add(user_id)
                contagem_deleted_users_servidor[servidor] = contagem_servidor
                contagem_total_mensagens_servidor[servidor] = total_mensagens_servidor
                if total_mensagens_servidor != 0:
                    razao_deleted_users_mensagens_servidor[servidor] = contagem_servidor / total_mensagens_servidor
                else:
                    razao_deleted_users_mensagens_servidor[servidor] = 0

                writer.writerow({
                    'server': servidor,
                    'qtt_users': len(server_users[servidor]),
                    'tot_msg': total_mensagens_servidor,
                    'msg_deleted_users': contagem_servidor,
                    'qtt_cha': qtd_canais_texto,
                    'rat_dlt_tot_msg': razao_deleted_users_mensagens_servidor[servidor],
                    'first_datetime': primeiro_datetime.strftime('%Y-%m-%d %H:%M:%S') if primeiro_datetime else None,
                    'last_datetime': ultimo_datetime.strftime('%Y-%m-%d %H:%M:%S') if ultimo_datetime else None
                })

    return arquivo_saida

caminho_para_o_diretorio_principal = "/home/victoriaero/AMMS/data"
arquivo_saida = 'colected_info.csv'

resultado_arquivo = gerar_csv_dados(caminho_para_o_diretorio_principal, arquivo_saida)
print(f"Resultados salvos em: {resultado_arquivo}")