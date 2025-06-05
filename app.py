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
class CadastroEscolaForm(FlaskForm):
    nome_escola = StringField('Nome da Escola', validators=[DataRequired(), Length(max=100)])
    cnpj = StringField('CNPJ', validators=[DataRequired(), Length(min=14, max=18)])
    endereco = StringField('Endereço', validators=[DataRequired(), Length(max=200)])
    responsavel = StringField('Nome do Responsável', validators=[DataRequired(), Length(max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    telefone = TelField('Telefone', validators=[DataRequired(), Length(min=10, max=15)])
    mensagem = TextAreaField('Mensagem Adicional')
    submit = SubmitField('Cadastrar Escola')

class CadastroAgricultorForm(FlaskForm):
    nome_propriedade = StringField('Nome da Propriedade', validators=[DataRequired(), Length(max=100)])
    cpf_cnpj = StringField('CPF/CNPJ', validators=[DataRequired(), Length(min=11, max=18)]) # Ajustei min para CPF
    endereco = StringField('Endereço', validators=[DataRequired(), Length(max=200)])
    responsavel = StringField('Nome do Responsável', validators=[DataRequired(), Length(max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    telefone = TelField('Telefone', validators=[DataRequired(), Length(min=10, max=15)])
    produtos = StringField('Produtos Ofertados (ex: frutas, verduras, ovos)', validators=[DataRequired(), Length(max=200)])
    certificacao = StringField('Certificações (ex: Orgânico, Agroecológico)', validators=[Length(max=100)])
    mensagem = TextAreaField('Mensagem Adicional')
    submit = SubmitField('Cadastrar Produção')


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

@app.route('/cadastro_escola', methods=['POST'])
def cadastro_escola():
    form_escola = CadastroEscolaForm()
    if form_escola.validate_on_submit():
        nome_escola = form_escola.nome_escola.data
        cnpj = form_escola.cnpj.data
        endereco = form_escola.endereco.data
        responsavel = form_escola.responsavel.data
        email = form_escola.email.data
        telefone = form_escola.telefone.data
        mensagem = form_escola.mensagem.data

        # Falta termina o processamento dos dados: salvar no banco de dados, enviar email, etc.
        print(f"Dados da Escola: Nome={nome_escola}, CNPJ={cnpj}, Email={email}")
        # Após o processamento, Falta criar a página de sucesso
        return redirect(url_for('cadastro_sucesso'))
    else:
        # Se o formulário não for válido, renderize a página de cadastro novamente com os erros
        return render_template('escolas.html', form_escola=form_escola)

@app.route('/cadastro_agricultor', methods=['POST'])
def cadastro_agricultor():
    form_agricultor = CadastroAgricultorForm()
    if form_agricultor.validate_on_submit():
        nome_propriedade = form_agricultor.nome_propriedade.data
        cpf_cnpj = form_agricultor.cpf_cnpj.data
        endereco = form_agricultor.endereco.data
        responsavel = form_agricultor.responsavel.data
        email = form_agricultor.email.data
        telefone = form_agricultor.telefone.data
        produtos = form_agricultor.produtos.data
        certificacao = form_agricultor.certificacao.data
        mensagem = form_agricultor.mensagem.data

        # Realiza o processamento dos dados do agricultor
        print(f"Dados do Agricultor: Propriedade={nome_propriedade}, CPF/CNPJ={cpf_cnpj}, Produtos={produtos}")
        return redirect(url_for('cadastro_sucesso'))
    else:
        return render_template('agricultores.html', form_agricultor=form_agricultor)

@app.route('/cadastro_sucesso')
def cadastro_sucesso():
    return render_template('cadastro_sucesso.html')

if __name__ == '__main__':
    app.run(debug=True)