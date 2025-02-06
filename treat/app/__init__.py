from flask import Flask
from flask_cors import CORS
import os
import google.generativeai as genai

# Get the absolute path for the template and static folders
base_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(base_dir, "../../templates")
static_dir = os.path.join(base_dir, "../../static")

# Initialize Flask app
app = Flask(
    __name__,
    template_folder=template_dir,
    static_folder=static_dir
)

# Enable CORS
CORS(app)

# Load Google API key and initialize Gemini
try:
    with open("google_api_key.txt", "r") as f:
        api_key = f.read().strip()
        genai.configure(api_key=api_key)
except FileNotFoundError:
    print("Warning: google_api_key.txt not found. Please ensure it exists before analyzing content.")

# Import routes after initializing the Flask app
from app import routes