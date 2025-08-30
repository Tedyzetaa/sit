# SIT - Sistema de Inteligência do Teddy

## Sobre o Projeto
O SIT é um assistente de voz e texto com interface gráfica (GUI), projetado para executar uma variedade de tarefas no seu computador, desde consultas simples até a automação de programas. O projeto é modular e permite a fácil integração de novas funcionalidades.

## Funcionalidades
* **Comandos de Voz/Texto**: Use o microfone ou a caixa de texto para interagir com o assistente.
* **Informações Diversas**: Obtenha a hora atual, notícias, piadas e a previsão do tempo.
* **Integração com Programas**: Abra programas como o Google Chrome e o VSCode.
* **Reprodução de Mídia**: Peça para o assistente tocar músicas no YouTube.
* **Automação e Ferramentas**: Tire screenshots, feche abas do Chrome e obtenha informações de IP.
* **Integração com MidPainel**: O assistente pode iniciar e executar o programa `main.py` do seu projeto MidPainel em um novo terminal.

## Requisitos
Para rodar o SIT, você precisa ter as seguintes bibliotecas Python instaladas. Use o `pip` para instalá-las:
* `SpeechRecognition`
* `pyjokes`
* `gtts`
* `simpleaudio`
* `requests`
* `beautifulsoup4`
* `pyautogui`
* `netifaces`
* `shazamio`
* `Youtube`
* `ffplay` (componente do FFmpeg, necessário para reprodução de áudio).

## Como Usar
1.  **Verifique os Códigos**: Certifique-se de que os seus arquivos `main.py`, `gui.py` e `commands.py` estejam atualizados com as últimas versões.
2.  **Inicie o Assistente**: Execute o arquivo `gui.py` para abrir a interface gráfica.
3.  **Use os Comandos**:
    * **Por Texto**: Digite seu comando na caixa de texto e pressione "Enter" ou clique em "Enviar".
    * **Por Voz**: Clique no botão do microfone e fale o comando desejado.

## Histórico de Versões

### **Versão 2.0**
* Lançamento inicial do projeto.
* Funcionalidades básicas de voz e texto implementadas.
* Comandos como "olá", "hora" e "conte uma piada" foram adicionados.

### **Versão 2.1**
* **Atualização**: Adição do comando `abrir midpainel`.
* **Melhoria**: A integração permite que o assistente inicie o projeto MidPainel em um processo separado usando a biblioteca `subprocess.Popen`.

### **Versão 2.5**
* **Correção de Bug**: Resolvido o `TypeError` que ocorria ao chamar comandos que não exigiam entrada de voz adicional. A lógica no `main.py` foi ajustada para passar o número correto de argumentos (`falar` e `ouvir_comando`) para cada função.

### **Versão 2.8**
* **Correção de Bug**: Resolvido o problema de travamento da interface.
* **Melhoria**: A lógica de processamento de comandos no `gui.py` foi refatorada para usar `threading.Thread`, garantindo que o assistente permaneça responsivo mesmo durante a execução de tarefas demoradas.

### **Versão 2.9 (Atual)**
* **Estabilidade**: A versão final consolida todas as correções anteriores.
* **Refinamento**: O código está mais robusto e pronto para uso contínuo, permitindo que você interaja com o assistente de forma fluida e sem interrupções.