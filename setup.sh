#!/bin/sh

echo "Starting Ollama setup..."

# Start the Ollama server
/opt/ollama/ollama serve &

# Wait for the server to start
sleep 10

# Pull the model
echo "Pulling tinyllama model..."
/opt/ollama/ollama pull tinyllama

# Indicate that the setup is complete
echo "Model pulled successfully, Ollama setup complete."

# Keep the server running
wait
