from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
 
# Configuração da API do Google
genai.configure(api_key="AIzaSyDmU6bvVI5N-dx1vu5AKvRl5bW_mLMKRKY")
 
# Configuração do modelo
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])
 
# Criando o app Flask
app = Flask(__name__)
CORS(app)
 
# Processos
PROCESSES = {
 
     #PROCESSOS DA UX
 
     "UX": {
       
        #SAQUE
 
        "desbloquear saque": """Para desbloquear um BackOffice, acessar informações bancarias e clicar em resetar saques. após isso o usuario irá conseguir solicitar o saque normalmentem
        Um saque pode ser bloqueado após diversas falhas no saque, onde o sistema identifica algo suspeito e bloqueia Isso pode ser causado por informações bancárias incorretas no cadastro
        da plataforma, o que impede a transação. """,
 
        "saque cancelado": """Isso pode ser causado por informações bancárias incorretas no cadastro da plataforma, o que impede a transação.""",
 
        "saque bloqueado": """Solicite um print do erro e verifique os dados bancários do cliente em backoffice -> informações bancarias, após verificar caso necessario
        solicite para o cliente corrigir as informações bancarias, para editar basta ir nos três pontinhos ou no ícone de seu perfil na aba depósito, e "Meu peril"
        > "Em Pix e pagamentos" para adicionar ou editar bancos cadastrados, caso as informações do usuario esteja correta, resete saques recusados em BackOffice  >
        Transações > Resetar Saques Recusados e verifique se o saque será concluido. Um saque pode ser bloqueado após diversas falhas no saque, onde o sistema identifica
         algo suspeito e bloqueia Isso pode ser causado por informações bancárias incorretas no cadastro da plataforma, o que impede a transação. caso necessario consulte um N2""",
 
        "Saque": """Solicite um print do erro e verifique os dados bancários do cliente em backoffice -> informações bancarias, após verificar caso necessario
        solicite para o cliente corrigir as informações bancarias, para editar basta ir nos três pontinhos ou no ícone de seu perfil na aba depósito, e "Meu peril"
        > "Em Pix e pagamentos" para adicionar ou editar bancos cadastrados, caso as informações do usuario esteja correta, resete saques recusados em BackOffice  >
        Transações > Resetar Saques Recusados e verifique se o saque será concluido. Um saque pode ser bloqueado após diversas falhas no saque, onde o sistema identifica
         algo suspeito e bloqueia Isso pode ser causado por informações bancárias incorretas no cadastro da plataforma, o que impede a transação. caso necessario consulte um N2""",
 
        "Sacar": """Solicite um print do erro e verifique os dados bancários do cliente em backoffice -> informações bancarias, após verificar caso necessario
        solicite para o cliente corrigir as informações bancarias, para editar basta ir nos três pontinhos ou no ícone de seu perfil na aba depósito, e "Meu peril"
        > "Em Pix e pagamentos" para adicionar ou editar bancos cadastrados, caso as informações do usuario esteja correta, resete saques recusados em BackOffice  >
        Transações > Resetar Saques Recusados e verifique se o saque será concluido. Um saque pode ser bloqueado após diversas falhas no saque, onde o sistema identifica
         algo suspeito e bloqueia Isso pode ser causado por informações bancárias incorretas no cadastro da plataforma, o que impede a transação. caso necessario consulte um N2""",
 
        #DEPOSITO
        "Delay de deposito": """Verifique no BackOffice se o depósito foi processado corretamente. Caso não tenha sido identificado, peça ao cliente um comprovante de pagamento para validar
        a transação. Oriente o cliente a conferir se o valor foi debitado da conta e se os dados utilizados no depósito estão corretos. Alguns métodos podem levar mais tempo para compensação,
        dependendo do banco ou meio de pagamento.Se necessário, encaminhe o caso para análise com o comprovante para o N2""",
 
 
        "depositar":"""solicite um print do erro que consta quando o usuario tenta realizar um deposito, ou se o valor não estiver sendo enviado para a plataforma solicite
        o comprovante de deposito para verificar o que está ocorrendo.""",
 
 
        "Deposito": """Solicite o comprovante bancário completo, é necessário que o mesmo tenha. Remetente, destinatário, data, horário, valor e ID de transação
        e confirme as informações no BackOffice ou intermediadora. caso não seja concluido contate um N2""",
 
        #BONUS
 
        "freebet": """freebet é um tipo de bonus oferecido para os usuarios utilizar o valor determinado valor em uma aposta""",
 
        "Bonus": """pergunte de qual bonus o cliente está se referindo. caso seja algum bonus do instagram solicite um print da mensagem que enviamos a ele via instagram,
        na mensagem irá estar informando o prazo para o bonus ser creditado, caso o prazo esteja expirado contate o N2. Caso o cliente esteja se referindo a outro bonus,
        informe que no momento não temos bonus disponiveis e solicite que ele acompanhe nosso instagram ux.bet""",
 
        #APOSTA
 
        "aposta anulada": """Verifique primeiro o motivo da aposta ser anulada, após descobrir o motivo informe o usuario""",
 
        "aposta esportiva": """solicite um print do blihete de aposta do cliente, caso a partida tenha se encerrado e a aposta ainda está com o status em aberto informe um N2,
        caso seja outro caso, realize a analise normalmente e auxilie o usuario.""",
 
        "Aposta": """Primeiro solicite ao cliente informar o que ocorreu, após isso peça um print do histórico de apostas dentro do jogo com a aposta em questão, após verificar
        qual é a aposta, verifique no BackOffice o que ocorreu com a aposta e se de fato ocorreu um erro, caso tenha ocorrido um erro, junte prints que mostram o erro, informe o
        que ocorreu e envie o caso para a fila de N2""",
 
        "Apostou":"""Primeiro solicite ao cliente informar o que ocorreu, após isso peça um print do histórico de apostas dentro do jogo com a aposta em questão, após verificar
        qual é a aposta, verifique no BackOffice o que ocorreu com a aposta e se de fato ocorreu um erro, caso tenha ocorrido um erro, junte prints que mostram o erro, informe o
        que ocorreu e envie o caso para a fila de N2""",
 
        #ACESSAR CONTA
 
        "login": """Peça um print do que ocorre quando o cliente tenta acessar a conta e verifique se o usuario está digitando seu e-mail corretamente, caso o e-mail esteja correto
        e ainda não consiga acessar a conta solicite a redefinição de senha""",
 
        "acessar": """Peça um print do que ocorre quando o cliente tenta acessar a conta e verifique se o usuario está digitando seu e-mail corretamente, caso o e-mail esteja correto
        e ainda não consiga acessar a conta solicite a redefinição de senha""",
 
        "conta": """Peça um print do que ocorre quando o cliente tenta acessar a conta e verifique se o usuario está digitando seu e-mail corretamente, caso o e-mail esteja correto
        e ainda não consiga acessar a conta solicite a redefinição de senha""",
 
        #REGULAMENTAÇÃO
 
        "validação": """caso o usuario não esteja conseguindo realizar a validação, consulte o CPF do usuario na base da legitimuz e verifique o que está ocorrendo com a validação.
        caso necessario consulte um N2""",
 
        "Regulamentação": """caso o usuario não esteja conseguindo realizar a validação, consulte o CPF do usuario na base da legitimuz e verifique o que está ocorrendo com a validação.
        caso necessario consulte um N2""",
    },
 
     #PROCESSOS REALS
 
     "Reals": {
 
        #SAQUE
 
        "saque cancelado": """Isso pode ser causado por informações bancárias incorretas no cadastro da plataforma, o que impede a transação.""",
 
        "Sacar": """Confirme os dados bancários e oriente o cliente a usar o mesmo banco da chave Pix(CPF) registrada.""",
 
        "Saque": """Confirme os dados bancários e oriente o cliente cadastrar uma conta com mesmo banco da chave Pix(CPF) registrada. após o cliente cadastrar o banco
        corretamente, acompanhe o saque para ver se será concluido.""",
 
        #DEPOSITO
 
        "Delay de deposito": """Verifique no BackOffice se o depósito foi processado corretamente. Caso não tenha sido identificado, peça ao cliente um comprovante de pagamento para validar
        a transação. Oriente o cliente a conferir se o valor foi debitado da conta e se os dados utilizados no depósito estão corretos. Alguns métodos podem levar mais tempo para compensação,
        dependendo do banco ou meio de pagamento.Se necessário, encaminhe o caso para análise com o comprovante para o N2""",
 
        "depositar":"""solicite um print do erro que consta quando o usuario tenta realizar um deposito, ou se o valor não estiver sendo enviado para a plataforma solicite
        o comprovante de deposito para verificar o que está ocorrendo.""",
 
        "Deposito": """Solicite o comprovante bancário completo, é necessário que o mesmo tenha. Remetente, destinatário, data, horário, valor e ID de transação.
        e confirme as informações no BackOffice ou intermediadora. caso não seja concluido contate um N2""",
 
        #BONUS
 
        "freebet": """freebet é um tipo de bonus oferecido para os usuarios utilizar o valor determinado valor em uma aposta""",
 
        "Bonus": """Pergunte ao cliente de qual bonus está se referindo, caso ele informe um bonus que esta em ativa no momento faça a analise normalmente, caso o
        bonus não esteja ativo ou expirado informe ao cliente e solicite que ele nos acompanhe no nstagram""",
 
        #LOGIN OU SENHA
 
        "login": """Peça um print do que ocorre quando o cliente tenta acessar a conta e verifique se o usuario está digitando seu e-mail/cpf/user corretamente, caso
        a informação esteja correta e ainda não consiga acessar a conta, solicite a redefinição de senha""",
       
        "acessar": """Peça um print do que ocorre quando o cliente tenta acessar a conta e verifique se o usuario está digitando seu e-mail/cpf/user corretamente, caso a informação esteja correta e ainda
        não consiga acessar a conta, solicite a redefinição de senha""",
 
        "conta": """Peça um print do que ocorre quando o cliente tenta acessar a conta e verifique se o usuario está digitando seu e-mail/cpf/user corretamente, caso a informação esteja correta e ainda
        não consiga acessar a conta, solicite a redefinição de senha""",
 
        #APOSTA
 
        "aposta esportiva": "solicite um print do blihete de aposta do cliente, caso a partida tenha se encerrado e o jogo ainda está em aberto informe um N2., caso seja outro caso, realize a analise normalmente e auxilie o usuario.",
   
        "Aposta": """Primeiro solicite ao cliente informar o que ocorreu, após isso peça um print do histórico de apostas dentro do jogo com a aposta em questão, após
        verificar qual é a aposta, verifique no BackOffice o que ocorreu com a aposta e se de fato ocorreu um erro, caso tenha ocorrido um erro, junte prints que mostram o erro,
        informe o que ocorreu e envie o caso para a fila de N2""",
 
        #REGULAMENTAÇÃO
 
        "validação": "caso o usuario não esteja conseguindo realizar a validção, consulte o CPF do usuario na base da legitimuz e verifique o que está ocorrendo com a validação e faça analise, caso necessario consulte o N2.",
 
        "Regulamentação": "caso o usuario não esteja conseguindo realizar a validação, consulte o CPF do usuario na base da legitimuz e verifique o que está ocorrendo com a validação. caso necessario consulte um N2",
    }
}
 
