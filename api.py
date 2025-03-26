# api.py
import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_script(description, theme):
    prompt = f"Generate a script for a {theme} video based on the following description: {description}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        temperature=0.7,
    )
    script = response['choices'][0]['text'].strip()
    return script
