import speech_recognition as sr
import commands
import os
import sys

# Mapeia os comandos de voz para as funções correspondentes em commands.py
comandos_map = {
    "olá": commands.dizer_ola,
    "hora": commands.dizer_hora,
    "conte uma piada": commands.contar_piada,
    "notícias": commands.obter_noticias_principais,
    "preço do bitcoin": lambda falar, ouvir_comando: commands.obter_cotacao_cripto(falar, "bitcoin"),
    "preço do ethereum": lambda falar, ouvir_comando: commands.obter_cotacao_cripto(falar, "ethereum"),
    "cotação do bitcoin": lambda falar, ouvir_comando: commands.obter_cotacao_cripto(falar, "bitcoin"),
    "cotação do ethereum": lambda falar, ouvir_comando: commands.obter_cotacao_cripto(falar, "ethereum"),
    "tirar print": lambda falar, ouvir_comando: commands.tirar_print_e_salvar(falar, ouvir_comando),
    "fechar abas": lambda falar: commands.fechar_abas_chrome(falar),
    "mutar áudio": lambda falar: commands.mutar_audio(falar),
    "desmutar áudio": lambda falar: commands.desmutar_audio(falar),
    "tchau": lambda falar: commands.desligar_assistente(falar),
    "desligar": lambda falar: commands.desligar_assistente(falar),
    "até logo": lambda falar: commands.desligar_assistente(falar),
    "consultar cpf": lambda falar, ouvir_comando: commands.consultar_cpf(falar, ""),
    "consultar nome": lambda falar, ouvir_comando: commands.consultar_nome(falar, ""),
    "consultar ip": lambda falar, ouvir_comando: commands.consultar_ip(falar, ""),
    "qual meu ip": lambda falar: commands.consultar_meu_ip(falar),
    "tocar música": lambda falar, ouvir_comando: commands.tocar_musica(falar, ouvir_comando),
    "tocar canção": lambda falar, ouvir_comando: commands.tocar_musica(falar, ouvir_comando),
    "abrir chrome": lambda falar: commands.abrir_programa(falar, "chrome"),
    "abrir vscode": lambda falar: commands.abrir_programa(falar, "code"),
    "pesquisar": lambda falar, ouvir_comando: commands.pesquisar_google(falar, ""),
    "previsão do tempo": lambda falar, ouvir_comando: commands.obter_previsao_do_tempo(falar, ouvir_comando),
    "interagir com gemini": lambda falar, ouvir_comando: commands.interagir_com_gemini(falar, ouvir_comando),
    "abrir midpainel": lambda falar: commands.abrir_midpainel(falar),
}

def executar_comando(comando, falar, ouvir_comando):
    rodando = True
    comando_encontrado = False

    # Verifica comandos específicos primeiro
    if comando.lower() in comandos_map:
        func = comandos_map[comando.lower()]
        # Decide quantos argumentos a função precisa
        if func.__code__.co_argcount == 2:
            func(falar, ouvir_comando)
        else:
            func(falar)
        comando_encontrado = True
    
    # Processa comandos de pesquisa e programas
    elif comando.startswith("pesquisar "):
        query = comando.split("pesquisar ", 1)[1]
        commands.pesquisar_google(falar, query)
        comando_encontrado = True
    elif comando.startswith("abrir "):
        programa = comando.split("abrir ", 1)[1]
        commands.abrir_programa(falar, programa)
        comando_encontrado = True

    if not comando_encontrado:
        falar("Desculpe, não entendi o comando. Por favor, tente novamente.")
    
    return rodando, ""