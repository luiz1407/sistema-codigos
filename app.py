from flask import Flask, render_template_string, request
import pyotp

app = Flask(__name__)

# ==========================================
# CONTAS VINCULADAS
# ==========================================

usuarios = {

    "ggmaxvendassteam@gmail.com": {
        "secret": "DD5CEWK6PNQGU2HACPWU6F5YDX2RNUSN",
        "plataforma": "Google"
    },

    "warzone@gmail.com": {
        "secret": "JBSWY3DPEHPK3PXP",
        "plataforma": "Activision"
    }

}

# ==========================================
# HTML
# ==========================================

HTML = """

<!DOCTYPE html>
<html lang="pt-br">
<head>

    <meta charset="UTF-8">

    <title>Gerador 2FA</title>

    <style>

        body{
            background:#0f172a;
            color:white;
            font-family:Arial;
            display:flex;
            justify-content:center;
            align-items:center;
            height:100vh;
            margin:0;
        }

        .card{
            background:#1e293b;
            padding:40px;
            border-radius:15px;
            width:380px;
            box-shadow:0 0 25px rgba(0,0,0,0.4);
        }

        h1{
            text-align:center;
            margin-bottom:25px;
        }

        input{
            width:100%;
            padding:14px;
            border:none;
            border-radius:8px;
            margin-bottom:15px;
            font-size:16px;
            box-sizing:border-box;
        }

        button{
            width:100%;
            padding:14px;
            background:#2563eb;
            border:none;
            border-radius:8px;
            color:white;
            font-size:16px;
            cursor:pointer;
        }

        button:hover{
            background:#1d4ed8;
        }

        .codigo{
            font-size:50px;
            text-align:center;
            margin-top:25px;
            color:#4ade80;
            font-weight:bold;
        }

        .erro{
            background:#dc2626;
            padding:12px;
            border-radius:8px;
            margin-top:20px;
            text-align:center;
        }

        .info{
            text-align:center;
            margin-top:10px;
            color:#cbd5e1;
        }

    </style>

</head>
<body>

<div class="card">

    <h1>Gerador 2FA</h1>

    <form method="POST">

        <input
            type="email"
            name="email"
            placeholder="Digite seu email"
            required
        >

        <button type="submit">
            Gerar Código
        </button>

    </form>

    {% if codigo %}

        <div class="codigo">
            {{ codigo }}
        </div>

        <div class="info">
            {{ email }}
        </div>

        <div class="info">
            Plataforma: {{ plataforma }}
        </div>

    {% endif %}

    {% if erro %}

        <div class="erro">
            {{ erro }}
        </div>

    {% endif %}

</div>

</body>
</html>

"""

# ==========================================
# ROTAS
# ==========================================

@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':

        email = request.form.get('email')

        # verifica email
        if email not in usuarios:

            return render_template_string(
                HTML,
                erro='Email não encontrado'
            )

        try:

            dados = usuarios[email]

            secret = dados["secret"]

            plataforma = dados["plataforma"]

            # cria TOTP
            totp = pyotp.TOTP(secret)

            # gera código
            codigo = totp.now()

            return render_template_string(
                HTML,
                codigo=codigo,
                email=email,
                plataforma=plataforma
            )

        except Exception as e:

            return render_template_string(
                HTML,
                erro=f'Erro ao gerar código: {str(e)}'
            )

    return render_template_string(HTML)

# ==========================================
# INICIAR SERVIDOR
# ==========================================

if __name__ == '__main__':
    app.run(debug=True)