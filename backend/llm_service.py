# llm_service.py
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# --- IMPORTANT ---
# Make sure you have your OpenAI API key in a file named .env
# The .env file should look like this:
# OPENAI_API_KEY="sk-YourSecretKeyGoesHere"
# -----------------

try:
    # Initialize the OpenAI client
    # The client automatically looks for the OPENAI_API_KEY in environment variables
    client = OpenAI()
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    # You might want to handle this more gracefully
    client = None

def get_llm_completion(prompt_text):
    """
    Sends a prompt to the OpenAI API and gets a JSON completion.
    """
    if not client:
        return '{"error": "OpenAI client not initialized. Check your API key."}'

    try:
        # Create a chat completion request to the API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",  # A model that is good at following instructions
            messages=[
                {"role": "system", "content": "You are a helpful nutrition planning assistant. Respond with only a valid JSON object, without any surrounding text or markdown formatting."},
                {"role": "user", "content": prompt_text}
            ],
            response_format={"type": "json_object"} # Use JSON mode for reliable output
        )
        # Extract the JSON string from the response
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"An error occurred while calling the OpenAI API: {e}")
        # Return an error formatted as a JSON string to prevent the app from crashing
        return f'{{"error": "Failed to get a response from the LLM.", "details": "{str(e)}"}}'
