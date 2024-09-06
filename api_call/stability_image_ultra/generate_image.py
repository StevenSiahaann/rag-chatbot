import requests
import streamlit as st
from io import BytesIO
from PIL import Image
import time
import os
from dotenv import load_dotenv

load_dotenv() 
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")
STABILITY_API_HOST = "https://api.stability.ai/v2beta/stable-image/generate/ultra"

def generate_image_from_stability(prompt, aspect_ratio="3:2", seed=0, output_format="png"):
    headers = {"Accept": "image/*", "Authorization": f"Bearer {STABILITY_API_KEY}"}
    params = {
        "prompt": prompt,
        "negative_prompt": "low quality, blurry, pixelated, distorted, overexposed...",
        "aspect_ratio": aspect_ratio,
        "seed": str(seed),
        "output_format": output_format
    }
    response = requests.post(STABILITY_API_HOST, headers=headers, files={key: (None, value) for key, value in params.items()})
    if response.status_code == 200:
        output_image = response.content
        finish_reason = response.headers.get("finish-reason")
        seed = response.headers.get("seed")
        if finish_reason == 'CONTENT_FILTERED':
            st.warning("Generation failed due to NSFW classifier")
            return None, None
        return output_image, seed
    else:
        st.error(f"Failed to generate image. HTTP Error: {response.status_code}, {response.text}")
        return None, None
    
def handle_add_temp_knowledge_pdf(uploaded_file):
    temp_file = f"sample_data/{uploaded_file.name}"
    with open(temp_file, "wb") as file:
        file.write(uploaded_file.getvalue())
    return temp_file

def handle_image_response(image_data, seed, output_format):
    st.write("Image generated successfully:")
    image = Image.open(BytesIO(image_data))
    st.image(image, caption=f"Generated Image with Seed: {seed}")
    img_bytes = BytesIO()
    image.save(img_bytes, format=output_format.upper())
    img_bytes.seek(0)
    st.download_button(label="Download Image", data=img_bytes, file_name=f"generated_image_{seed}_{str(time.time())}.{output_format}", mime=f"image/{output_format}")
