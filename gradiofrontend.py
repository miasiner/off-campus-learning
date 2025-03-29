import os
from dotenv import load_dotenv
import gradio as gr
from openai import OpenAI
from speechify import Speechify

# pip install openai
# pip install speechify-api

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Initialize Speechify client
speechify_client = Speechify(token=os.environ.get("SPEECHIFY_API_KEY"))

# Function to generate the monologue script
def generate_script(theme, description):
    prompt = f"Generate a {theme} monologue based on the following description: {description}"
    
    response = client.responses.create(
        model="gpt-4o",  
        instructions="You are an AI script writer. Generate a monologue only, without formatting or stage directions.",
        input=prompt
    )
    
    monologue = response.output_text.strip()
    return monologue

# Function to convert the monologue to audio and save it locally
def generate_audio(monologue):
    # Use Speechify to convert text to speech
    audio_stream = speechify_client.tts.audio.stream(
        accept="audio/mpeg",  # Desired audio format
        input=monologue,
        voice_id="005ccf96-959d-4eeb-920f-f13e2bb84f21"  # You can specify any voice you want here
    )
    
    # Save the audio file locally by consuming the audio stream
    audio_file_path = "generated_audio.mp3"
    
    # Write the content of the audio stream to a file
    with open(audio_file_path, 'wb') as f:
        for chunk in audio_stream:
            f.write(chunk)  # Write each chunk to the file
    
    return audio_file_path

# Gradio interface
theme_options = ["Challenge video", "True crime video", "Drama yap session video"]

def generate_script_and_audio(theme, description):
    # Step 1: Generate the script (monologue)
    monologue = generate_script(theme, description)

    # Step 2: Generate the audio from the monologue
    audio_file_path = generate_audio(monologue)

    return monologue, audio_file_path

demo = gr.Interface(
    fn=generate_script_and_audio,
    inputs=[
        gr.Dropdown(theme_options, label="Select a Theme"),
        gr.Textbox(placeholder="Enter video description here...", label="Video Description")
    ],
    outputs=[
        gr.Textbox(label="Generated Monologue"),
        gr.Audio(label="Generated Speech", type="filepath")  # Provide the file path for the audio
    ],
    title="AI Monologue Generator",
    description="Generate a monologue and convert it to speech using AI."
)

demo.launch()
