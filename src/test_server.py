import os
import pytest
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from server import server, ocr_core
import json

# Helper function to create a fake image
def create_fake_receipt_image():
    """
    Creates an in-memory image that looks like a receipt.
    """
    text = """
    My Awesome Store
    123 Main St, Anytown, USA
    Date: 10/10/2025 Time: 10:00

    ITEM 1 1 10.00
    ITEM 2 2 20.00
    TOTAL 30.00
    TIP 5.00
    """
    img = Image.new('RGB', (400, 300), color = (255, 255, 255))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 15)
    except IOError:
        font = ImageFont.load_default()
    d.text((10,10), text, fill=(0,0,0), font=font)

    img_io = BytesIO()
    img.save(img_io, 'PNG', name='test_receipt.png')
    img_io.seek(0)
    return img_io

# Test for the ocr_core function
def test_ocr_core_receipt():
    """
    Tests the ocr_core function with a fake receipt image.
    """
    fake_image = create_fake_receipt_image()
    text = ocr_core(fake_image)
    assert "My Awesome Store" in text
    assert "10.00" in text

# Test for the /upload endpoint
@pytest.fixture
def client():
    server.config['TESTING'] = True
    with server.test_client() as client:
        yield client

def test_upload_page_integration_receipt(client, mocker):
    """
    Tests the /upload endpoint by simulating a receipt upload.
    """
    # Mock the ollama.chat function
    mock_response = {
        'message': {
            'content': '{"store_name": "My Awesome Store", "date": "10/10/2025", "time": "10:00", "receipt_items": [{"item": "ITEM 1", "price": 10.0, "quantity": 1, "category": "grocery"}, {"item": "ITEM 2", "price": 20.0, "quantity": 2, "category": "grocery"}], "total_amount": 30.0, "tip": 5.0}'
        }
    }
    mocker.patch('ollama.chat', return_value=mock_response)

    fake_image = create_fake_receipt_image()

    response = client.post('/upload',
                           data={'file': (fake_image, 'test_receipt.png')},
                           content_type='multipart/form-data')

    assert response.status_code == 200
    assert b'Successfully processed' in response.data
    assert b'My Awesome Store' in response.data
    assert b'10/10/2025' in response.data
    assert b'10:00' in response.data
    assert b'ITEM 1' in response.data
    assert b'10.0' in response.data
    assert b'grocery' in response.data
    assert b'30.0' in response.data
    assert b'5.0' in response.data
