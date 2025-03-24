from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
from flask_cors import CORS
import google.generativeai as genai

# Configuração da API do Google
genai.configure(api_key="")

# Configuração do modelo
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

# Criando o app Flask
app = Flask(__name__)
app.secret_key = "a159a293d850aba32a1877383fd1a6b813fc74d9f8bf8173cbc98685c6b71edf"  # Necessário para gerenciar sessões
CORS(app)

# Usuários cadastrados (simulação)
USERS = {
    "webchat": "analistas65834983847534"
}

# Processos
def load_processes():
    with open('processos.json', 'r', encoding='utf-8') as file:
        return json.load(file)

# Carregar os processos ao iniciar o app
PROCESSES = load_processes()

# Instrução do papel da IA
ROLE_MESSAGE = (
    """
    Já estamos em contato com o cliente, não solicite para entrar em contato com o cliente, apenas informe para avisar ou pedir ao cliente.
    Eu ajudo a responder clientes. Quando o cliente faz uma pergunta, eu forneço respostas claras e objetivas com base no que ele precisa informar.
    Caso um processo específico não seja encontrado, responda de forma espontânea, como o analista poderia dizer ou informar, com base na mensagem recebida e informe para consultar com um N2.
    Caso um usuário informe que não entendeu ou solicitar para explicar de novo o processo passado, explique novamente.
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

@app.route('/')
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        
        if email in USERS and USERS[email] == password:
            session["user"] = email
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Credenciais inválidas")
    
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

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
    if "user" not in session:
        return jsonify({'response': 'Erro: Você precisa estar logado para usar o chatbot.'})
    
    user_message = request.json.get('message', "").strip().lower()
    if not user_message:
        return jsonify({'response': 'Erro: Nenhuma mensagem recebida.'})
    
    response = chat.send_message(user_message)
    return jsonify({'response': response.text})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
