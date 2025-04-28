import os
from dotenv import load_dotenv
import gradio as gr
from openai import OpenAI
from speechify import Speechify
from PIL import Image
import io
import requests

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Initialize Speechify client
speechify_client = Speechify(token=os.environ.get("SPEECHIFY_API_KEY"))

# Function to generate the monologue script
def generate_script(theme, description):
    prompt = f"Generate a {theme} monologue based on the following description: {description} . Make the video fun and engaging. Make it interesting and keep the audience engaged. We want this to go viral."
    
    response = client.responses.create(
        model="gpt-4",  
        instructions="You are an AI script writer. Generate a monologue only, without formatting or stage directions.",
        input=prompt
    )
    
    monologue = response.output_text.strip()
    return monologue

# Function to generate a thumbnail using DALL-E
def generate_thumbnail(monologue, theme):
    # Create theme-specific prompts
    theme_prompts = {
        "Mr Beast Video": "Create a high-energy YouTube thumbnail in MrBeast style. Include bold text, bright colors, and dramatic imagery. The thumbnail should look expensive and viral-worthy, similar to MrBeast's thumbnails with dramatic facial expressions and eye-catching elements.",
        "True crime video": "Create a mysterious and dramatic true crime YouTube thumbnail. Use dark, moody colors with dramatic lighting. Include elements like crime scene tape, dramatic shadows, or mysterious imagery. The style should be similar to popular true crime channels.",
        "Call Her Daddy Video": "Create a bold, edgy YouTube thumbnail in the style of Call Her Daddy. Use vibrant colors, bold text, and confident imagery. The thumbnail should be attention-grabbing and slightly provocative, similar to the podcast's branding."
    }
    
    # Get the theme-specific prompt
    theme_prompt = theme_prompts.get(theme, "Create a YouTube thumbnail that is eye-catching and professional.")
    
    # Create the final prompt
    thumbnail_prompt = f"{theme_prompt} Content context: {monologue[:100]}... The thumbnail should be optimized for YouTube with bold text, vibrant colors, and professional design elements that will make viewers want to click."
    
    # Generate image using DALL-E
    response = client.images.generate(
        model="dall-e-3",
        prompt=thumbnail_prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    
    # Get the image URL
    image_url = response.data[0].url
    
    # Download the image
    image_response = requests.get(image_url)
    image = Image.open(io.BytesIO(image_response.content))
    
    # Save the image
    thumbnail_path = "generated_thumbnail.png"
    image.save(thumbnail_path)
    
    return thumbnail_path

# Function to convert the monologue to audio and save it locally
def generate_audio(monologue):
    # Use Speechify to convert text to speech
    audio_stream = speechify_client.tts.audio.stream(
        accept="audio/mpeg",  # Desired audio format
        input=monologue,
        voice_id="0134fdf0-b4a3-40f7-b225-a0db5498e1a0"  # You can specify any voice you want here
    )
    
    # Save the audio file locally by consuming the audio stream
    audio_file_path = "generated_audio.mp3"
    
    # Write the content of the audio stream to a file
    with open(audio_file_path, 'wb') as f:
        for chunk in audio_stream:
            f.write(chunk)  # Write each chunk to the file
    
    return audio_file_path

# Gradio interface
theme_options = ["Mr Beast Video", "True crime video", "Call Her Daddy Video"]

def generate_script_and_audio(theme, description):
    # Step 1: Generate the script (monologue)
    monologue = generate_script(theme, description)

    # Step 2: Generate the audio from the monologue
    audio_file_path = generate_audio(monologue)
    
    # Step 3: Generate the thumbnail
    thumbnail_path = generate_thumbnail(monologue, theme)

    return monologue, audio_file_path, thumbnail_path

demo = gr.Interface(
    fn=generate_script_and_audio,
    inputs=[
        gr.Dropdown(theme_options, label="Select a Theme"),
        gr.Textbox(placeholder="Enter video description here...", label="Video Description")
    ],
    outputs=[
        gr.Textbox(label="Generated Monologue"),
        gr.Audio(label="Generated Speech", type="filepath"),
        gr.Image(label="Generated Thumbnail", type="filepath")
    ],
    title="AI Monologue Generator",
    description="Generate a monologue, convert it to speech, and create a thumbnail using AI."
)

demo.launch()
