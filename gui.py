import tkinter as tk
from tkinter import scrolledtext
import threading
import sys
import os
import subprocess
import requests
import speech_recognition as sr
import time

# Certifique-se de que o diretório pai esteja no PATH para importar main e commands
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import executar_comando
from gtts import gTTS
import simpleaudio as sa
import time

class VoiceAssistantGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("SIT")
        self.geometry("800x600")
        self.config(bg="#36454F")

        self.chat_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, bg="#4A5B6A", fg="white", font=("Helvetica", 12))
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.entry_frame = tk.Frame(self, bg="#36454F")
        self.entry_frame.pack(padx=10, pady=10, fill=tk.X)

        self.user_input_entry = tk.Entry(self.entry_frame, bg="#4A5B6A", fg="white", font=("Helvetica", 12))
        self.user_input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        self.user_input_entry.bind("<Return>", self.on_send_button_click)

        self.send_button = tk.Button(self.entry_frame, text="Enviar", command=self.on_send_button_click, bg="#6A829A", fg="white", font=("Helvetica", 10, "bold"))
        self.send_button.pack(side=tk.RIGHT, padx=5)

        self.mic_button = tk.Button(self.entry_frame, text="🎙️", command=self.on_mic_button_click, bg="#6A829A", fg="white", font=("Helvetica", 10, "bold"))
        self.mic_button.pack(side=tk.RIGHT)

        self.rodando = True
        
        self.menu_options = {
            "dizer_ola": "Olá",
            "dizer_hora": "Hora",
            "conte_uma_piada": "Conte uma piada",
            "noticias": "Notícias",
            "previsao_do_tempo": "Previsão do tempo",
            "abrir_midpainel": "Abrir MidPainel",
            "consultar_cpf": "Consultar CPF",
            "consultar_nome": "Consultar nome",
            "consultar_ip": "Consultar IP",
            "qual_meu_ip": "Qual meu IP",
            "tocar_musica": "Tocar música",
            "pesquisar_google": "Pesquisar no Google",
            "desligar_assistente": "Desligar"
        }
        self.create_menu()

        self.display_message("Olá, eu sou SIT, Sistema de Inteligência do Teddy, o que você gostaria?")

    def display_message(self, message, sender="SIT"):
        self.chat_area.config(state=tk.NORMAL)
        if sender == "SIT":
            self.chat_area.insert(tk.END, f"{message}\n", "sit_message")
            self.chat_area.tag_configure("sit_message", foreground="#ADD8E6", background="#36454F", justify="left")
        else:
            self.chat_area.insert(tk.END, f"{message}\n", "user_message")
            self.chat_area.tag_configure("user_message", foreground="#90EE90", background="#36454F", justify="right")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)

    def on_send_button_click(self, event=None):
        comando = self.user_input_entry.get()
        self.display_message(comando, "Usuário")
        self.user_input_entry.delete(0, tk.END)
        threading.Thread(target=self.processar_comando_thread, args=(comando,)).start()

    def on_mic_button_click(self):
        self.display_message("Ouvindo...", "SIT")
        threading.Thread(target=self.processar_comando_por_voz_thread).start()

    def create_menu(self):
        self.menu = tk.Menu(self, bg="#4A5B6A", fg="white")
        self.config(menu=self.menu)

        comandos_menu = tk.Menu(self.menu, tearoff=0, bg="#4A5B6A", fg="white")
        self.menu.add_cascade(label="Comandos", menu=comandos_menu)

        for text, command in self.menu_options.items():
            comandos_menu.add_command(label=command, command=lambda cmd=text: threading.Thread(target=self.processar_comando_menu_thread, args=(cmd,)).start())

    def processar_comando_menu_thread(self, comando_key):
        comando_texto = self.menu_options.get(comando_key)
        self.display_message(f"Comando selecionado pelo menu: {comando_texto}", "Usuário")
        self.processar_comando_thread(comando_texto)
    
    def falar(self, texto):
        if not self.rodando:
            return
        self.display_message(texto)
        try:
            tts = gTTS(text=texto, lang='pt', slow=False)
            tts.save("response.mp3")
            subprocess.run(['ffplay', '-nodisp', '-autoexit', 'response.mp3'], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            os.remove("response.mp3")
        except FileNotFoundError:
            print("Aviso: O ffplay não foi encontrado. A voz não será reproduzida.")
        except Exception as e:
            print(f"Erro ao reproduzir áudio: {e}")

    def ouvir_comando(self):
        # Esta é uma versão dummy para o modo de texto
        self.display_message("Estou ouvindo. Por favor, digite o seu comando.", "SIT")
        return self.user_input_entry.get()

    def processar_comando_thread(self, comando):
        comando_processado = comando.lower()
        rodando, resposta = executar_comando(comando_processado, self.falar, self.ouvir_comando)
        if not rodando:
            self.rodando = False
            self.quit()

    def processar_comando_por_voz_thread(self):
        comando = self.ouvir_comando_real()
        if comando:
            self.display_message(comando, "Usuário")
            self.processar_comando_thread(comando)
        else:
            self.display_message("Desculpe, não entendi o que você disse.", "SIT")

    def ouvir_comando_real(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                self.falar("Ouvindo...")
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source, timeout=5)
                comando_voz = r.recognize_google(audio, language="pt-BR")
                return comando_voz
            except sr.UnknownValueError:
                self.falar("Desculpe, não entendi o que você disse.")
                return None
            except sr.RequestError:
                self.falar("Erro no serviço de reconhecimento de fala.")
                return None
            except Exception as e:
                print(f"Erro ao ouvir: {e}")
                return None

if __name__ == "__main__":
    app = VoiceAssistantGUI()
    app.mainloop()