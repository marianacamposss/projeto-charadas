from flask import Flask, jsonify, redirect
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

lista_charadas = [
    {"id": 1, "pergunta": "O que é, o que é? A capital brasileira que está presente em todos os aniversários", "resposta": "Palmas"},
    {"id": 2, "pergunta": "O que é, o que é? Que dá o poder de atravessar paredes", "resposta": "Porta"},
    {"id": 3, "pergunta": "O que é, o que é? Tem centenas de rodas, mas não sai do lugar", "resposta": "Estacionamento"},
    {"id": 4, "pergunta": "O que é, o que é? O zero disse para o oito", "resposta": "Cinto"},
    {"id": 5, "pergunta": "O que é, o que é? O motivo dos ovos não contarem piadas", "resposta": "Rachar"},
    {"id": 6, "pergunta": "O que é, o que é? A praia disse ao mar", "resposta": "Onda"},
    {"id": 7, "pergunta": "O que é, o que é? Quebra quando se fala", "resposta": "Segredo"},
    {"id": 8, "pergunta": "O que é, o que é? Quanto mais se tira, maior ele fica.", "resposta": "Buraco"},
    {"id": 9, "pergunta": "O que é, o que é? Não tem boca, mas sempre responde quando falam com ele.", "resposta": "Eco"},
    {"id": 10, "pergunta": "O que é, o que é? Tem chaves, mas não abre portas.", "resposta": "Teclado"}
]


@app.route("/")
def index(): 
    return redirect('/charadas/random')
@app.route('/charadas', methods=['GET'])
def obter_todas_charadas():
    charadas_embaralhadas = random.sample(lista_charadas, len(lista_charadas))
    return jsonify(charadas_embaralhadas), 200

@app.route('/charadas/random', methods=['GET'])
def obter_charada_aleatoria():
    return jsonify(random.choice(lista_charadas)), 200

if __name__ == '__main__':
    app.run(debug=True, port=5004)
