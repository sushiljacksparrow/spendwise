from flask import Flask, render_template, request, redirect, url_for
import os
import re
server = Flask(__name__, template_folder='../templates')

@server.route("/")
def index():
    return redirect(url_for('upload_page'))

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

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

            # parse the receipt
            receipt_data = parse_receipt(extracted_text)

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
    text = pytesseract.image_to_string(Image.open(filename), config=config)  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text

def parse_receipt(text):
    """
    This function will parse the OCR text and extract structured data.
    """
    lines = text.split('\n')

    store_name = lines[0] if lines else "Unknown"

    date_pattern = r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}'
    time_pattern = r'\d{1,2}:\d{2}'

    date = "Unknown"
    time = "Unknown"

    for line in lines:
        if re.search(date_pattern, line):
            date = re.search(date_pattern, line).group()
        if re.search(time_pattern, line):
            time = re.search(time_pattern, line).group()

    price_pattern = r'([0-9]+\.[0-9]+)'
    parsed_items = []
    for line in lines:
        if re.search(price_pattern, line):
            try:
                price_match = re.search(price_pattern, line)
                price = float(price_match.group())
                item = line[:price_match.start()].strip()
                parsed_items.append({'item': item, 'price': price})
            except (ValueError, AttributeError):
                continue

    return {
        'store_name': store_name,
        'date': date,
        'time': time,
        'receipt_items': parsed_items
    }

if __name__ == "__main__":
   server.run(debug=True, host='0.0.0.0')
