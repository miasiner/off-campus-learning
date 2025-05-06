# Off Campus Learning
This program is hypothetically used by an associated of Off Campus Learning to generate fun, entertaining, educational content for the company to post to their YouTube channel. A user of this program can choose a voice and a topic, which the program will use to generate a script of that topic, an audio file of the chosen voice reading the generated script, and a photo that goes along with the content of the script. All of the outputs can be read, listened to, or downloaded for further use.

## Setup
Before running the program, make sure you have the necessary dependencies installed:

```
pip install openai
pip install speechify-api
```

## Running the program
To launch the program locally, run the following command in your terminal from the project directory:
```
python3 gradiofrontend.py
```

or

```
python gradiofrontend.py
```

## Important notes

### API keys
This program makes API calls to OpenAI and Speechify. Thus, you will need your own API keys to make the program actually work. Keep in mind, this will likely cost a small amount of money. Here are the steps to do obtain and use your own API keys in our program:

1. [Obtain an API key from OpenAI](https://platform.openai.com/welcome?step=create)
2. [Obtain an API key from Speechify](https://speechify.com/text-to-speech-api/)
3. Create a file titled ".env" in the project folder.
4. In the .env file, paste the text below and fill in your API keys between the double quotes.

```
OPENAI_API_KEY="your-openai-key-here"
SPEECHIFY_API_KEY="your-speechify-key-here"
```

5. After you've created your .env file, you should be able to run the program!

### Speechify Voices
The voice ids provided in the code (under the comment "# voices") may not work unless you have our Speechify account API key. Thus, you may have to use different voice id's provided by Speechify, or create your own voices on your Speechify account.
