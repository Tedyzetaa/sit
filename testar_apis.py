import requests
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

def checar_api(nome, url):
    """Verifica se uma API está online."""
    print(f"Testando a API: {nome}...")
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ A API {nome} está ONLINE.")
        elif response.status_code == 401 or response.status_code == 403:
            print(f"⚠️ A API {nome} retornou um erro de autenticação (código {response.status_code}). A URL está correta, mas a chave de API pode estar faltando ou ser inválida.")
        else:
            print(f"❌ A API {nome} retornou um erro inesperado (código {response.status_code}).")
    except requests.exceptions.Timeout:
        print(f"❌ A API {nome} excedeu o tempo limite. Ela pode estar offline ou muito lenta.")
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Falha ao conectar na API {nome}. Ela está OFFLINE ou o endereço não existe.")
        print(f"Detalhes do erro: {e}")
    except Exception as e:
        print(f"❌ Ocorreu um erro desconhecido ao testar a API {nome}.")
        print(f"Detalhes do erro: {e}")
    print("-" * 30)

if __name__ == "__main__":
    # APIs que não precisam de chaves de acesso
    checar_api("IP-API", "http://ip-api.com/json/")
    checar_api("CoinGecko", "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=brl")
    
    # API de consulta que sabemos que pode estar offline
    checar_api("GhostCenter (CPF)", "http://ghostcenter.xyz/api/cpf/12345678900")
    checar_api("GhostCenter (Nome)", "http://ghostcenter.xyz/api/nome/joao")

    # APIs que precisam de uma chave de API para funcionar corretamente
    # Chave de API de notícias
    news_api_key = os.getenv("NEWS_API_KEY")
    if news_api_key:
        checar_api("NewsAPI", f"https://newsapi.org/v2/top-headlines?country=br&apiKey={news_api_key}")
    else:
        print("⚠️ Chave NEWS_API_KEY não encontrada no arquivo .env. Pulando o teste da NewsAPI.")
        print("-" * 30)

    # Chave de API do clima
    weather_api_key = os.getenv("WEATHER_API_KEY")
    if weather_api_key:
        checar_api("OpenWeatherMap", f"http://api.openweathermap.org/data/2.5/weather?q=Nova%20Andradina&appid={weather_api_key}")
    else:
        print("⚠️ Chave WEATHER_API_KEY não encontrada no arquivo .env. Pulando o teste da OpenWeatherMap.")
        print("-" * 30)
    
    print("Teste de APIs concluído.")