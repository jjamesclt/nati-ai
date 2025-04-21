from flask import request, jsonify
from .chatbot import get_bot_response

def register_routes(app):

    @app.route('/chat', methods=['POST'])
    def chat():
        message = request.json.get('message')
        response = get_bot_response(message)
        return jsonify({'response': response})

    @app.route('/api', methods=['POST'])
    def api():
        payload = request.json
        return jsonify({
            'input': payload,
            'message': 'API endpoint received your request.',
            'status': 'success'
        })
