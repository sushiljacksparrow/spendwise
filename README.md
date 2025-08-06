# OCR Web Application

This is a simple web application that uses Tesseract to perform Optical Character Recognition (OCR) on images.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* Python 3
* pip
* Tesseract

You will need to have Tesseract installed on your system. You can find installation instructions for your OS here: [https://github.com/tesseract-ocr/tesseract/wiki](https://github.com/tesseract-ocr/tesseract/wiki)

### Installing

1. Clone the repository:
   ```bash
   git clone https://github.com/example/ocr-app.git
   cd ocr-app
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the server:
   ```bash
   python src/server.py
   ```

The server will be running at `http://localhost:5000`. You can access the application by navigating to `http://localhost:5000/upload` in your web browser.

To change the port, you can set the `PORT` environment variable:
```bash
export PORT=8080
python src/server.py
```

## Docker

You can also run the application using Docker.

1. Build the Docker image:
   ```bash
   docker build -t ocr-app .
   ```

2. Run the Docker container:
   ```bash
   docker run -p 5000:5000 ocr-app
   ```

The application will be accessible at `http://localhost:5000/upload`.
