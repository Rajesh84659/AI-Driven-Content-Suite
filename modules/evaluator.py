from google import genai
from dotenv import load_dotenv
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "templates", "prompt_templates.json")

# Get Evaluation Prompt
with open(DATA_DIR, "r") as f:
        templates = json.load(f)

evaluation_prompt = templates.get("evaluation", {}).get("prompt", {})

# Load .env variables
load_dotenv()

# Get API key
API_KEY = os.getenv("GEMINI_API_KEY")

# Assign API key
client = genai.Client(api_key= API_KEY)

def evaluate_content(response):
    
   # Final Prompt
   final_prompt = evaluation_prompt.replace("<<content>>", response)   

   # Generate Evaluation Response
   evaluation_response = client.models.generate_content(model= "gemini-3.5-flash", contents= final_prompt)
   evaluation_text = evaluation_response.text

   # Clean JSON Formatting
   evaluation_text = evaluation_text.replace("```json", "")
   evaluation_text = evaluation_text.replace("```", "")
   evaluation_text = evaluation_text.strip()

   # Convert String to JSON
   evaluation_report = json.loads(evaluation_text)

   return evaluation_report
