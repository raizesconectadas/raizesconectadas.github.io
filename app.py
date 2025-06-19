# app.py - O Cérebro do Nosso Projeto "Raízes Conectadas"!
# Enzo Aqui é onde a mágica acontece, sabe? A gente conecta o site, o banco e a galera!

# --- Importações Essenciais (Sem isso, nada funciona!) ---
from flask import Flask, render_template, request, redirect, url_for, flash # O Flask em si, e umas ferramentas úteis
from flask_wtf import FlaskForm # Pra fazer formulários de um jeito seguro e fácil
from wtforms import StringField, EmailField, TelField, TextAreaField, SubmitField # Os tipos de campos dos nossos formulários
from wtforms.validators import DataRequired, Length, Email # Regrinhas pra validar o que o povo digita
from flask_wtf.csrf import CSRFProtect # Proteção contra uns ataques chatinhos de formulário

# Ferramentas do Banco de Dados (Pra guardar tudo bonitinho!)
from flask_sqlalchemy import SQLAlchemy # O ORM que ajuda a conversar com o banco sem muito SQL
from flask_migrate import Migrate # Pra gente conseguir mudar o banco de dados sem bagunçar tudo depois
# import os # Não vamos usar 'os' aqui por enquanto, mas é bom saber que existe!

# --- Configurações Iniciais do Aplicativo (O "DNA" do nosso SITE) ---

app = Flask(__name__) # 

# EM PRODUÇÃO: Troca essa aqui por uma gerada de forma super aleatória e guarda num lugar seguro )!
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'RAIZES_SECRETA_MUITO_ALEATORIA_E_LONGA_ABC123XYZ987KJH654FDGHJ7890PLMNBG54RFVBNGTFRD')
csrf = CSRFProtect(app) # Ativando a proteção de formulários com essa chave secreta.

# --- Configuração do Banco de Dados PostgreSQL ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://raizes_user:1997xf11ASDF@localhost:5432/raizes_conectadas_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Isso aqui é pra não gastar memória à toa.

db = SQLAlchemy(app) # Conecta o nosso aplicativo com o Banco de Dados.
migrate = Migrate(app, db) # Prepara o Flask para futuras atualizações no banco

# --- Modelos do Banco de Dados (As "plantas" das nossas tabelas) ---
# Cada classe aqui é como um tipo de "ficha cadastral" que a gente guarda no banco.

class Escola(db.Model):
    __tablename__ = 'escolas' 
    id = db.Column(db.Integer, primary_key=True) # Um número único pra cada escola (o RG dela no sistema)
    nome_escola = db.Column(db.String(100), nullable=False) 
    cnpj = db.Column(db.String(18), unique=True, nullable=False) 
    endereco = db.Column(db.String(200), nullable=False) 
    responsavel = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False) # E-mail de contato, tem que ser único e válido
    telefone = db.Column(db.String(15)) # Telefone de contato (com DDD, né?,R sim Enzo)
    mensagem = db.Column(db.Text) 

    def __repr__(self):
        return f'<Escola: {self.nome_escola}>'

class Agricultor(db.Model):
    __tablename__ = 'agricultores'
    id = db.Column(db.Integer, primary_key=True) # ID único do agricultor
    nome_propriedade = db.Column(db.String(100), nullable=False) # O nome do sítio, fazenda, chácara... obrigatório!
    cpf_cnpj = db.Column(db.String(18), unique=True, nullable=False) 
    endereco = db.Column(db.String(200), nullable=False) 
    responsavel = db.Column(db.String(100), nullable=False) 
    email = db.Column(db.String(120), unique=True, nullable=False) 
    telefone = db.Column(db.String(15)) 
    produtos = db.Column(db.Text, nullable=False) 
    certificacao = db.Column(db.String(100)) # Se ele tem alguma certificação (orgânico, etc., não esquece de criar as abas de exemplo)
    mensagem = db.Column(db.Text) 

    def __repr__(self):
        # Pra identificar um agricultor quando o código mostrar ele.OBS: Estava dando erro enzo, se ja ajeitou beleza
        return f'<Agricultor: {self.nome_propriedade}>'

# --- Definição dos Formulários (Flask-WTF) (As "fichas" que o usuário preenche) ---
# Usamos o Flask-WTF pra garantir que o formulário é seguro e validado / Ta bom, não esquece de testa em ação.

