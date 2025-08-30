import speech_recognition as sr

def testar_ouvir():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ajustando para o ruído do ambiente...")
        microfone.adjust_for_ambient_noise(source)
        print("Diga algo, por favor...")
        try:
            audio = microfone.listen(source, timeout=5)
            print("Áudio capturado. Processando...")
            comando = microfone.recognize_google(audio, language='pt-BR')
            print(f"Você disse: {comando}")
        except sr.WaitTimeoutError:
            print("Tempo de espera excedido. Nenhum áudio detectado.")
        except sr.UnknownValueError:
            print("Não foi possível entender o áudio.")
        except sr.RequestError as e:
            print(f"Erro no serviço de reconhecimento de voz do Google: {e}")

if __name__ == "__main__":
    testar_ouvir()