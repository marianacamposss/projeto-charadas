from flask import Flask, jsonify, request  # Importa o Flask para criar a API, jsonify para formatar respostas JSON e request para capturar dados das requisições.
import random  # Importa a biblioteca random para escolher uma charada aleatoriamente.
import firebase_admin  # Importa o Firebase Admin SDK para conectar com o Firestore.
from firebase_admin import credentials, firestore  # Importa as credenciais e o Firestore para armazenar os dados.
from flask_cors import CORS  # Importa o CORS para permitir que a API seja acessada de diferentes domínios.
import os
import json
from dotenv import load_dotenv #Carrega variaveis do firebase a partir de variaveis de ambiente

# Inicializa a aplicação Flask
app = Flask(__name__)
CORS(app)  # Habilita CORS para permitir requisições de diferentes origens

load_dotenv()

FBKEY = json.loads(os.getenv('CONFIG_FIREBASE'))
os.getenv('CONFIG_FAREBASE')

# Autenticação com o Firebase usando um arquivo de credenciais
cred = credentials.Certificate(FBKEY)

firebase_admin.initialize_app(cred)

# Conecta ao banco de dados Firestore
db = firestore.client()

# ---- Rota principal de teste ----
@app.route('/', methods=['GET'])  # Define a rota raiz da API

def index():
    return 'CHARADAS API', 200  # Retorna uma mensagem de boas-vindas

# ---- Método GET - Charada aleatória ----
@app.route('/charadas', methods=['GET'])  # Define a rota para obter uma charada aleatória
def charada_aleatoria():
    charadas = [item.to_dict() for item in db.collection('charadas').stream()]

    if charadas:
        return jsonify(random.choice(charadas)), 200  # Retorna uma charada aleatória em formato JSON
    else:
        return jsonify({'mensagem': 'Erro! Nenhuma charada encontrada'}), 404  # Retorna erro se não houver charadas

# ---- Método GET - Buscar charada pelo ID ----
@app.route('/charadas/<id>', methods=['GET'])  # Define a rota para buscar uma charada específica pelo ID
def busca(id):
    doc_ref = db.collection('charadas').document(id)  # Acessa o documento com o ID fornecido
    doc = doc_ref.get()

    if doc.exists:
        return jsonify(doc.to_dict()), 200  # Retorna a charada encontrada
    else:
        return jsonify({'mensagem': 'Erro! - Charada não encontrada'}), 404  # Retorna erro se a charada não existir

# ---- Método POST - Adicionar nova charada ----
@app.route('/charadas', methods=['POST'])  # Define a rota para adicionar uma nova charada
def adicionar_charada():
    dados = request.json  # Captura os dados enviados na requisição

    if 'pergunta' not in dados or "resposta" not in dados:
        return jsonify({'mensagem': 'Erro! - Dados inválidos'}), 400  # Retorna erro se os campos obrigatórios não forem informados
    
    # Atualiza o contador de IDs para garantir um novo ID único
    contador_ref = db.collection('controle_id').document('contador')
    contador_doc = contador_ref.get().to_dict()
    
    if contador_doc:
        ultimo_id = contador_doc.get('id', 0)
    else:
        ultimo_id = 0
        contador_ref.set({'id': 0})  # Se não existir, cria o contador
    
    novo_id = ultimo_id + 1
    contador_ref.update({'id': novo_id})

    # Adiciona a nova charada ao banco de dados
    db.collection('charadas').document(str(novo_id)).set({
        "id": novo_id,
        "pergunta": dados['pergunta'],
        "resposta": dados['resposta']
    })
    return jsonify({'mensagem': 'Charada adicionada com sucesso!'}), 201  # Retorna sucesso

# ---- Método PUT - Alterar charada existente ----
@app.route('/charadas/<id>', methods=['PUT'])  # Define a rota para alterar uma charada existente
def alterar_charada(id):
    dados = request.json  # Captura os dados da requisição
    
    if 'pergunta' not in dados or "resposta" not in dados:
        return jsonify({'mensagem': 'Erro! Campos pergunta e resposta são obrigatórios'}), 400  # Valida os campos obrigatórios
    
    doc_ref = db.collection('charadas').document(id)  # Obtém a referência do documento
    doc = doc_ref.get()
    
    if doc.exists:
        doc_ref.update({
            "pergunta": dados['pergunta'],
            "resposta": dados['resposta']
        })
        return jsonify({'mensagem': 'Charada alterada com sucesso!'}), 200  # Retorna sucesso
    else:
        return jsonify({'mensagem': 'Erro! - Charada não encontrada'}), 404  # Retorna erro se a charada não existir
    
# ---- Método DELETE - Remover charada ----
@app.route('/charadas/<id>', methods=['DELETE'])  # Define a rota para deletar uma charada
def deletar_charada(id):
    doc_ref = db.collection('charadas').document(id)  # Obtém a referência do documento
    doc = doc_ref.get()
    
    if not doc.exists:
        return jsonify({'mensagem': 'Erro! - Charada não encontrada'}), 404  # Retorna erro
    
    doc_ref.delete()  # Remove a charada do banco de dados
    return jsonify({'mensagem': 'Charada deletada com sucesso!'}), 200  # Retorna sucesso

# ---- Inicializa o servidor Flask ----
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Inicia a API na porta 5000 e ativa o modo debug