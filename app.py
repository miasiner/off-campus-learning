# app.py
from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
app = Flask(__name__)

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

@app.route('/generate_script', methods=['POST'])
def generate_script_route():
    data = request.get_json()
    description = data.get('description')
    theme = data.get('theme')

    if not description or not theme:
        return jsonify({'error': 'Description and theme are required'}), 400

    if theme not in ['Challenge video', 'True crime video', 'Drama yap session video']:
        return jsonify({'error': 'Invalid theme selected.'}), 400

    try:
        script = generate_script(description, theme)
        return jsonify({'script': script})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
