from flask import Flask, render_template, request, redirect, url_for
import os
import re
import json
from PIL import Image
import pytesseract
import ollama

server = Flask(__name__, template_folder='../templates')

# define a folder to store and later serve the images
UPLOAD_FOLDER = '/static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# function to check the file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# route and function to handle the upload page
@server.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):

            # call the OCR function on it
            extracted_text = ocr_core(file)

            # process the OCR text with Ollama
            receipt_data = process_with_ollama(extracted_text)

            # extract the text and display it
            return render_template('upload.html',
                                   msg='Successfully processed',
                                   receipt_data=receipt_data,
                                   img_src=UPLOAD_FOLDER + file.filename)
    elif request.method == 'GET':
        return render_template('upload.html')

def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """
    config = '--psm 4'
    text = pytesseract.image_to_string(Image.open(filename), config=config)
    return text

def process_with_ollama(text):
    """
    This function will process the OCR text with Ollama to get structured data.
    """
    prompt = f"""
    The following text is the output of an OCR scan of a store receipt.
    Please extract the store name, date, time, and a list of items with their prices.
    Return the information as a JSON object with the following keys: "store_name", "date", "time", "items".
    The "items" should be a list of objects, where each object has the keys "item" and "price".
    If you find any errors in the OCR output, please try to correct them.

    OCR Text:
    {text}
    """

    response = ollama.chat(model='llama2:7b', messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])

    try:
        # The LLM output might not be a perfect JSON, so we need to be careful
        result_text = response['message']['content']
        json_part = result_text[result_text.find('{'):result_text.rfind('}')+1]
        receipt_data = json.loads(json_part)
    except (json.JSONDecodeError, IndexError, KeyError):
        # If the LLM fails to return a valid JSON, we return a default object
        receipt_data = {
            "store_name": "Unknown",
            "date": "Unknown",
            "time": "Unknown",
            "items": []
        }

    return receipt_data

if __name__ == "__main__":
   server.run(debug=True, host='0.0.0.0')
