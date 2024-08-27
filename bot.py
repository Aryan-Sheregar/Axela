# genai_helper.py
from dotenv import load_dotenv
import os
import google.generativeai as genai
load_dotenv()
google_api_key = os.getenv('GOOGLE_API')


genai.configure(api_key=google_api_key)

model = genai.GenerativeModel('gemini-1.5-flash')

# Store context as an array of strings
context_store = []


def add_context(context):
    """Add a new context string to the context store."""
    context_store.append(context)


def clear_context():
    context_store.clear()


def generate_response(prompt, context=""):
    # Combine all contexts from the context store and the new context
    full_context = " ".join(context_store)
    full_prompt = f"{full_context} {context} {prompt}".strip()  # Combine full context with prompt
    response = model.generate_content(full_prompt)
    return response.text

