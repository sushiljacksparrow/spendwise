# Use the official Ollama image as the base
FROM ollama/ollama:latest AS ollama

# Set up the Python environment
FROM python:3.9

# Set the working directory
WORKDIR /app

# Install Ollama and other dependencies
COPY --from=ollama /bin/ollama /usr/local/bin/
# Install libssl-dev to make sure the ssl module is available in python
RUN apt-get -y update && apt-get install -y tesseract-ocr libssl-dev

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code
COPY src/ .
COPY templates/ templates/

# Pull the model
RUN ollama serve & \
    sleep 5 && \
    ollama pull llama2:7b

# Expose the port
EXPOSE 5000

# Start Ollama and the Flask app
CMD ["sh", "-c", "ollama serve & python ./server.py"]
