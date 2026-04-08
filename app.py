import os
from flask import Flask, request, jsonify
import keras
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

# Load the trained Keras 3 Siamese model
MODEL_PATH = 'model/siamese_digit_similarity.keras'
model = keras.models.load_model(
    MODEL_PATH, 
    custom_objects={'abs': abs}, 
    compile=False
)

def preprocess_image(image_bytes):
    # Convert image to grayscale ('L') and resize to 28x28 for MNIST
    image = Image.open(io.BytesIO(image_bytes)).convert('L')
    image = image.resize((28, 28))
    
    # Normalize pixel values to [0, 1]
    img_array = np.array(image) / 255.0
    
    # Expand dimensions to match model input shape (1, 28, 28, 1)
    return np.expand_dims(img_array, axis=(0, -1))

@app.route('/predict', methods=['POST'])
def predict():
    # Check if both images are present in the request
    if 'image1' not in request.files or 'image2' not in request.files:
        return jsonify({'error': 'Please provide both image1 and image2 as form data'}), 400
    
    try:
        # Read the file bytes
        img1_bytes = request.files['image1'].read()
        img2_bytes = request.files['image2'].read()
        
        # Preprocess both inputs
        img1_processed = preprocess_image(img1_bytes)
        img2_processed = preprocess_image(img2_bytes)
        
        # Predict similarity (Contrastive loss network output)
        prediction = model.predict([img1_processed, img2_processed])
        similarity_score = float(prediction[0][0])
        
        return jsonify({'similarity': similarity_score})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # host=0.0.0.0 and port 5000 as requested
    app.run(host='0.0.0.0', port=5000)