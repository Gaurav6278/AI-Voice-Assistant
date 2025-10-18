# AI-Voice-Assistant

A Python-based voice assistant using Gemini API for voice interaction and task automation.

Overview

This is a Python-based AI Voice Assistant that can:

Recognize your voice commands.

Speak responses using text-to-speech.

Open websites and applications.

Fetch weather and news.

Interact with AI using Google Gemini API (optional, using .env for API key storage).

Features

Voice Commands: Talk to Jarvis and it will respond or perform actions.

AI Chat: Interact with Google Gemini AI using voice or text input.

Web & App Automation: Open websites like YouTube, Google, and apps like Calculator, Notepad, etc.

Weather Updates: Get weather information for any city.

News Fetching: Get top headlines based on your query.

Installation

Clone the repository:

git clone https://github.com/Gaurav6278/AI-Voice-Assistant.git

cd AI-Voice-Assistant

Create a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows

Install dependencies:

pip install -r requirements.txt

Create a .env file to store API keys (optional for Gemini AI):

GEMINI_API_KEY=your_api_key_here
OPENWEATHER_API_KEY=your_api_key_here
NEWSAPI_KEY=your_api_key_here

Usage

Run the main script:

python main.py

Then you can:

Speak commands (e.g., "Open YouTube", "weather", "news", "the time").

Type commands in the terminal.

Reset chat with "reset chat".

Exit Jarvis with "Jarvis exit".


Dependencies:

speech_recognition

pyttsx3

requests

python-dotenv

google-genai (for AI functionality)

Note:

Make sure you have a microphone connected for voice commands.

API keys for Gemini AI, OpenWeather, and NewsAPI should be placed in .env.

Without .env, only local features (opening apps, websites, telling time) will work.
