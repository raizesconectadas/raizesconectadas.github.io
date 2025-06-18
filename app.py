from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TelField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email # Importa o que precisa para validar os campos
from flask_wtf.csrf import CSRFProtect

# Importações para o banco de dados
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# import os # Não vamos usar isso por enquanto, então deixei comentado

# --- Configurações do Aplicativo Flask (As coisas básicas que o app precisa) ---

app = Flask(__name__) # Cria a aplicação Flask
app.config['SECRET_KEY'] = 'uma_chave_secreta_bem_longa_e_complicada_mas_nao_importa_muito_agora' # Chave para segurança, importante pra Formulários
csrf = CSRFProtect(app) # Ativa a proteção contra ataques de formulário

# --- Configuração do Banco de Dados (Onde os dados vão ser guardados) ---
# Usando PostgreSQL, porque é o que o professor mostrou na aula.
# Coloca aqui os dados do seu banco de verdade!
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://usuario_db:sua_senha@localhost:5432/nome_do_seu_banco'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Isso é pra não gastar muita memória, disseram que é bom deixar False

db = SQLAlchemy(app) # Conecta o Flask com o banco de dados
migrate = Migrate(app, db) # Ajuda a mudar o banco de dados depois, se precisar

# --- Modelos do Banco de Dados (Como as tabelas do banco vão ser) ---
# Cada classe é uma tabela no banco.

class Escola(db.Model):
    __tablename__ = 'escolas' # Nome da tabela no banco
    id = db.Column(db.Integer, primary_key=True) # ID da escola, é o principal
    nome_escola = db.Column(db.String(100), nullable=False) # Nome da escola, obrigatório
    cnpj = db.Column(db.String(18), unique=True, nullable=False) # CNPJ, tem que ser único e obrigatório
    endereco = db.Column(db.String(200), nullable=False) # Endereço, obrigatório
    responsavel = db.Column(db.String(100), nullable=False) # Nome de quem responde pela escola
    email = db.Column(db.String(120), unique=True, nullable=False) # E-mail, único e obrigatório
    telefone = db.Column(db.String(15)) # Telefone da escola
    mensagem = db.Column(db.Text) # Um campo para uma mensagem maior

    def __repr__(self):
        # Isso é só pra quando a gente imprimir um objeto Escola, ver o nome dela
        return f'<Escola: {self.nome_escola}>'

class Agricultor(db.Model):
    __tablename__ = 'agricultores' # Nome da tabela
    id = db.Column(db.Integer, primary_key=True)
    nome_propriedade = db.Column(db.String(100), nullable=False) # Nome da fazenda ou sítio
    cpf_cnpj = db.Column(db.String(18), unique=True, nullable=False) # Pode ser CPF ou CNPJ, único
    endereco = db.Column(db.String(200), nullable=False)
    responsavel = db.Column(db.String(100), nullable=False) # Nome do agricultor responsável
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone = db.Column(db.String(15))
    produtos = db.Column(db.Text, nullable=False) # Quais produtos o agricultor vende
    certificacao = db.Column(db.String(100)) # Se tem alguma certificação
    mensagem = db.Column(db.Text) # Mensagem extra

    def __repr__(self):
        # Pra imprimir o nome da propriedade
        return f'<Agricultor: {self.nome_propriedade}>'

# --- Formulários (Como os dados vão ser digitados no site) ---
# Cada classe aqui é um formulário que o usuário vai preencher.

class CadastroEscolaForm(FlaskForm):
    nome_escola = StringField('Nome da Escola', validators=[DataRequired(), Length(max=100)])
    cnpj = StringField('CNPJ', validators=[DataRequired(), Length(min=14, max=18)]) # CNPJ geralmente tem 14 ou 18 (com pontos)
    endereco = StringField('Endereço Completo', validators=[DataRequired(), Length(max=200)])
    responsavel = StringField('Nome do Responsável', validators=[DataRequired(), Length(max=100)])
    email = EmailField('Email de Contato', validators=[DataRequired(), Email(), Length(max=120)])
    telefone = TelField('Telefone (DDD+Número)', validators=[DataRequired(), Length(min=10, max=15)])
    mensagem = TextAreaField('Algo mais que queira dizer?')
    submit = SubmitField('Cadastrar Escola') # Botão pra enviar

