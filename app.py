from flask import Flask, request, jsonify
import requests
from deepface import DeepFace
import os
from PIL import Image
from io import BytesIO

app = Flask(__name__)

# Function to download an image from a URL and save it to a file
def download_image(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Extract the file name without query parameters
    img_name_with_ext = url.split("/")[-1].split("?")[0]

    img = Image.open(BytesIO(response.content))
    img.save(img_name_with_ext)
    return img_name_with_ext

@app.route('/verify', methods=['POST'])
def compare_faces():
    # Get image data from JSON body
    data = request.get_json()
    image1_url = data.get('base_image')
    image2_url = data.get('comparison_image')

    # Ensure user provides URLs for both images
    if not image1_url or not image2_url:
        return jsonify({"error": "Both base_image and comparison_image URLs are required."}), 400

    try:
        # Download and save images
        image1_path = download_image(image1_url)
        image2_path = download_image(image2_url)

        # Perform face verification using DeepFace
        result = DeepFace.verify(img1_path=image1_path, img2_path=image2_path)
        verification_result = {
            "verified": result["verified"],
            "distance": result["distance"]
        }

        # Clean up temporary images after processing
        os.remove(image1_path)
        os.remove(image2_path)

        return jsonify(verification_result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
