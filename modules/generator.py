from google import genai
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

# Get API key
API_KEY = os.getenv("GEMINI_API_KEY")

# Assign API key
client = genai.Client(api_key= API_KEY)

def generate_content(prompt : str):
    response = client.models.generate_content(model= "gemini-3.5-flash", contents= prompt)
    output = response.text

    return output