class CadastroAgricultorForm(FlaskForm):
    nome_propriedade = StringField('Nome da Propriedade / Sítio', validators=[DataRequired(), Length(max=100)])
    cpf_cnpj = StringField('CPF ou CNPJ', validators=[DataRequired(), Length(min=11, max=18)]) # Pra CPF (11) ou CNPJ (14/18)
    endereco = StringField('Endereço da Propriedade', validators=[DataRequired(), Length(max=200)])
    responsavel = StringField('Seu Nome (Responsável)', validators=[DataRequired(), Length(max=100)])
    email = EmailField('Seu Email', validators=[DataRequired(), Email(), Length(max=120)])
    telefone = TelField('Seu Telefone (DDD+Número)', validators=[DataRequired(), Length(min=10, max=15)])
    produtos = TextAreaField('Quais produtos você oferece? (Ex: Alface, Tomate, Ovos)', validators=[DataRequired()])
    certificacao = StringField('Tem alguma certificação? (Ex: Orgânico)', validators=[Length(max=100)])
    mensagem = TextAreaField('Alguma mensagem extra?')
    submit = SubmitField('Cadastrar Produção') # Botão de envio

# --- Rotas do Aplicativo (As "páginas" do site) ---
# Cada @app.route define uma página ou uma ação no site.

@app.route('/') # Quando a pessoa acessa o endereço principal do site (ex: localhost:5000)
def index():
    print("Acessaram a página inicial!") # Um print pra saber que chegou aqui
    return render_template('index.html') # Mostra o arquivo index.html

@app.route('/escolas.html') # A página para cadastrar escolas
def escolas_page():
    print("Acessaram a página de escolas.")
    form_escola = CadastroEscolaForm() # Cria um formulário de escola
    return render_template('escolas.html', form_escola=form_escola) # Mostra a página de escolas com o formulário

@app.route('/agricultores.html') # A página para cadastrar agricultores
def agricultores_page():
    print("Acessaram a página de agricultores.")
    form_agricultor = CadastroAgricultorForm() # Cria um formulário de agricultor
    return render_template('agricultores.html', form_agricultor=form_agricultor) # Mostra a página de agricultores

@app.route('/cadastro_escola', methods=['POST']) # Quando o formulário de escola é enviado (método POST)
def cadastro_escola():
    form_escola = CadastroEscolaForm() # Pega os dados que vieram do formulário
    if form_escola.validate_on_submit(): # Se o formulário foi preenchido certo (sem erros de validação)
        print("Formulário de escola válido! Tentando salvar no banco...")
        nova_escola = Escola( # Cria um novo objeto Escola com os dados do formulário
            nome_escola=form_escola.nome_escola.data,
            cnpj=form_escola.cnpj.data,
            endereco=form_escola.endereco.data,
            responsavel=form_escola.responsavel.data,
            email=form_escola.email.data,
            telefone=form_escola.telefone.data,
            mensagem=form_escola.mensagem.data
        )
        db.session.add(nova_escola) # Adiciona a nova escola para ser salva
        db.session.commit() # Salva de verdade no banco de dados

        print(f"Escola cadastrada com sucesso! Nome: {nova_escola.nome_escola}") # Um print de confirmação
        return redirect(url_for('cadastro_sucesso')) # Redireciona para uma página de sucesso
    else:
        print("Erro no formulário da escola. Mostrando a página de novo com os erros.")
        # Se deu algum erro no formulário, mostra a página de novo e o Flask-WTF já exibe os erros
        return render_template('escolas.html', form_escola=form_escola)

@app.route('/cadastro_agricultor', methods=['POST']) # Quando o formulário de agricultor é enviado
def cadastro_agricultor():
    form_agricultor = CadastroAgricultorForm() # Pega os dados do formulário
    if form_agricultor.validate_on_submit(): # Se o formulário está ok
        print("Formulário de agricultor válido! Salvando no banco...")
        novo_agricultor = Agricultor( # Cria um novo objeto Agricultor
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
        db.session.add(novo_agricultor) # Adiciona o agricultor
        db.session.commit() # Salva no banco

        print(f"Agricultor cadastrado com sucesso! Propriedade: {novo_agricultor.nome_propriedade}")
        return redirect(url_for('cadastro_sucesso')) # Redireciona para o sucesso
    else:
        print("Erro no formulário do agricultor. Mostrando a página de novo com os erros.")
        return render_template('agricultores.html', form_agricultor=form_agricultor)

@app.route('/cadastro_sucesso') # Uma página simples para mostrar que o cadastro deu certo
def cadastro_sucesso():
    print("Redirecionado para a página de sucesso.")
    return render_template('cadastro_sucesso.html')

if __name__ == '__main__': # Isso aqui faz o aplicativo rodar quando você executa o arquivo
    # Não usamos mais db.create_all() aqui porque o 'flask db migrate' e 'flask db upgrade' cuidam disso.
    # Isso é algo que a gente aprende depois de um tempo.
    app.run(debug=True) # Inicia o servidor Flask. 'debug=True' é bom pra ver os erros enquanto desenvolve.
