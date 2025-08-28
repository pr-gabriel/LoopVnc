import os

# Caminho da pasta com os arquivos .vnc
caminho_pasta = r"C:\Users\greis\Documents\Hosts - VNC 30-04-2025"

# Lista para armazenar os hosts
hosts = []

# Percorre todos os arquivos da pasta
for nome_arquivo in os.listdir(caminho_pasta):
    if nome_arquivo.lower().endswith('.vnc'):
        caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                if linha.startswith('Host='):
                    host = linha.strip().split('=')[1].split(':')[0]
                    hosts.append(host)

# Remove duplicatas e salva no arquivo de saída
hosts_unicos = sorted(set(hosts))
with open("hosts_extraidos.txt", "w", encoding='utf-8') as saida:
    for host in hosts_unicos:
        saida.write(host + "\n")

print("Extracao concluida com sucesso. Verifique o arquivo 'hosts_extraidos.txt'.")