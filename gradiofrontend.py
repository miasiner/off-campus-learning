# import gradio as gr
# import requests

# API_URL = "http://127.0.0.1:5000/generate_script"

# def get_script(description, theme):
#     response = requests.post(API_URL, json={"description": description, "theme": theme})
#     if response.status_code == 200:
#         return response.json().get("script", "Script generation failed.")
#     else:
#         return f"Error: {response.status_code} - {response.text}"

# with gr.Blocks() as demo:
#     gr.Markdown("# Video Script Generator")
#     description = gr.Textbox(label="Description", placeholder="Enter your video description here...")
#     theme = gr.Radio(label="Select Theme", choices=["Challenge video", "True crime video", "Drama yap session video"])
    
#     generate_button = gr.Button("Generate Script")
#     output_textbox = gr.Textbox(label="Generated Script")

#     generate_button.click(fn=get_script, inputs=[description, theme], outputs=[output_textbox])

# demo.launch()
import os
from dotenv import load_dotenv
import gradio as gr
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from the environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to generate the script
def generate_script(theme, description):
    prompt = f"Generate a {theme} monologue based on the following description: {description}. The monologue should be long enough to cover a two minute video. Only include the spoken parts of the monologue in your output."
    
    response = client.responses.create(
        model="gpt-3.5-turbo",
        input=prompt
    )
    
    script = response.output_text.strip()
    return script

# Gradio interface
theme_options = ["Challenge video", "True crime video", "Drama yap session video"]

demo = gr.Interface(
    fn=generate_script,
    inputs=[gr.Dropdown(theme_options, label="Select a Theme"),
            gr.Textbox(placeholder="Enter video description here...", label="Video Description")],
    outputs="textbox",
    title="AI Video Script Generator",
    description="Generate a script for your themed video using AI. Select a theme and provide a description to get started."
)

demo.launch()
