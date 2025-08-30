import os
import requests
from bs4 import BeautifulSoup
import webbrowser
import datetime
import pyjokes
import wikipedia
import pyautogui
import platform
import subprocess
import json
from shazamio import Shazam
import simpleaudio as sa
from gtts import gTTS
import time
import netifaces
from youtube_search import YoutubeSearch

# ==================== FUNÇÕES DE COMANDO ====================

def dizer_ola(falar):
    falar("Olá! Em que posso ajudar?")

def pesquisar_google(falar, query):
    if query:
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        falar(f"Pesquisando por {query} no Google.")
    else:
        falar("Por favor, diga o que você gostaria de pesquisar.")

def obter_noticias_principais(falar):
    api_key = os.getenv("NEWS_API_KEY")
    
    if not api_key:
        falar("A chave de API para notícias não está configurada.")
        return

    try:
        url = f"https://newsapi.org/v2/top-headlines?country=br&apiKey={api_key}"
        response = requests.get(url)
        data = response.json()
        
        if data["status"] == "ok" and data["articles"]:
            falar("Aqui estão as notícias mais recentes:")
            for article in data["articles"][:5]:
                falar(article['title'])
                time.sleep(1)
        else:
            falar("Não foi possível obter as notícias no momento.")
    except Exception as e:
        falar("Ocorreu um erro ao tentar obter as notícias.")
        print(f"Erro ao obter notícias: {e}")

def obter_previsao_do_tempo(falar, ouvir_comando):
    api_key = os.getenv("WEATHER_API_KEY")

    if not api_key:
        falar("A chave de API para previsão do tempo não está configurada.")
        return

    falar("Para qual cidade você gostaria da previsão?")
    cidade = ouvir_comando()

    if cidade:
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&units=metric&lang=pt_br"
            response = requests.get(url)
            data = response.json()

            if data["cod"] == 200:
                temp_celsius = data["main"]["temp"]
                descricao = data["weather"][0]["description"]
                falar(f"A temperatura em {cidade} é de {temp_celsius:.1f} graus Celsius, com {descricao}.")
            else:
                falar(f"Não foi possível encontrar a previsão para {cidade}.")
        except Exception as e:
            falar("Ocorreu um erro ao tentar obter a previsão do tempo.")
            print(f"Erro ao obter a previsão: {e}")

def interagir_com_gemini(falar, ouvir_comando):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        falar("A chave da API Gemini não está configurada.")
        return

    falar("O que você gostaria de me perguntar?")
    pergunta = ouvir_comando()

    if pergunta:
        falar("Desculpe, a funcionalidade do Gemini ainda não está implementada.")
        print(f"Chave da API Gemini usada: {api_key}")

def dizer_hora(falar):
    hora_atual = datetime.datetime.now().strftime("%H:%M")
    falar(f"Agora são {hora_atual}.")

def contar_piada(falar):
    falar("Pronto para rir?")
    piada = pyjokes.get_joke(language='en', category='all')
    falar(piada)

def abrir_programa(falar, programa):
    try:
        if platform.system() == "Windows":
            os.startfile(programa)
        else:
            subprocess.Popen([programa])
        falar(f"Abrindo {programa}.")
    except Exception as e:
        falar(f"Não foi possível abrir o programa {programa}.")
        print(f"Erro ao abrir programa: {e}")

def tocar_musica(falar, ouvir_comando):
    falar("Qual música você gostaria de ouvir?")
    musica = ouvir_comando()
    if musica:
        try:
            results = YoutubeSearch(musica, max_results=1).to_dict()
            if results:
                url = f"https://www.youtube.com/watch?v={results[0]['id']}"
                webbrowser.open(url)
                falar(f"Reproduzindo {results[0]['title']} no YouTube.")
            else:
                falar("Não encontrei a música no YouTube.")
        except Exception as e:
            falar("Ocorreu um erro ao tentar reproduzir a música no YouTube.")
            print(f"Erro ao tocar música: {e}")
    else:
        falar("Por favor, diga o nome da música.")

