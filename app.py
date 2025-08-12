from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = 'data.json'


def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)


@app.route('/empresas', methods=['GET'])
def get_empresas():
    data = load_data()
    return jsonify(data)


@app.route('/empresas/<int:empresa_id>', methods=['GET'])
def get_empresa(empresa_id):
    data = load_data()
    empresa = next((e for e in data if e['id'] == empresa_id), None)
    if empresa:
        return jsonify(empresa)
    return jsonify({'erro': 'Empresa não encontrada'}), 404


@app.route('/empresas', methods=['POST'])
def adicionar_empresa():
    data = load_data()
    novo = request.get_json()

    if not novo.get('nome') or not novo.get('cnpj'):
        return jsonify({'erro': 'Nome e CNPJ são obrigatórios'}), 400

    novo['id'] = max([e['id'] for e in data], default=0) + 1
    data.append(novo)
    save_data(data)
    return jsonify(novo), 201


@app.route('/empresas/<int:empresa_id>', methods=['PUT'])
def editar_empresa(empresa_id):
    data = load_data()
    empresa = next((e for e in data if e['id'] == empresa_id), None)
    if not empresa:
        return jsonify({'erro': 'Empresa não encontrada'}), 404

    atualizacao = request.get_json()
    empresa.update(atualizacao)
    save_data(data)
    return jsonify(empresa)


@app.route('/empresas/<int:empresa_id>', methods=['DELETE'])
def excluir_empresa(empresa_id):
    data = load_data()
    novo_data = [e for e in data if e['id'] != empresa_id]

    if len(data) == len(novo_data):
        return jsonify({'erro': 'Empresa não encontrada'}), 404

    save_data(novo_data)
    return jsonify({'mensagem': 'Empresa excluída com sucesso'})


# Novo método de pesquisa
@app.route('/empresas/pesquisar', methods=['GET'])
def pesquisar_empresa():
    nome = request.args.get('nome', '').lower()
    cnpj = request.args.get('cnpj', '')

    data = load_data()

    if nome:
        data = [e for e in data if nome in e['nome'].lower()]

    if cnpj:
        data = [e for e in data if cnpj in e['cnpj']]

    if not data:
        return jsonify({'erro': 'Nenhuma empresa encontrada'}), 404

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
