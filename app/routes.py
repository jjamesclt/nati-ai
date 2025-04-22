from flask import request, jsonify
from .chatbot import get_bot_response

def register_routes(app):

    @app.route('/', methods=['GET'])
    def index():
        return 'nati-ai Falcon model running. Use POST /chat or /api.', 200

    @app.route('/chat', methods=['GET', 'POST'])
    def chat():
        if request.method == 'GET':
            return 'Use POST with JSON body: {"message": "your text"}', 200
        message = request.json.get('message')
        response = get_bot_response(message)
        return jsonify({'response': response})

    @app.route('/api', methods=['GET', 'POST'])
    def api():
        if request.method == 'GET':
            return 'Use POST with JSON body: {"key": "value"}', 200
        payload = request.json
        return jsonify({
            'input': payload,
            'message': 'API endpoint received your request.',
            'status': 'success'
        })
