import os
import json
import random
from flask import Flask, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configure Gemini API
# NOTE: Set GOOGLE_API_KEY as an env variable in Render
API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

# A2A Compliant Agent Card
@app.route('/a2a/illustration_agent/.well-known/agent.json', methods=['GET'])
@app.route('/a2a/agent.json', methods=['GET'])
def get_agent_card():
    card = {
        "name": "illustration_agent",
        "description": "An agent designed to generate branded illustrations for Cymbal Stadiums.",
        "defaultInputModes": ["text/plain"],
        "defaultOutputModes": ["application/json"],
        "skills": [
            {
                "id": "illustrate_text",
                "name": "Illustrate Text",
                "description": "Generate an illustration to illustrate the meaning of provided text.",
                "tags": ["illustration", "image generation"]
            }
        ],
        "url": f"https://{request.host}/a2a/illustration_agent",
        "capabilities": {},
        "version": "1.0.0"
    }
    return jsonify(card)

# A2A Task Endpoint
@app.route('/a2a/illustration_agent/task', methods=['POST'])
@app.route('/task', methods=['POST'])
def handle_task():
    data = request.json
    user_prompt = data.get("prompt", "Stadium Maintenance")
    
    # 1. Enhance prompt with brand guidelines using Gemini
    brand_context = (
        "You are the Cymbal Stadiums Illustration Agent. "
        "Enhance the user prompt for 'Corporate Memphis' style illustration. "
        "Use stadium and maintenance imagery with purples (#BF40BF) and bright greens (#DAF7A6) on sunset gradients. "
        "Keep the prompt brief and descriptive for an image model."
    )
    
    enhanced_prompt = f"Corporate Memphis style: {user_prompt}"
    if model:
        try:
            response = model.generate_content(f"{brand_context}\nUser says: {user_prompt}")
            enhanced_prompt = response.text
        except Exception as e:
            print(f"Error calling Gemini: {e}")
    
    # 2. Call Real Image Generation (Pollinations.ai)
    # This is a public URL-based generator for unique image generation
    encoded_prompt = enhanced_prompt.replace(" ", "%20").replace("\n", "")
    image_url = f"https://pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed={random.randint(1, 99999)}"
    
    return jsonify({
        "status": "success",
        "enhanced_prompt": enhanced_prompt.strip(),
        "image_url": image_url,
        "message": f"Here is your real-time branded illustration for: {user_query}"
    })

@app.route('/', methods=['GET'])
def home():
    return "Cymbal Stadiums Illustration Agent is LIVE on Render!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
