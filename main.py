from flask import Flask, jsonify
from app import create_app

app = create_app('default')

@app.route('/')
def index():
    return jsonify({
        "name": "MoradiApp API",
        "version": "1.0.0",
        "description": "Backend API for MoradiApp - Gestão de Repúblicas Estudantis"
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint não encontrado'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Erro interno do servidor'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)