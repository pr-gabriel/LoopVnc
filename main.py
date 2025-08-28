import subprocess
import time
import os
import random
import tkinter as tk
import threading

label_mensagem = None
label_historico = None
ultimos_hosts = []
janela_host = None
janela_hist = None

def iniciar_interfaces():
    def criar_janela_host():
        global label_mensagem, janela_host
        janela_host = tk.Tk()
        janela_host.title("Host")
        janela_host.geometry("440x220+1480+860")
        janela_host.attributes("-topmost", True)
        janela_host.overrideredirect(True)
        label_mensagem = tk.Label(janela_host, text="", font=("Arial", 35))
        label_mensagem.pack(expand=True)
        janela_host.mainloop()

    def criar_janela_hist():
        global label_historico, janela_hist
        janela_hist = tk.Tk()
        janela_hist.title("Historico")
        janela_hist.geometry("350x220+0+860")
        janela_hist.attributes("-topmost", True)
        janela_hist.overrideredirect(True)
        label_historico = tk.Label(janela_hist, text="", font=("Arial", 18), justify="left", anchor="nw")
        label_historico.pack(expand=True, fill='both', padx=10, pady=10)
        janela_hist.mainloop()

    threading.Thread(target=criar_janela_host, daemon=True).start()
    threading.Thread(target=criar_janela_hist, daemon=True).start()
    time.sleep(1)  # Garante que as janelas sejam criadas antes da atualizacao

def atualizar_mensagem(mensagem):
    if label_mensagem:
        label_mensagem.config(text=mensagem)

def atualizar_historico(novo_host):
    global ultimos_hosts
    ultimos_hosts.append(novo_host)
    if len(ultimos_hosts) > 6:
        ultimos_hosts.pop(0)
    texto = "HISTORICO HOSTS: \n" + "\n".join(ultimos_hosts[-6:][::-1])
    if label_historico:
        label_historico.config(text=texto)

def criar_arquivo(nome):
    arquivo = f"""
ClientCutText=1
ConnMethod=tcp
ConnTime=2024-01-19T15:46:34.913z
Emulate3=0
FullScreen=0
Host={nome}::7007
Password=04eaafa663af8e0d
SendKeyEvents=0
ServerCutText=0
Shared=1
ShareFiles=0
UUid=8c26b451-eed1-4fbf-aae3-e8142bd36f8b
viewonly=0
FullScreen=1
Quality=Low
AcceptBell=1
"""
    path = f"/home/admin/Desktop/tighvnc/temp/{nome}.vnc"
    if not os.path.exists(path):
        with open(path, "w") as documento:
            documento.write(arquivo)

def abrir_fechar_vnc(host, duration=20):
    config_file = f"/home/admin/Desktop/tighvnc/temp/{host}.vnc"
    if not os.path.exists(config_file):
        criar_arquivo(host)
    try:
        command = ["vncviewer", "-config", config_file]
        process = subprocess.Popen(command)
        print(f"Acesso {config_file} iniciado.")
        time.sleep(duration)
        process.kill()
    except Exception as e:
        with open("/home/admin/erro_tighvnc.log", "a") as log:
            log.write(f"Erro ao abrir/fechar VNC para {host}: {str(e)}\n")

def abri_host():
    path = "/home/admin/Desktop/tighvnc/names"
    with open(path, "r") as arquivo:
        conteudo = arquivo.read().split("\n")
    return [x.strip() for x in conteudo if x.strip() != ""]

def ler_Identities(host):
    path = "/home/admin/.vnc/identities"
    with open(path, "r") as arquivo:
        conteudo = arquivo.read().split("\n")
    if not any(linha.split(":")[0] == host for linha in conteudo if linha):
        with open(path, "a") as arq:
            arq.write(f"{host}::7007/extra=0201\n")

if __name__ == "__main__":
    iniciar_interfaces()
    while True:
        try:
            hosts = abri_host()
            random.shuffle(hosts)
            for y in hosts:
                ler_Identities(y)
                tempo_espera = 35
                criar_arquivo(y)
                atualizar_mensagem(y)
                abrir_fechar_vnc(y, tempo_espera)
                atualizar_historico(y)
                time.sleep(2)
        except Exception as e:
            with open("/home/admin/erro_tighvnc.log", "a") as log:
                log.write(f"Erro geral no loop: {str(e)}\n")
            time.sleep(5)
