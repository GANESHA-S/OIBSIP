import sounddevice as sd
import vosk
import queue
import json
import requests
import pyttsx3
import nltk
from nltk.tokenize import word_tokenize
from datetime import datetime, timedelta
import threading
import webbrowser
from word2number import w2n

MODEL_PATH = "D:\\projects\\Oasis infobyte\\vosk-model-small-en-us-0.15"
model = vosk.Model(MODEL_PATH)
recognizer_queue = queue.Queue()
engine = pyttsx3.init()

def audio_callback(indata, frames, time, status):
    recognizer_queue.put(bytes(indata))

def speak(text):
    engine.say(text)
    engine.runAndWait()
    
def recognize_speech():
    recognizer = vosk.KaldiRecognizer(model, 16000)
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1, callback=audio_callback):
        speak("Hello! How can i help you?")
        while True:
            data = recognizer_queue.get()
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result).get("text", "")
                if text:
                    print(f"You said: {text}")
                    if handle_command(text):
                        break

def handle_command(command):
    tokens = word_tokenize(command.lower())
    
    if any(greet in tokens for greet in ["hello", "hi", "good", "morning", "evening", "afternoon"]):
        greet_user()
    elif "climate" in tokens or "weather" in tokens:
        ask_for_city()
    elif "time" in tokens or "date" in tokens:
        give_time_date()
    elif "reminder" in tokens:
        set_reminder()
    elif "my reminder" in tokens and "reminders" in tokens:
        tell_reminders()
    elif "search" in tokens:
        web_search(command)
    elif "thank" in tokens and "you" in tokens:
        speak("You're welcome! Goodbye!")
        return True
    else:
        speak("Sorry, I didn't understand.")
    return False

def greet_user():
    now = datetime.now()
    hour = now.hour
    if hour < 12:
        speak("Good morning!")
    elif hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
        
def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def ask_for_city():
    speak("Please tell me the city name.")
    city = wait_for_input()
    if city:
        get_climate(city)

def get_climate(city):
    api_key = "1a6511480bed9b7b706355319794a2ed"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        weather = response.json()
        temperature = weather["main"]["temp"]
        description = weather["weather"][0]["description"]
        speak(f"The temperature in {city} is {temperature} degrees Celsius with {description}.")
    else:
        speak("I couldn't fetch the climate information. Please try again.")

def give_time_date():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%B %d, %Y")
    speak(f"The time is {current_time} and today's date is {current_date}.")

def set_reminder():
    speak("What should I remind you about?")
    reminder_text = wait_for_input()
    speak("At what time should I set the reminder?")
    time_input = wait_for_input()
    
    try:
        minutes = w2n.word_to_num(time_input)
        reminder_time = datetime.now() + timedelta(minutes=minutes)
        reminders[reminder_time] = reminder_text
        speak(f"The Reminder is set for {reminder_time.strftime('%H:%M:%S')}.")
        threading.Timer(minutes * 60, trigger_reminder, args=[reminder_time]).start()
    except ValueError:
        speak("I couldn't understand. Please try again.")

reminders = {}       
def tell_reminders():
    if reminders:
        speak("Here are your active reminders:")
        for time, text in sorted(reminders.items()):
            speak(f"At {time.strftime('%H:%M:%S')}, remind you to {text}.")
    else:
        speak("You have no reminders.")


def trigger_reminder(reminder_time):
    reminder_text = reminders.pop(reminder_time, None)
    if reminder_text:
        speak(f"Reminder: {reminder_text}")

    
def web_search(query):
    speak("What would you like to search for?")
    search_query = wait_for_input()
    url = f"https://www.google.com/search?q={search_query}"
    speak(f"Searching for {search_query}.")
    webbrowser.open(url)
    
def open_website(command):
    speak("Which website should I open?")
    website_name = wait_for_input()
    if not website_name.startswith("http://") and not website_name.startswith("https://"):
        website_name = f"http://{website_name}"
    speak(f"Opening {website_name}.")
    webbrowser.open(website_name)

def wait_for_input():
    recognizer = vosk.KaldiRecognizer(model, 16000)
    while True:
        data = recognizer_queue.get()
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            text = json.loads(result).get("text", "")
            return text
        
if __name__ == "__main__":
    recognize_speech()