#!/bin/sh

echo "Starting Ollama setup..."

# Start the Ollama server
/opt/ollama/bin/ollama serve &

# Wait for the server to start
sleep 10

# Ensure the Modelfile directory exists
mkdir -p /opt/ollama

# Ensure Modelfile is a file, not a directory
if [ ! -f "/opt/ollama/Modelfile" ]; then
  echo "Modelfile does not exist, creating a default one."
  echo "model mistral" > /opt/ollama/Modelfile
fi

# Pull the model
echo "Pulling mistral model..."
/opt/ollama/bin/ollama pull mistral

# Indicate that the setup is complete
echo "Model pulled successfully, Ollama setup complete."

# Keep the server running
wait
