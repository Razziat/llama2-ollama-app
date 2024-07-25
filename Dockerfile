# Ollama server Dockerfile

FROM ubuntu:20.04

# Install dependencies
RUN apt-get update && apt-get install -y python3 python3-pip wget curl

# Create a directory for Ollama
RUN mkdir -p /opt/ollama/bin

# Copy the Ollama binary
COPY ollama /opt/ollama/bin/ollama

# Make the binary executable
RUN chmod +x /opt/ollama/bin/ollama

# Copy the setup script
COPY setup.sh /opt/ollama/setup.sh
RUN chmod +x /opt/ollama/setup.sh

# Set environment variables for Ollama
ENV OLLAMA_HOST=0.0.0.0
ENV OLLAMA_ORIGINS=http://0.0.0.0:11434

# Expose the port for the Ollama server
EXPOSE 11434

# Start the setup script
CMD ["/opt/ollama/setup.sh"]
