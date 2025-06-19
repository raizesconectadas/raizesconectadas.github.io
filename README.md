# 🌳 Raízes Conectadas: Conectando o Campo à Mesa! 🏫

Bem-vindo(a) ao repositório do projeto **Raízes Conectadas**! 👋

Este projeto super especial tem como objetivo principal conectar nossos queridos agricultores familiares diretamente com as escolas, garantindo que a merenda escolar seja sempre fresquinha, nutritiva e venha da nossa terra. É uma iniciativa que valoriza a produção local e nutre o futuro das nossas crianças!

---

## 🚀 Como Explorar Nosso Projeto

Aqui você vai encontrar a estrutura do nosso aplicativo web feito com Flask. Para facilitar sua vida (e a minha, que adoro um código organizado!), separei tudo direitinho em pastas.

### 📄 Páginas do Site (Nossos HTMLs Humanizados!)

Todos os arquivos HTML das nossas páginas estão guardados com carinho na pasta `templates`. Eles são a "cara" do nosso site!

* **Página Inicial (Home):** Onde tudo começa! Apresenta a ideia geral do Raízes Conectadas.
    * [Acessar `index.html`](./templates/index.html)
* **Cadastro de Agricultores:** Se você planta, aqui é seu lugar! Formulário para nossos agricultores se cadastrarem.
    * [Acessar `agricultores.html`](./templates/agricultores.html)
* **Cadastro de Escolas:** Sua escola quer merenda de qualidade e de pertinho? É por aqui!
    * [Acessar `escolas.html`](./templates/escolas.html)
* **Sucesso do Cadastro (Agradecimento):** A página que aparece depois que tudo deu certo no cadastro. Um "muito obrigado!" com carinho.
    * [Acessar `agradecimento.html` (ou `cadastro_sucesso.html`)](./templates/agradecimento.html)
    * *P.S.: No nosso código Python (`app.py`), a gente chamou essa rota de `cadastro_sucesso`, mas o arquivo mesmo tá como `agradecimento.html`. Coisas de dev, né? 😉*

### 🎨 Estilos e Beleza (Nosso CSS)

Para deixar o site com aquela carinha amigável e bonita, todos os nossos estilos CSS estão aqui:

* [Acessar `style.css`](./static/css/style.css)

### 🖼️ Imagens do Projeto (Alegria para os Olhos!)

As imagens que ilustram e dão vida ao nosso site estão guardadas na pasta `static/images`. Dá uma espiadinha!

* **Exemplo de Imagem:** `agricultor_colhendo.jpg`, `criancas_merenda.jpeg` (e outras que você tiver!)
    * [Ver Imagens na Pasta](./static/images/)

---

## ⚙️ Configuração Local (Para rodar o projeto na sua máquina!)

Se você quiser brincar um pouco com o código ou contribuir, siga esses passos básicos:

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/SeuUsuario/NomeDoSeuRepositorio.git](https://github.com/SeuUsuario/NomeDoSeuRepositorio.git)
    cd NomeDoSeuRepositorio
    ```
2.  **Crie e ative um ambiente virtual** (sempre bom para não bagunçar seu Python!):
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Linux/macOS
    # ou
    .\venv\Scripts\activate   # No Windows
    ```
3.  **Instale as dependências** (Flask, Flask-WTF, SQLAlchemy, etc.):
    ```bash
    pip install -r requirements.txt # Se você tiver um arquivo requirements.txt
    # Ou instale individualmente se preferir:
    # pip install Flask Flask-WTF Flask-SQLAlchemy Flask-Migrate psycopg2-binary
    ```
4.  **Configure seu banco de dados PostgreSQL:**
    * Crie um banco de dados e um usuário no PostgreSQL.
    * Atualize a `SQLALCHEMY_DATABASE_URI` no `app.py` com suas credenciais.
5.  **Rode as migrações do banco de dados** (isso cria as tabelas):
    ```bash
    flask db init
    flask db migrate -m "Cria tabelas iniciais"
    flask db upgrade
    ```
6.  **Inicie o aplicativo Flask:**
    ```bash
    flask run
    ```
    Depois é só abrir seu navegador e ir para `http://127.0.0.1:5000`!

---

## 🤝 Quer Contribuir?

Se você gostou da ideia e quer ajudar a melhorar o Raízes Conectadas, suas contribuições são super bem-vindas! Abra uma `issue` para ideias ou `pull requests` com suas melhorias.

---

Feito com ❤️ e muita dedicação pelo [Seu Nome/Nome da Equipe] para o CETI Lucas Meireles Alves.

</div>
