import gradio as gr
import requests

API_URL = "http://127.0.0.1:5000/generate_script"

def get_script(description, theme):
    response = requests.post(API_URL, json={"description": description, "theme": theme})
    if response.status_code == 200:
        return response.json().get("script", "Script generation failed.")
    else:
        return f"Error: {response.status_code} - {response.text}"

with gr.Blocks() as demo:
    gr.Markdown("# Video Script Generator")
    description = gr.Textbox(label="Description", placeholder="Enter your video description here...")
    theme = gr.Radio(label="Select Theme", choices=["Challenge video", "True crime video", "Drama yap session video"])
    
    generate_button = gr.Button("Generate Script")
    output_textbox = gr.Textbox(label="Generated Script")

    generate_button.click(fn=get_script, inputs=[description, theme], outputs=[output_textbox])

demo.launch()