class CadastroEscolaForm(FlaskForm):
    # Campos para o formulário de cadastro de escolas
    nome_escola = StringField('Nome da Escola', validators=[DataRequired('O nome da escola é essencial!'), Length(max=100, message='Nome da escola muito longo.')])
    cnpj = StringField('CNPJ', validators=[DataRequired('Precisamos do CNPJ da escola.'), Length(min=14, max=18, message='CNPJ inválido (min 14, max 18 caracteres).')])
    endereco = StringField('Endereço Completo', validators=[DataRequired('O endereço é fundamental para nos localizarmos!'), Length(max=200, message='Endereço muito longo.')])
    responsavel = StringField('Nome do Responsável', validators=[DataRequired('Por favor, informe o nome do responsável.'), Length(max=100, message='Nome do responsável muito longo.')])
    email = EmailField('Email de Contato', validators=[DataRequired('Um e-mail é crucial para entrarmos em contato!'), Email('Por favor, digite um e-mail válido.'), Length(max=120, message='E-mail muito longo.')])
    telefone = TelField('Telefone (DDD+Número)', validators=[DataRequired('Um telefone para contato é importante!'), Length(min=10, max=15, message='Telefone inválido (min 10, max 15 caracteres).')])
    mensagem = TextAreaField('Algo mais que queira dizer? (Opcional)') # Mensagem adicional, não obrigatória
    submit = SubmitField('Cadastrar Escola') # O botão que envia tudo! / Tu não esquece de tirar essas observações, pra depois não ficarem pensando besteira. deixa so o importante

class CadastroAgricultorForm(FlaskForm):
    # Campos para o formulário de cadastro de agricultores
    nome_propriedade = StringField('Nome da Propriedade / Sítio', validators=[DataRequired('Qual o nome da sua propriedade? É importante!'), Length(max=100, message='Nome da propriedade muito longo.')])
    cpf_cnpj = StringField('CPF ou CNPJ', validators=[DataRequired('Seu CPF ou CNPJ é obrigatório para o cadastro.'), Length(min=11, max=18, message='CPF/CNPJ inválido (min 11, max 18 caracteres).')])
    endereco = StringField('Endereço da Propriedade', validators=[DataRequired('Precisamos saber onde fica sua propriedade!'), Length(max=200, message='Endereço da propriedade muito longo.')])
    responsavel = StringField('Seu Nome (Responsável pela Produção)', validators=[DataRequired('Por favor, informe o seu nome.'), Length(max=100, message='Nome do responsável muito longo.')])
    email = EmailField('Seu Email', validators=[DataRequired('Um e-mail para contato é essencial!'), Email('Por favor, digite um e-mail válido.'), Length(max=120, message='E-mail muito longo.')])
    telefone = TelField('Seu Telefone (DDD+Número)', validators=[DataRequired('Seu telefone para contato é importante!'), Length(min=10, max=15, message='Telefone inválido (min 10, max 15 caracteres).')])
    produtos = TextAreaField('Quais produtos você oferece? (Ex: Alface, Tomate, Ovos Caipira)', validators=[DataRequired('Conte-nos sobre seus produtos, por favor!')])
    certificacao = StringField('Tem alguma certificação? (Ex: Orgânico, Agroecológico)', validators=[Length(max=100, message='Certificação muito longa.')])
    mensagem = TextAreaField('Alguma mensagem extra para a equipe Raízes Conectadas? (Opcional)') # Mensagem adicional, não obrigatória
    submit = SubmitField('Cadastrar Produção') # O botão de envio!

# --- Rotas do Aplicativo (Os "caminhos" do nosso site) ---
# Cada função aqui é uma "parada" que o usuário pode fazer no site./Enzo kkkk, os icones, vai deixa?

@app.route('/') # A nossa porta de entrada!
def index():
    print("✨ Alguém acabou de chegar na página inicial! Seja bem-vindo(a)! ✨")
    return render_template('index.html') # Carrega a página principal.

@app.route('/escolas.html') # Caminho para a página das escolas
def escolas_page():
    print("🏫 Ops! Parece que uma escola está querendo se cadastrar. Mostrando o formulário...")
    form_escola = CadastroEscolaForm() # Prepara o formulário vazio para a escola preencher.
    return render_template('escolas.html', form_escola=form_escola) 

@app.route('/agricultores.html') # Caminho para a página dos agricultores
def agricultores_page():
    print("🌱 Um agricultor visitou a página! Hora de mostrar as oportunidades de cadastro.")
    form_agricultor = CadastroAgricultorForm() # Prepara o formulário vazio para o agricultor.
    return render_template('agricultores.html', form_agricultor=form_agricultor) 

# --- Rotas de Cadastro (É AQUI QUE A GENTE SALVA OS DADOS NO BANCO!) // Enzo muito provavel não vai da tempo e vamos ter que criar no googlesite, entao arrisca esse mesmo---

