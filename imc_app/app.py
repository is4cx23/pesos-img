# app.py
from Flask import Flask, render_template, request, redirect, url_for
from Flask_sqlalchemy import SQLAlchemy
from Flask_migrate import Migrate
import config

app = Flask(__name__)
app.config.from_object(config)

# Configuração do banco de dados
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Person

# Função para calcular o IMC
def calculate_imc(weight, height):
    return weight / (height ** 2)

# Rota para exibir o formulário de IMC
@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        name = request.form["name"]
        weight = float(request.form["weight"])
        height = float(request.form["height"])
        imc = calculate_imc(weight, height)
        
        # Armazena os dados no banco de dados
        person = Person(name=name, weight=weight, height=height, imc=imc)
        db.session.add(person)
        db.session.commit()
        
        # Redireciona para a página de resultados
        return redirect(url_for("result", person_id=person.id))
    
    return render_template("form.html")

# Rota para exibir o resultado do IMC
@app.route("/result/<int:person_id>")
def result(person_id):
    person = Person.query.get(person_id)
    return render_template("result.html", person=person)

if __name__ == "__main__":
    app.run(debug=True)
