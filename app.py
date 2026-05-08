from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = "super_secret_key_2026"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Codigo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(100), unique=True, nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)


with app.app_context():
    db.create_all()

    if Codigo.query.count() == 0:
        codigos_iniciais = [
            "VIP123",
            "PREMIUM2026",
            "ACESSO777"
        ]

        for c in codigos_iniciais:
            novo = Codigo(codigo=c)
            db.session.add(novo)

        db.session.commit()


@app.route('/')
def login_page():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    codigo_digitado = request.form.get('codigo')

    codigo = Codigo.query.filter_by(
        codigo=codigo_digitado,
        ativo=True
    ).first()

    if codigo:
        session['acesso'] = True
        session['codigo'] = codigo_digitado
        return redirect('/painel')

    return render_template(
        'login.html',
        erro='Código inválido'
    )


@app.route('/painel')
def painel():
    if not session.get('acesso'):
        return redirect('/')

    return render_template(
        'painel.html',
        codigo=session.get('codigo')
    )


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/admin')
def admin():
    codigos = Codigo.query.all()
    return render_template('admin.html', codigos=codigos)


@app.route('/gerar_codigo')
def gerar_codigo():
    novo_codigo = secrets.token_hex(4).upper()

    novo = Codigo(codigo=novo_codigo)
    db.session.add(novo)
    db.session.commit()

    return redirect('/admin')


@app.route('/desativar/<int:id>')
def desativar(id):
    codigo = Codigo.query.get(id)

    if codigo:
        codigo.ativo = False
        db.session.commit()

    return redirect('/admin')


if __name__ == '__main__':
    app.run(debug=True)