@app.route('/cadastro_escola', methods=['POST']) # Quando o formulário da escola é ENVIADO (método POST)
def processa_cadastro_escola(): # Renomeei a função para evitar conflito com a rota GET / Não esquce
    print("✉️ Recebi um formulário de cadastro de escola! Vamos ver se está tudo certo...")
    form_escola = CadastroEscolaForm() 
    if form_escola.validate_on_submit(): 
        print("✅ Formulário da escola validado com sucesso! Agora é com o banco de dados...")
        try:
            nova_escola = Escola( 
                nome_escola=form_escola.nome_escola.data,
                cnpj=form_escola.cnpj.data,
                endereco=form_escola.endereco.data,
                responsavel=form_escola.responsavel.data,
                email=form_escola.email.data,
                telefone=form_escola.telefone.data,
                mensagem=form_escola.mensagem.data
            )
            db.session.add(nova_escola) 
            db.session.commit() 

            print(f"🎉 Escola '{nova_escola.nome_escola}' cadastrada com sucesso no DB! CNPJ: {nova_escola.cnpj}")
            flash('Sua escola foi cadastrada com sucesso! Em breve entraremos em contato.', 'success') # Mensagem de sucesso para o usuário
            return redirect(url_for('cadastro_sucesso')) 

        except Exception as e:
            # algo deu errado na hora de salvar no banco!, // Enzo eu não criei a VPN ainda para leva ao banco. tera que fica local, meu pc ta cheio
            db.session.rollback() # Desfaz qualquer coisa que tenha sido feita no banco (pra não dar bagunça)
            print(f"❌ ERRO ao salvar a escola no banco de dados: {e}")
            flash(f'Puxa! Não conseguimos cadastrar sua escola agora. Tente novamente mais tarde, por favor. Erro: {e}', 'error') 
            return render_template('escolas.html', form_escola=form_escola) 

    else: # Se o formulário não passou na validação (algum campo faltando, e-mail errado, etc.)
        print("⚠️ Formulário da escola com erros. Mostrando a página de novo com as correções necessárias.")
        # O Flask-WTF já vai se virar pra mostrar os erros ao lado dos campos.
        return render_template('escolas.html', form_escola=form_escola)

@app.route('/cadastro_agricultor', methods=['POST']) # Quando o formulário do agricultor é ENVIADO
def processa_cadastro_agricultor(): # Renomeei a função também!
    print("✉️ Recebi um formulário de cadastro de agricultor! Vamos conferir...")
    form_agricultor = CadastroAgricultorForm() # Pega os dados do formulário.
    if form_agricultor.validate_on_submit(): # Valida!
        print("✅ Formulário do agricultor validado! Preparando para salvar no banco...")
        try:
            novo_agricultor = Agricultor( # Cria um novo registro de agricultor
                nome_propriedade=form_agricultor.nome_propriedade.data,
                cpf_cnpj=form_agricultor.cpf_cnpj.data,
                endereco=form_agricultor.endereco.data,
                responsavel=form_agricultor.responsavel.data,
                email=form_agricultor.email.data,
                telefone=form_agricultor.telefone.data,
                produtos=form_agricultor.produtos.data,
                certificacao=form_agricultor.certificacao.data,
                mensagem=form_agricultor.mensagem.data
            )
            db.session.add(novo_agricultor) # Adiciona à fila de salvamento
            db.session.commit() # Salva de verdade no banco

            print(f"🎉 Agricultor '{novo_agricultor.nome_propriedade}' cadastrado com sucesso no DB! Produtos: {novo_agricultor.produtos}")
            flash('Sua produção foi cadastrada com sucesso! Em breve entraremos em contato.', 'success') # Mensagem de sucesso
            return redirect(url_for('cadastro_sucesso')) # Redireciona para o agradecimento!

        except Exception as e:
            db.session.rollback() # Desfaz se deu erro!
            print(f"❌ ERRO ao salvar o agricultor no banco de dados: {e}")
            flash(f'Puxa! Não conseguimos cadastrar sua produção agora. Tente novamente mais tarde, por favor. Erro: {e}', 'error') # Mensagem de erro
            return render_template('agricultores.html', form_agricultor=form_agricultor)

    else: # Se o formulário do agricultor tiver erros
        print("⚠️ Formulário do agricultor com erros. Mostrando a página de novo com as correções necessárias.")
        return render_template('agricultores.html', form_agricultor=form_agricultor)

@app.route('/cadastro_sucesso') 
def cadastro_sucesso():
    print("💖 Redirecionado para a página de sucesso/agradecimento. Missão cumprida!")
    return render_template('agradecimento.html') 

# --- Roda o Aplicativo (O "start" do nosso projeto!) ---
if __name__ == '__main__': 
    # Lembrete pro futuro: Com Flask-Migrate, a gente não usa mais db.create_all() aqui.
    # O banco é criado e atualizado com os comandos 'flask db migrate' e 'flask db upgrade' no terminal.
    # Isso é algo que a gente vai colocar depois de um tempo! ;)
    app.run(debug=True) 
                       
                        # Enzo NUNCA use debug=True em produção, ok? É perigoso!
