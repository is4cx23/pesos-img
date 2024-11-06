from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///imc.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    peso = db.Column(db.Float, nullable=False)
    altura = db.Column(db.Float, nullable=False)

    def __init__(self, nome, peso, altura):
        self.nome = nome
        self.peso = peso
        self.altura = altura

with app.app_context():
    db.create_all()

def calculate_imc(peso, altura):
    altura_metros = altura / 100   
    imc = peso / (altura_metros ** 2)
    return imc

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form['nome']
        peso = float(request.form['peso'])
        altura = float(request.form['altura'])

        imc = calculate_imc(peso, altura)

        if imc < 18.5:
            imc_message = "Você está abaixo do peso."
        elif 18.5 <= imc < 24.9:
            imc_message = "Você está com peso normal."
        elif 25 <= imc < 29.9:
            imc_message = "Você está com sobrepeso."
        else:
            imc_message = "Você está com obesidade."

        novo_usuario = Usuario(nome=nome, peso=peso, altura=altura)
        db.session.add(novo_usuario)
        db.session.commit()

        return render_template('index.html', nome=nome, peso=peso, altura=altura, imc=imc, imc_message=imc_message)
    return render_template('index.html')

@app.route('/api/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([{
        "id": usuario.id,
        "nome": usuario.nome,
        "peso": usuario.peso,
        "altura": usuario.altura
    } for usuario in usuarios])

@app.route('/api/usuarios/<int:id>', methods=['GET'])
def get_usuario(id):
    usuario = Usuario.query.get(id)
    if usuario:
        return jsonify({
            "id": usuario.id,
            "nome": usuario.nome,
            "peso": usuario.peso,
            "altura": usuario.altura
        })
    return jsonify({"error": "Usuário não encontrado"}), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)