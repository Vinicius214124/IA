from flask import Flask, render_template, request, jsonify
import json
from flask_cors import CORS
import google.generativeai as genai

# Configuração da API do Google
genai.configure(api_key="AIzaSyAdr7ebyuoqW_b-R6qPUTCm1sxu79OABug")

# Configuração do modelo
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

# Criando o app Flask
app = Flask(__name__)
CORS(app)

# Processos
def load_processes():
    with open('processos.json', 'r', encoding='utf-8') as file:
        return json.load(file)

# Carregar os processos ao iniciar o app
PROCESSES = load_processes()

# Instrução do papel da IA
ROLE_MESSAGE = (
    """
    Já estamos em contato com o cliente, não solicite para entrar em contato com o cliente, apenas informe para avisar ou pedir ao cliete.
    Eu ajudo a responder clientes. Quando o cliente faz uma pergunta, eu forneço respostas claras e objetivas com base no que ele precisa informar.
    Caso um processo específico não seja encontrado, responda de forma espontânea, como o analista poderia dizer ou informar, com base na mensagem recebida e informe para consultar com um N2.
    Caso um usuario informe que nao entendeu ou solicitar para explicar de novo o processo passado, explique novamente.
    Eu ajudo analistas responder clientes.
    Eu não preciso ser tão formal.
    Eu ajudo clientes no atendimento de uma casa de aposta sobre processos informados.
    Quando alguém ficar com dúvida de alguma parte do processo, irei tentar ajudá-lo da melhor forma, e de forma mais clara possível.
    Eu ajudo apenas os analistas a responder clientes do setor de suporte, não atendo cliente final.
    Meu criador é o Gustavo Moura.
    O e-mail dele é gustavo.moura@hrgama.
    Eu apenas passo informações para os clientes com dúvidas.
    """
)

# Variáveis globais
user_area = "Reals"  # Definir a área "Reals" por padrão
last_matched_process = None
repeated_message_count = 0

@app.route('/')
def home():
    return render_template('index.html')

# Rota para adicionar um atalho no iPhone
@app.route('/add-to-home')
def add_to_home():
    return '''
    <html>
    <head>
        <title>Adicionar Atalho</title>
        <link rel="apple-touch-icon" href="/static/images/download.png">
        <script>
            if (navigator.userAgent.includes('iPhone')) {
                document.location.href = 'https://processos-ux.onrender.com';
            }
        </script>
    </head>
    <body>
        <h2>Para adicionar o atalho ao seu iPhone:</h2>
        <p>1. Toque no botão de compartilhamento (ícone de quadrado com seta para cima).</p>
        <p>2. Escolha "Adicionar à Tela de Início".</p>
        <p>3. Confirme o nome do aplicativo e toque em "Adicionar".</p>
    </body>
    </html>
    '''

@app.route('/chat', methods=['POST'])
def chat_with_bot():
    global user_area, last_matched_process, repeated_message_count

    user_message = request.json.get('message', "").strip().lower()
    if not user_message:
        return jsonify({'response': 'Erro: Nenhuma mensagem recebida.'})

    if user_message in ["reals"]:
        repeated_message_count += 1
        if repeated_message_count > 2:
            return jsonify({'response': f"Já entendi que você atende {user_message.upper()}!"})
    else:
        repeated_message_count = 0

    if "não entendi" in user_message or "explique novamente" in user_message or "me explique" in user_message:
        if last_matched_process:
            prompt = (
                f"{ROLE_MESSAGE}\n\n"
                f"O processo é o seguinte: {last_matched_process}\n"
                "Explique de forma clara e detalhada como o analista deve proceder, usando linguagem acessível e didática."
            )
            try:
                response = chat.send_message(prompt)
                return jsonify({'response': response.text})
            except Exception as e:
                print(f"Erro ao chamar a API do Google: {e}")
                return jsonify({'response': "Desculpe, houve um erro ao processar sua solicitação."})
        else:
            prompt = (
                f"{ROLE_MESSAGE}\n\n"
                f"Mensagem recebida do usuário: {user_message}\n"
                "Responda de forma espontânea, como o analista poderia informar ao cliente."
            )
            try:
                response = chat.send_message(prompt)
                return jsonify({'response': response.text})
            except Exception as e:
                print(f"Erro ao chamar a API do Google: {e}")
                return jsonify({'response': "Desculpe, houve um erro ao processar sua solicitação."})

def match_process(user_message):
    for category, processes in PROCESSES.items():
        for process_name, process_desc in processes.items():
            if process_name.lower() in user_message:
                return process_desc
    return None

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
