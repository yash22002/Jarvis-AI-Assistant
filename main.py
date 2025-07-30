import pyttsx3
import speech_recognition as sr
import pywhatkit
import webbrowser
import wikipedia
import pyautogui
import pyperclip
import time
import os
from datetime import datetime

# Speak function
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
    engine.say(text)
    engine.runAndWait()

# Take voice input
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Speak now...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except:
        speak("Sorry sir, I didn't understand.")
        return ""

# Wikipedia search
def search_wikipedia(query):
    try:
        topic = query.replace("what is", "").replace("who is", "").replace("tell me about", "").strip()
        speak(f"Searching Wikipedia for {topic}")
        result = wikipedia.summary(topic, sentences=2)
        print("📚", result)
        speak(result)
    except wikipedia.exceptions.DisambiguationError:
        speak("Topic is too broad. Please be more specific.")
    except wikipedia.exceptions.PageError:
        speak("Sorry, no matching page found.")
    except Exception:
        speak("Error fetching data from Wikipedia.")

# Remember multiple items
def remember_this(info):
    with open("memory.txt", "a") as file:
        file.write(info + "\n")
    speak("Okay sir, I will remember that.")

# Recall all memory
def recall_memory():
    if os.path.exists("memory.txt"):
        with open("memory.txt", "r") as file:
            lines = file.readlines()
            if lines:
                speak("Sir, here is everything you asked me to remember:")
                for item in lines:
                    speak(item.strip())
            else:
                speak("I don't have anything in memory right now.")
    else:
        speak("No memory found, sir.")

# Greet function
def greet():
    hour = datetime.now().hour
    if hour < 12:
        speak("Good morning sir.")
    elif hour < 18:
        speak("Good afternoon sir.")
    else:
        speak("Good evening sir.")
    speak("I am Jarvis, your persnal A I assistant. How can I help you?")

greet()

clipboard_content = ""

# Listening Loop
while True:
    query = take_command()

    # Exit
    if "exit" in query or "bye" in query:
        speak("Goodbye sir. Have a nice day!")
        break

    # Recall memory
    elif "what do you remember" in query or "do you remember anything" in query or "recall" in query:
        recall_memory()

    # Remember something
    elif "remember that" in query or ("remember" in query and "what do you remember" not in query):
        info = query.replace("remember that", "").replace("remember", "").strip()
        if info:
            remember_this(info)
        else:
            speak("What should I remember, sir?")

    # Wikipedia Search
    elif "what is" in query or "who is" in query or "tell me about" in query:
        search_wikipedia(query)

    # YouTube Play
    elif "play" in query:
        song = query.replace("play", "").strip()
        speak(f"Playing {song} on YouTube")
        pywhatkit.playonyt(song)

    # Open Website
    elif "open" in query:
        site = query.replace("open", "").strip().replace(" ", "")
        if "." not in site:
            site += ".com"
        url = f"https://www.{site}"
        webbrowser.open(url)
        speak(f"Opening {site}")

    # Generate Image
    elif "generate image of" in query or "create image of" in query:
        topic = query.replace("generate image of", "").replace("create image of", "").strip()
        url = f"https://www.craiyon.com/?prompt={topic.replace(' ', '-')}"
        webbrowser.open(url)
        speak(f"Generating image of {topic}. Please click the 'Draw' button to start.")

    # Copy Commandclipboardclipboardclipboard
    elif "copy jarvis" in query or "jarvis copy" in query:
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.5)
        clipboard_content = pyperclip.paste()
        print("✅ Copied:", clipboard_content)
        speak("Text copied to clipboard")

    # Paste Command
    elif "paste jarvis" in query or "jarvis paste" in query or "paste it" in query:
        if clipboard_content:
            pyautogui.write(clipboard_content)
            speak("Text pasted successfully.")
        else:
            speak("Clipboard is empty, sir.")

    # Fallback
    elif query:
        speak("I'm not sure how to respond to that yet, sir.")
