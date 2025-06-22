# app.py - Meu primeiro site com Flask! (Que legal!)

# Importando o Flask. O professor disse que é tipo a ferramenta principal.
from flask import Flask, render_template, request, flash

# O professor falou que isso é pra configurar o aplicativo.
app = Flask(__name__)

# A chave secreta é importante pra segurança, mas pra agora, uma simples serve.
# Em projetos de verdade, é mais complicado, mas aqui é só pra aprender.
app.config['SECRET_KEY'] = 'minha_chave_super_secreta_pra_aula'

# -- As Páginas do Meu Site --

# Página Inicial (o index.html)
# Quando alguém vai pro endereço principal, mostra essa página.
@app.route('/')
def index():
    # Removido: print("Alguém visitou a página inicial!")
    return render_template('index.html')

# Página dos Agricultores (o agricultores.html)
# Aqui a gente fala pros agricultores o que o site faz por eles.
@app.route('/agricultores', methods=['GET', 'POST']) # Pode ver ou enviar dados
def agricultores():
    if request.method == 'POST':
        # Quando alguém envia o formulário de agricultor...
        nome_agricultor = request.form['nome_agricultor']
        email_agricultor = request.form['email_agricultor']
        telefone_agricultor = request.form['telefone_agricultor']
        producao_agricultor = request.form['producao_agricultor']
        mensagem_agricultor = request.form.get('mensagem_agricultor', '')

        # REMOVIDO: Bloco de print para o terminal/log
        # print(f"\n--- Dados de Agricultor Recebidos ---")
        # print(f"Nome: {nome_agricultor}")
        # print(f"Email: {email_agricultor}")
        # print(f"Telefone: {telefone_agricultor}")
        # print(f"Produção: {producao_agricultor}")
        # print(f"Mensagem: {mensagem_agricultor}")
        # print(f"------------------------------------\n")

        flash('Seu cadastro de produção foi enviado! Em breve entraremos em contato.', 'sucesso')

        # Renderiza agradecimento.html e passa os dados para exibição na tela do usuário
        return render_template('agradecimento.html',
                               tipo_cadastro='Agricultor',
                               nome_usuario=nome_agricultor,
                               email_usuario=email_agricultor,
                               telefone_usuario=telefone_agricultor,
                               producao_info=producao_agricultor,
                               mensagem_usuario=mensagem_agricultor)

    # Se não for POST (se só estiver visitando a página), mostra o formulário.
    return render_template('agricultores.html')

# Página das Escolas (o escolas.html)
# Pra mostrar pras escolas como se cadastrar.
@app.route('/escolas', methods=['GET', 'POST']) # Também pode ver ou enviar
def escolas():
    if request.method == 'POST':
        # Quando alguém envia o formulário de escola...
        nome_escola = request.form['nome_escola']
        endereco_escola = request.form['endereco_escola']
        email_escola = request.form['email_escola']
        telefone_escola = request.form['telefone_escola']
        mensagem_escola = request.form.get('mensagem_escola', '')

        # REMOVIDO: Bloco de print para o terminal/log
        # print(f"\n--- Dados de Escola Recebidos ---")
        # print(f"Nome da Escola: {nome_escola}")
        # print(f"Endereço: {endereco_escola}")
        # print(f"Email: {email_escola}")
        # print(f"Telefone: {telefone_escola}")
        # print(f"Mensagem: {mensagem_escola}")
        # print(f"--------------------------------\n")

        flash('Seu cadastro de escola foi enviado! Muito obrigado!', 'sucesso')

        # Renderiza agradecimento.html e passa os dados para exibição na tela do usuário
        return render_template('agradecimento.html',
                               tipo_cadastro='Escola',
                               nome_instituicao=nome_escola,
                               endereco_instituicao=endereco_escola,
                               email_instituicao=email_escola,
                               telefone_instituicao=telefone_escola,
                               mensagem_instituicao=mensagem_escola)

    return render_template('escolas.html')

# Página de Agradecimento (agradecimento.html)
@app.route('/cadastro_sucesso')
def cadastro_sucesso():
    # Removido: print("Página de agradecimento genérica visitada.")
    # Esta rota serve como uma página de agradecimento genérica
    # caso seja acessada diretamente (não por um envio de formulário).
    return render_template('agradecimento.html')


# Página Sobre o Projeto (sobre.html)
@app.route('/sobre')
def sobre():
    # Removido: print("Página 'Sobre' visitada.")
    return render_template('sobre.html')

# Página de Contato (contato.html)
@app.route('/contato')
def contato():
    # Removido: print("Página 'Contato' visitada.")
    return render_template('contato.html')

# -- Pra fazer o aplicativo rodar --
if __name__ == '__main__':
    app.run(debug=True)