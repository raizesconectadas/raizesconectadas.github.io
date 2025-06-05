from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TelField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email
from flask_wtf.csrf import CSRFProtect

# Importações para o banco de dados
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os # Importar para usar variáveis de ambiente

app = Flask(_name_)

# --- Configurações do Aplicativo ---

app = Flask(__name__)
app.config['SECRET_KEY'] = 'A7X2B9L5Q3V8D1M6Y4T0R7J5CX7B2L9Q5V1D8M3Y4T6R0J'  # **Coloque o codigo secreto aqui!**
csrf = CSRFProtect(app)

# --- Configuração do Banco de Dados PostgreSQL ---
# credenciais postgresql
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://raizes_user:1997xf11ASDF@localhost:5432/raizes_conectadas_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Desativa o rastreamento de modificações do SQLAlchemy (consome menos memória)

db = SQLAlchemy(app) # Inicializa o SQLAlchemy
migrate = Migrate(app, db) # Inicializa o Flask-Migrate

# --- Definição dos Formulários (Flask-WTF) ---

class Escola(db.Model):
    # _tablename_ = 'escolas' # Opcional: Define explicitamente o nome da tabela no DB
    id = db.Column(db.Integer, primary_key=True)
    nome_escola = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(18), unique=True, nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    responsavel = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone = db.Column(db.String(15))
    mensagem = db.Column(db.Text) # Use Text para mensagens mais longas

    def _repr_(self):
        return f'<Escola {self.nome_escola}>'

class Agricultor(db.Model):
    # _tablename_ = 'agricultores' # Opcional: Define explicitamente o nome da tabela no DB
    id = db.Column(db.Integer, primary_key=True)
    nome_propriedade = db.Column(db.String(100), nullable=False)
    # CPF/CNPJ: unique=True garante que não haverá duplicidade. Max length 18 cobre ambos.
    cpf_cnpj = db.Column(db.String(18), unique=True, nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    responsavel = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone = db.Column(db.String(15))
    # Produtos: se for uma lista curta, String é ok. Se for uma descrição longa, Text é melhor.
    produtos = db.Column(db.Text, nullable=False)
    certificacao = db.Column(db.String(100))
    mensagem = db.Column(db.Text) # Use Text para mensagens mais longas

    def _repr_(self):
        return f'<Agricultor {self.nome_propriedade}>'


class CadastroEscolaForm(FlaskForm):
    nome_escola = StringField('Nome da Escola', validators=[DataRequired(), Length(max=100)])
    cnpj = StringField('CNPJ', validators=[DataRequired(), Length(min=14, max=18)])  # Validação básica de CNPJ
    endereco = StringField('Endereço', validators=[DataRequired(), Length(max=200)])
    responsavel = StringField('Nome do Responsável', validators=[DataRequired(), Length(max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    telefone = TelField('Telefone', validators=[DataRequired(), Length(min=10, max=15)])  # Validação básica de telefone
    mensagem = TextAreaField('Mensagem Adicional')
    submit = SubmitField('Cadastrar Escola')

class CadastroAgricultorForm(FlaskForm):
    nome_propriedade = StringField('Nome da Propriedade', validators=[DataRequired(), Length(max=100)])
    cpf_cnpj = StringField('CPF/CNPJ', validators=[DataRequired(), Length(min=11, max=18)])  # Validação básica
    endereco = StringField('Endereço', validators=[DataRequired(), Length(max=200)])
    responsavel = StringField('Nome do Responsável', validators=[DataRequired(), Length(max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    telefone = TelField('Telefone', validators=[DataRequired(), Length(min=10, max=15)])
    produtos = TextAreaField('Produtos Ofertados', validators=[DataRequired()])
    certificacao = StringField('Certificação (Opcional)', validators=[Length(max=100)])
    mensagem = TextAreaField('Mensagem Adicional')
    submit = SubmitField('Cadastrar Produção')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/escolas.html')
def escolas_page():
    form_escola = CadastroEscolaForm()
    return render_template('escolas.html', form_escola=form_escola)

@app.route('/agricultores.html')
def agricultores_page():
    form_agricultor = CadastroAgricultorForm()
    return render_template('agricultores.html', form_agricultor=form_agricultor)

# --- ROTAS DE CADASTRO (AQUI VAMOS SALVAR NO DB) ---
@app.route('/cadastro_escola', methods=['POST'])
def cadastro_escola():
    form_escola = CadastroEscolaForm()
    if form_escola.validate_on_submit():
        # Cria uma nova instância do modelo Escola com os dados do formulário
        nova_escola = Escola(
            nome_escola=form_escola.nome_escola.data,
            cnpj=form_escola.cnpj.data,
            endereco=form_escola.endereco.data,
            responsavel=form_escola.responsavel.data,
            email=form_escola.email.data,
            telefone=form_escola.telefone.data,
            mensagem=form_escola.mensagem.data
        )
        # Adiciona a nova escola à sessão do banco de dados
        db.session.add(nova_escola)
        # Confirma a transação, salvando no banco de dados
        db.session.commit()

        print(f"Dados da Escola salvos no DB: Nome={nova_escola.nome_escola}, CNPJ={nova_escola.cnpj}, Email={nova_escola.email}")
        return redirect(url_for('cadastro_sucesso'))
    else:
        # Se o formulário não for válido, renderize a página de cadastro novamente com os erros
        return render_template('escolas.html', form_escola=form_escola)

@app.route('/cadastro_agricultor', methods=['POST'])
def cadastro_agricultor():
    form_agricultor = CadastroAgricultorForm()
    if form_agricultor.validate_on_submit():
        # Cria uma nova instância do modelo Agricultor com os dados do formulário
        novo_agricultor = Agricultor(
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
        # Adiciona o novo agricultor à sessão do banco de dados
        db.session.add(novo_agricultor)
        # Confirma a transação, salvando no banco de dados
        db.session.commit()

        print(f"Dados do Agricultor salvos no DB: Propriedade={novo_agricultor.nome_propriedade}, CPF/CNPJ={novo_agricultor.cpf_cnpj}, Produtos={novo_agricultor.produtos}")
        return redirect(url_for('cadastro_sucesso'))
    else:
        return render_template('agricultores.html', form_agricultor=form_agricultor)

@app.route('/cadastro_sucesso')
def cadastro_sucesso():
    return render_template('cadastro_sucesso.html')

if _name_ == '_main_':
    # REMOVIDO: db.create_all() - Com o Flask-Migrate, não criamos mais as tabelas aqui.
    # Elas serão criadas pelos comandos de migração no terminal.
    app.run(debug=True)