# Instrução do papel da IA
ROLE_MESSAGE = (
    """
    Já estamos em contato com o cliente, não solicite para entrar em contati com o cliente, apenas informe para avisar ou pedir ao cliete.
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
user_area = None
last_matched_process = None
repeated_message_count = 0
 
@app.route('/')
def home():
    return render_template('index.html')
 
# Rota principal para o chat
@app.route('/chat', methods=['POST'])
def chat_with_bot():
    global user_area, last_matched_process, repeated_message_count
 
    user_message = request.json.get('message', "").strip().lower()
    if not user_message:
        return jsonify({'response': 'Erro: Nenhuma mensagem recebida.'})
 
    # Verificar repetição de mensagens
    if user_message in ["ux", "reals"]:
        repeated_message_count += 1
        if repeated_message_count > 2:
            return jsonify({'response': f"Já entendi que você atende {user_message.upper()}!"})
    else:
        repeated_message_count = 0
 
    # Mudar a área do usuário
    if "mudar para reals" in user_message:
        user_area = "Reals"
        return jsonify({'response': "Ok, você atende Reals! Agora vou responder com os processos de Reals."})
    elif "mudar para ux" in user_message:
        user_area = "UX"
        return jsonify({'response': "Ok, você atende UX! Agora vou responder sobre processos de UX."})
    elif not user_area:
        if "ux" in user_message:
            user_area = "UX"
            return jsonify({'response': "Ok, você atende UX! Vou responder sobre processos UX."})
        elif "reals" in user_message:
            user_area = "Reals"
            return jsonify({'response': "Ok, você atende Reals! Vou responder sobre processos Reals."})
        else:
            return jsonify({'response': "Desculpe, não entendi. Você atende UX ou Reals? Por favor, informe."})
 
    # Verificar se o usuário pediu para repetir ou explicar novamente
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
            # Se não há processo anterior, responder espontaneamente com a IA
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
 
    # Procurar processo relacionado
    matched_process = match_process(user_message)
    if matched_process:
        last_matched_process = matched_process  # Salva o último processo encontrado
        prompt = (
            f"{ROLE_MESSAGE}\n\n"
            f"O processo é o seguinte: {matched_process}\n"
            "Explique de forma clara e detalhada como o analista deve proceder, usando linguagem acessível e didática."
        )
        try:
            response = chat.send_message(prompt)
            return jsonify({'response': response.text})
        except Exception as e:
            print(f"Erro ao chamar a API do Google: {e}")
            return jsonify({'response': "Desculpe, houve um erro ao processar sua solicitação."})
 
    # Se nenhum processo for encontrado, responder espontaneamente com a IA
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
 
# Função para verificar processos com base na mensagem do usuário
def match_process(user_message):
    global user_area
    if not user_area:
        return None
 
    process_dict = PROCESSES.get(user_area, {})
    for process, details in process_dict.items():
        if process.lower() in user_message:
            return details
    return None
 
# Inicializa o servidor Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
