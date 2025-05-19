import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API token from environment or use hardcoded one (for testing)
api_token = os.getenv("HF_TOKEN") or "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"

# Set up the headers with the API token
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

# Updated model URL for v0.3
url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"

# Define the payload with an example prompt
payload = {
    "inputs": "[INST] What is AI? [/INST]"
}

# Make the POST request to Hugging Face API
response = requests.post(url, headers=headers, json=payload)

# Print out the status and response from the API
print("STATUS CODE:", response.status_code)
print("RESPONSE TEXT:", response.text)
