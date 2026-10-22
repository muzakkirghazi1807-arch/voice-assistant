import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 170)

def speak(text):
    import pyttsx3   
    engine = pyttsx3.init()
    
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  
    engine.setProperty('rate', 170)

    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except:
        print("Sorry, I didn't understand")
        return ""


def wish():
    hour = datetime.datetime.now().hour

    if hour < 12:
        speak("Good Morning")
    elif hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")

    speak("I am jarvis, your personal assistant")


def run_assistant():
    wish()

    while True:
        command = take_command()

        if command == "":
            continue

        print("Command received:", command)

        if "time" in command:
           current_time = datetime.datetime.now().strftime("%I:%M %p")
           speak("The time is " + current_time)
        
        elif "google" in command:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")
        elif "how r u" in command:
            speak("I am functioning perfectly. How can I help you?")

        elif "your name" in command:
            speak("I am Jarvis, your assistant")

        elif "open gmail" in command:
             speak("Opening Gmail")
             webbrowser.open("https://mail.google.com")    

        elif "youtube" in command:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif "search" in command:
            query = command.replace("search", "").strip()
            speak("Searching for " + query)
            webbrowser.open(f"https://www.google.com/search?q={query}")

        elif "notepad" in command:
            speak("Opening Notepad")
            os.system("notepad")
        
        elif "wikipedia" in command or "who is" in command or "what is" in command:
            speak("Searching Wikipedia")
    
            query = command.replace("wikipedia", "")
            query = query.replace("who is", "")
            query = query.replace("what is", "")
    
            try:
                result = wikipedia.summary(query, sentences=2)
                speak(result)
            except:
                speak("Sorry, I couldn't find anything")


        elif "exit" in command:
            speak("Goodbye. Have a nice day")
            break

        else:
            speak("Sorry, I didn't understand that")

if __name__ == "__main__":
    run_assistant()