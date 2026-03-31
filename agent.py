import os
from typing import Optional
from google.adk import LlmAgent, tool
from google.cloud import storage
import google.generativeai as genai

# Setup Vertex AI / Gen AI (Gemini)
# In high-level ADK, this is often handled by the environment or wrapper
# but we define tools here.

@tool
def generate_image(prompt: str) -> str:
    """
    Generates a branded illustration according to Cymbal Stadiums guidelines.
    Guidelines: Corporate Memphis style, purples and greens on sunset gradients.
    """
    # 1. Enhance prompt with brand guidelines
    brand_prompt = f"A charming, flat, geometric, corporate memphis diagrammatic illustration with no text. {prompt}. " \
                   "The overall palette features prominent purple (#BF40BF) and bright green (#DAF7A6) accents, " \
                   "conveying a sense of efficient, collaborative achievement."
    
    # 2. Call the Image Generation Model (e.g., Imagen-3)
    # Note: Simplified for this lab example
    # In a real ADK agent, this would use Vertex AI SDK
    print(f"Generating image with prompt: {brand_prompt}")
    
    # 3. Upload to GCS and return URL
    # Assuming GCS bucket is set in env
    bucket_name = os.getenv("GCS_BUCKET", "cymbal-stadium-assets")
    # Simulate URL (in prod, use storage.Client().bucket(bucket_name).blob(filename).upload_from_string(...))
    image_url = f"https://storage.googleapis.com/{bucket_name}/illustrations/generated_{os.urandom(4).hex()}.png"
    
    return f"Here is your branded illustration: {image_url}"

# Define the Agent
instructions = """
You are the Cymbal Stadiums Illustration Agent. Your job is to help users create
branded images for their presentations and reports. 
Always use the generate_image tool. 
Ensure you translate generic requests into stadium/maintenance themed prompts 
that follow our brand guidelines (Corporate Memphis style).
"""

agent = LlmAgent(
    name="illustration_agent",
    instructions=instructions,
    tools=[generate_image]
)

if __name__ == "__main__":
    # Local ADK runner
    agent.run_web()