def reconhecer_musica(falar):
    falar("Ouvindo para reconhecer a música...")
    async def get_song():
        try:
            shazam = Shazam()
            song = await shazam.recognize_song()
            falar(f"A música que está tocando é: {song.track.title} de {song.track.subtitle}")
        except Exception as e:
            falar("Não foi possível reconhecer a música.")
            print(f"Erro no Shazam: {e}")
            
    # Lógica para rodar a função assíncrona
    # asyncio.run(get_song())

def criar_lembrete(falar):
    falar("O que você gostaria que eu lembrasse?")
    lembrete = ouvir_comando()
    if lembrete:
        falar("Lembrete criado com sucesso.")
    else:
        falar("Desculpe, não entendi. Por favor, tente novamente.")

def criar_prompt(falar):
    falar("Qual prompt você gostaria de criar?")
    prompt = ouvir_comando()
    if prompt:
        falar("Prompt criado com sucesso.")
    else:
        falar("Desculpe, não entendi o que você disse. Por favor, tente novamente.")

def obter_cotacao_cripto(falar, cripto):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={cripto}&vs_currencies=brl"
        response = requests.get(url)
        data = json.loads(response.text)
        preco = data[cripto]["brl"]
        falar(f"A cotação do {cripto} é de {preco:.2f} reais.")
    except Exception as e:
        falar(f"Não foi possível obter a cotação do {e}.")
        print(f"Erro na cotação: {e}")

def tirar_print_e_salvar(falar, ouvir_comando):
    try:
        screenshot = pyautogui.screenshot()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"screenshot_{timestamp}.png"
        screenshot.save(filename)
        falar(f"Printscreen salvo como {filename}.")
        
        falar("Gostaria de pesquisar essa imagem no Google?")
        resposta = ouvir_comando()
        if "sim" in resposta:
            falar("Pesquisando a imagem no Google...")
    except Exception as e:
        falar("Não foi possível tirar o printscreen.")
        print(f"Erro ao tirar print: {e}")

def fechar_abas_chrome(falar):
    falar("Fechando abas do Chrome...")

def mutar_audio(falar):
    falar("Áudio mutado.")

def desmutar_audio(falar):
    falar("Áudio desmutado.")

# === Funções de Consulta de Dados (Agora com aviso de serviço offline) ===

def consultar_cpf(falar, cpf_input):
    falar("A função de consulta de CPF está temporariamente indisponível. O serviço de API que ela utiliza está offline.")

def consultar_nome(falar, nome_input):
    falar("A função de consulta de nome está temporariamente indisponível. O serviço de API que ela utiliza está offline.")

def consultar_ip(falar, ip_input):
    if not ip_input:
        falar("Por favor, diga o IP que você quer consultar.")
        return

    try:
        request = requests.get(f'http://ip-api.com/json/{ip_input}')
        rjson = request.json()

        if rjson['status'] == 'fail':
            falar("IP não encontrado.")
        else:
            falar(f"IP {rjson['query']} encontrado. País: {rjson['country']}, Cidade: {rjson['city']}, Fornecedor de Rede: {rjson['isp']}.")
    except Exception as e:
        falar("Ocorreu um erro ao consultar o IP. O serviço pode estar indisponível.")
        print(f"Erro ao consultar IP: {e}")

def consultar_meu_ip(falar):
    try:
        gateways = netifaces.gateways()
        gateway_padrao = gateways['default'][netifaces.AF_INET][0]
        falar(f"O endereço de IP do seu computador é {gateway_padrao}.")
    except Exception as e:
        falar("Não foi possível obter o seu endereço de IP.")
        print(f"Erro ao consultar meu IP: {e}")

def desligar_assistente(falar):
    falar("Desligando, até logo!")

def abrir_midpainel(falar):
    caminho_midpainel = r"C:\MidPainel\main.py"  # Use r"..." para evitar erros com as barras
    try:
        falar("Abrindo o MidPainel.")
        subprocess.Popen(['python', caminho_midpainel])
    except FileNotFoundError:
        falar("Não foi possível encontrar o arquivo do MidPainel.")
    except Exception as e:
        falar("Ocorreu um erro ao tentar abrir o MidPainel.")
        print(f"Erro ao abrir MidPainel: {e}")