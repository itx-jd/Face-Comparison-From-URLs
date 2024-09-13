from flask import Flask, request, jsonify
import requests
from io import BytesIO
import base64
from PIL import Image

app = Flask(__name__)

# Function to download an image from a URL
def download_image(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Extract the file name without query parameters
    img_name_with_ext = url.split("/")[-1].split("?")[0]
    
    with open(img_name_with_ext, 'wb') as file:
        file.write(response.content)
    
    return img_name_with_ext

# Function to save a base64-encoded image string to a file
def save_base64_image(base64_str):
    image_data = base64.b64decode(base64_str)
    img_path = "base64_image.jpg"  # Save it with a default name

    with open(img_path, 'wb') as file:
        file.write(image_data)

    return img_path

@app.route('/process_image', methods=['POST'])
def process_image():
    data = request.get_json()
    image_url = data.get('image_url')
    image_base64 = data.get('image_base64')

    if image_url and image_base64:
        return jsonify({"error": "Provide either image_url or image_base64, not both."}), 400

    try:
        if image_url:
            img_path = download_image(image_url)
        elif image_base64:
            img_path = save_base64_image(image_base64)
        else:
            return jsonify({"error": "image_url or image_base64 is required."}), 400

        return jsonify({"image_path": img_path})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
