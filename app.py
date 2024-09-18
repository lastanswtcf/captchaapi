from flask import Flask, render_template, jsonify
import random
import string
import os
from PIL import Image, ImageDraw, ImageFont
import base64

app = Flask(__name__)
CAPTCHA_DIR = 'static/captcha'

os.makedirs(CAPTCHA_DIR, exist_ok=True)

def generate_captcha():
    text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    width, height = 200, 80
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    for i, char in enumerate(text):
        x = 20 + i * 30
        y = random.randint(10, 30)
        font = ImageFont.load_default()
        draw.text((x, y), char, font=font, fill=(random.randint(0, 150), random.randint(0, 150), random.randint(0, 150)))

    captcha_filename = f"{text}.png"
    captcha_path = os.path.join(CAPTCHA_DIR, captcha_filename)
    image.save(captcha_path)
    
    return captcha_filename

@app.route('/api/generate_captcha', methods=['GET'])
def api_generate_captcha():
    filename = generate_captcha()
    captcha_path = os.path.join(CAPTCHA_DIR, filename)

    with open(captcha_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    
    return jsonify({"captcha_data": f"data:image/png;base64,{encoded_string}"})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
