import speech_recognition as sr
import pyttsx3
import webbrowser
from google import genai
import os
import datetime
import subprocess
import requests
from dotenv import load_dotenv

load_dotenv()
engine = pyttsx3.init()
engine.setProperty('rate', 110)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

chatStr = ""
def chat(query):
    global chatStr
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    chatStr+=f"User said: {query} "
    response = client.models.generate_content(
    model="gemini-2.0-flash", contents=chatStr
    )
    response_text = response.text.lstrip("Jarvis:").strip()
    print("Jarvis:", response_text)
    say(response_text) 
    chatStr += f"Jarvis: {response_text} \n"
    return response_text
    
def ai(prompt):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    text = f"Gemini response for prompt: {' '.join(prompt.split()[2:])} \n ************************\n\n"
    response = client.models.generate_content(
    model="gemini-2.0-flash", contents=prompt
    )

    text+=response.text
    if not os.path.exists("Gemini"):
        os.mkdir("Gemini")
    with open(f"Gemini/{' '.join(prompt.split()[2:])}.txt", "w") as f:
        f.write(text)


def get_weather(city):
    api_key = os.getenv("OPENWEATHER_API_KEY") 
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    response = requests.get(base_url, params=params)
    data = response.json()

    if data["cod"] == 200:
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        weather_info = f"The temperature in {city} is {temp}°C with {description}."
        print(f"Jarvis: {weather_info}")
        say(weather_info)
        return weather_info
    else:
        say("Sorry, I couldn't fetch the weather.")
        return "Weather data not found."

def get_news(query=None):
    api_key = os.getenv("NEWSAPI_API_KEY")  
    base_url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": api_key,
        "country": "us",
        "q": query,       
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if data["status"] == "ok":
        articles = data["articles"]
        if articles:
            news = f"Here are the top headlines:"
            for index, article in enumerate(articles, start=1):
                title = article["title"]
                description = article["description"]
                url = article["url"]
                news += f"\n\nArticle {index}: {title}\nDescription: {description}\nRead more: {url}"
            print(news)
            say(news)
        else:
            say("No articles found for your query.")
    else:
        say("Sorry, I couldn't fetch the news at the moment.")
        print("Failed to fetch news.")
              
def say(text):
    engine.say(text)
    engine.runAndWait()
    
def takeCommand():
     r=sr.Recognizer()
     with sr.Microphone() as source:
         r.pause_threshold = 0.6
         audio = r.listen(source)
         try:
             print("Recognizing...")
             query = r.recognize_google(audio, language="en-in")
             print(f"User said: {query}\n")
             return query
         except Exception as e:
             return "Some Error Occurred. Sorry from Jarvis."
         
if __name__ == '__main__':
    say("Hello I am Jarvis AI")
    while True:
        print("Listening...")
        query = takeCommand()
        if query == "Some Error Occurred. Sorry from Jarvis.":
            print("Recognition failed. Let's try again...")
            continue
        
        site_opened = False
        sites=[["YouTube","https://www.youtube.com"],["Wikipedia","https://www.wikipedia.com"],["Instagram","https://www.instagram.com"],["Google","https://www.google.com"],["Facebook","https://www.facebook.com"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
                site_opened = True
                break
            
        app_opened = False     
        apps = [["Calculator", "start calc"],["Notepad", "start notepad"],["Paint", "start mspaint"],["Camera", "start microsoft.windows.camera:"],["Spotify", "start spotify:"]]
        for app in apps:
            if f"open {app[0]}".lower() in query.lower():
                say(f"Opening {app[0]} sir...")
                subprocess.run(app[1], shell=True)
                app_opened = True
                break
           
        if "the time" in query:
            strDate = datetime.datetime.now().strftime("%B %d, %Y")
            strTime = datetime.datetime.now().strftime("%H:%M:%S")  
            say(f"Sir, the date is {strDate} and the time is {strTime}")

        elif "Using AI".lower() in query.lower():
            ai(prompt=query)
                
        elif "reset chat".lower() in query.lower():
            chatStr = ""
        
        elif "help" in query.lower():
            say("You can ask me to open websites, apps, tell time, or chat using AI.")
            
        elif "Jarvis exit".lower() in query.lower():
            say("Goodbye, Gaurav. Have a great day!")
            exit()
               
        elif "weather" in query.lower():
            say("Which city's weather would you like to know?")
            city_query = takeCommand()
            get_weather(city_query) 
            
        elif "news" in query.lower():
            say("What type of news would you like to hear? Please specify a topic or say 'latest'.")
            news_query = takeCommand()
            get_news(news_query)
            
        elif not site_opened and not app_opened and not ("the time" in query or "Using AI" in query or "weather" in query or "help" in query or "reset chat" in query or "Jarvis exit" in query or "news" in query):
            print("Chatting...")
            chat(query)
