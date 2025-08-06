import os
import pytest
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from server import server, ocr_core

# Helper function to create a fake image
def create_fake_image(text="Hello, world!", size=(400, 200), format='PNG'):
    """
    Creates an in-memory image with the given text.
    """
    img = Image.new('RGB', size, color = (255, 255, 255))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 30)
    except IOError:
        font = ImageFont.load_default()
    d.text((10,10), text, fill=(0,0,0), font=font)

    img_io = BytesIO()
    img.save(img_io, format, name='test.png')
    img_io.seek(0)
    return img_io

# Test for the ocr_core function
def test_ocr_core():
    """
    Tests the ocr_core function with a fake image.
    """
    fake_image = create_fake_image(text="This is a test")
    text = ocr_core(fake_image)
    assert "This is a test" in text

# Test for the /upload endpoint
@pytest.fixture
def client():
    server.config['TESTING'] = True
    with server.test_client() as client:
        yield client

def test_upload_page_integration(client):
    """
    Tests the /upload endpoint by simulating a file upload.
    """
    fake_image = create_fake_image(text="Another test")

    response = client.post('/upload',
                           data={'file': (fake_image, 'test.png')},
                           content_type='multipart/form-data')

    assert response.status_code == 200
    assert b'Successfully processed' in response.data
    assert b'Another test' in response.data
