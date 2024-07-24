from flask import Flask, request, render_template, redirect, url_for, jsonify
import requests
import os
import json
import time
import logging

app = Flask(__name__)

OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://ollama-server:11434')

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_assistant', methods=['POST'])
def create_assistant():
    assistant_type = request.form['assistant_type']
    logging.info(f"Creating assistant with type: {assistant_type}")

    model_file_content = f"""
    model tinyllama
    type {assistant_type}
    """
    with open('Modelfile', 'w') as f:
        f.write(model_file_content)

    logging.info("Sending request to pull model...")
    response = requests.post(f"{OLLAMA_URL}/api/pull", json={'model': 'tinyllama'})

    if response.status_code == 200:
        logging.info("Model pull request successful, redirecting to loading page.")
        return redirect(url_for('loading'))
    else:
        logging.error(f"Error pulling model: {response.text}")
        return f"Error pulling model: {response.text}", 500

@app.route('/loading')
def loading():
    return render_template('loading.html')

@app.route('/check_status')
def check_status():
    retries = 20
    while retries > 0:
        try:
            logging.info("Checking model status...")
            response = requests.post(f"{OLLAMA_URL}/api/generate", json={'model': 'tinyllama', 'prompt': ''})
            if response.status_code == 200:
                logging.info("Model is ready, redirecting to assistant page.")
                return redirect(url_for('assistant'))
        except requests.exceptions.ConnectionError as e:
            logging.warning(f"Connection error: {e}, retries left: {retries}")
            retries -= 1
            time.sleep(15)
    logging.error("Failed to connect to Ollama server after multiple retries.")
    return jsonify({'status': 'loading'})

@app.route('/assistant')
def assistant():
    return render_template('assistant.html')

@app.route('/query', methods=['POST'])
def query():
    user_input = request.form['user_input']
    logging.info(f"Received user input: {user_input}")

    response = requests.post(f"{OLLAMA_URL}/api/generate", json={'model': 'tinyllama', 'prompt': user_input}, stream=True)

    try:
        full_response = ""
        for line in response.iter_lines():
            if line:
                res_json = json.loads(line.decode('utf-8'))
                full_response += res_json.get('response', '')
        logging.info("Successfully received response from model.")
        return render_template('assistant.html', response=full_response)
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
        return f"Error: {response.text}", 500
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return f"Error: {response.text}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
