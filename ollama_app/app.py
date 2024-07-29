from flask import Flask, request, render_template, redirect, url_for, jsonify, session
import requests
import os
import json
import time
import logging

app = Flask(__name__)
app.secret_key = os.urandom(24)

OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://ollama-server:11434')

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_chat', methods=['POST'])
def create_chat():
    session['chat_history'] = []
    session['model'] = request.form['model']
    return redirect(url_for('chat'))

@app.route('/chat')
def chat():
    model = session.get('model', 'default_model')
    chat_history = session.get('chat_history', [])
    return render_template('chat.html', model=model, chat_history=chat_history)

@app.route('/query', methods=['POST'])
def query():
    user_input = request.form['user_input']
    model = session.get('model', 'default_model')

    chat_history = session.get('chat_history', [])
    chat_history.append({'role': 'user', 'content': user_input})
    
    logging.info(f"Received user input: {user_input}")

    # Add previous context to the prompt
    prompt = "\n".join([f"{entry['role']}: {entry['content']}" for entry in chat_history])
    
    response = requests.post(f"{OLLAMA_URL}/api/generate", json={'model': model, 'prompt': prompt}, stream=True)

    try:
        full_response = ""
        for line in response.iter_lines():
            if line:
                res_json = json.loads(line.decode('utf-8'))
                full_response += res_json.get('response', '')
        
        chat_history.append({'role': 'assistant', 'content': full_response})
        session['chat_history'] = chat_history

        logging.info("Successfully received response from model.")
        return render_template('chat.html', model=model, chat_history=chat_history)
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
        return f"Error: {response.text}", 500
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return f"Error: {response.text}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
