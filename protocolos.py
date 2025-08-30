import os

protocolo_ativo = False

def ativar_protocolo_seguranca(falar):
    global protocolo_ativo
    if not protocolo_ativo:
        protocolo_ativo = True
        falar("Qual protocolo o senhor gostaria de ativar?")
        print("Protocolo de segurança: ATIVADO.")
    else:
        falar("O protocolo de segurança já está ativo.")
        print("Protocolo de segurança: JÁ ESTÁ ATIVO.")

def desativar_protocolo_seguranca(falar):
    global protocolo_ativo
    if protocolo_ativo:
        protocolo_ativo = False
        falar("Protocolo de segurança desativado.")
        print("Protocolo de segurança: DESATIVADO.")
    else:
        falar("O protocolo de segurança já está desativado.")
        print("Protocolo de segurança: JÁ ESTÁ DESATIVADO.")

def protocolo_mine(falar):
    falar("Ativando o protocolo mine.")
    try:
        caminho_base = os.path.dirname(os.path.abspath(__file__))
        caminho_executavel = os.path.join(caminho_base, "miner", "unMiner.exe")
        os.system(f'start "" "{caminho_executavel}"')
        print(f"Tentando iniciar: {caminho_executavel}")
    except Exception as e:
        falar("Não foi possível iniciar o programa. Verifique o caminho.")
        print(f"Erro ao iniciar minerador: {e}")

def verificar_protocolo():
    global protocolo_ativo
    return protocolo_ativo