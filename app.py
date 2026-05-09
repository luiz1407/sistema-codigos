from flask import Flask, request, redirect, session, render_template_string, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pyotp

# =========================================
# APP
# =========================================

app = Flask(__name__)

CORS(app)

app.secret_key = "admin_secret_2026"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# =========================================
# DATABASE
# =========================================

db = SQLAlchemy(app)

# =========================================
# TABELA
# =========================================

class Conta(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(120), unique=True)

    secret = db.Column(db.String(120))

    plataforma = db.Column(db.String(50))

# =========================================
# CRIAR BANCO
# =========================================

with app.app_context():
    db.create_all()

# =========================================
# LOGIN ADMIN
# =========================================

ADMIN_USER = "admin"

ADMIN_PASS = "123456"

# =========================================
# HTML LOGIN
# =========================================

LOGIN_HTML = """

<h1>Login Admin</h1>

<form method="POST">

<input type="text" name="user" placeholder="Usuário">
<br><br>

<input type="password" name="pass" placeholder="Senha">
<br><br>

<button type="submit">Entrar</button>

</form>

"""

# =========================================
# HTML ADMIN
# =========================================

ADMIN_HTML = """

<h1>Painel Admin</h1>

<a href="/logout">Sair</a>

<hr>

<h2>Adicionar Conta</h2>

<form method="POST" action="/add">

<input name="email" placeholder="Email">
<br><br>

<input name="secret" placeholder="Secret">
<br><br>

<input name="plataforma" placeholder="Plataforma">
<br><br>

<button type="submit">Adicionar</button>

</form>

<hr>

<h2>Contas</h2>

{% for conta in contas %}

<div style="margin-bottom:20px;border:1px solid #ccc;padding:10px;">

<b>Email:</b> {{ conta.email }}
<br>

<b>Plataforma:</b> {{ conta.plataforma }}
<br>

{% set codigo = pyotp.TOTP(conta.secret).now() %}

<b>Código:</b>

<h2>{{ codigo }}</h2>

<a href="/delete/{{ conta.id }}">Remover</a>

</div>

{% endfor %}

"""

# =========================================
# LOGIN
# =========================================

@app.route('/', methods=['GET', 'POST'])

def login():

    if request.method == 'POST':

        user = request.form.get('user')

        senha = request.form.get('pass')

        if user == ADMIN_USER and senha == ADMIN_PASS:

            session['admin'] = True

            return redirect('/admin')

    return render_template_string(LOGIN_HTML)

# =========================================
# ADMIN
# =========================================

@app.route('/admin')

def admin():

    if not session.get('admin'):

        return redirect('/')

    contas = Conta.query.all()

    return render_template_string(
        ADMIN_HTML,
        contas=contas,
        pyotp=pyotp
    )

# =========================================
# ADD CONTA
# =========================================

@app.route('/add', methods=['POST'])

def add():

    if not session.get('admin'):

        return redirect('/')

    email = request.form.get('email')

    secret = request.form.get('secret')

    plataforma = request.form.get('plataforma')

    nova = Conta(
        email=email,
        secret=secret,
        plataforma=plataforma
    )

    db.session.add(nova)

    db.session.commit()

    return redirect('/admin')

# =========================================
# DELETE
# =========================================

@app.route('/delete/<int:id>')

def delete(id):

    if not session.get('admin'):

        return redirect('/')

    conta = Conta.query.get(id)

    if conta:

        db.session.delete(conta)

        db.session.commit()

    return redirect('/admin')

# =========================================
# LOGOUT
# =========================================

@app.route('/logout')

def logout():

    session.clear()

    return redirect('/')

# =========================================
# API
# =========================================

@app.route('/api/contas')

def api_contas():

    contas = Conta.query.all()

    resultado = []

    for conta in contas:

        codigo = pyotp.TOTP(conta.secret).now()

        resultado.append({

            "id": conta.id,
            "email": conta.email,
            "plataforma": conta.plataforma,
            "codigo": codigo

        })

    return jsonify(resultado)

# =========================================
# START
# =========================================

if __name__ == '__main__':

    app.run(debug=True)

@app.route('/teste')

def teste():

    return 'FUNCIONANDO'