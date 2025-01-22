import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
import threading
import time
from gtts import gTTS
import pygame
import os

engine = pyttsx3.init()
newsapi = "201eafcba3ff41608e6b9e227a58d21e"

# Initialize the stop flag
stop_flag = False


def speak_old(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load("temp.mp3")

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(6)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 


def commandprocess(c):
    """Process the command."""
    global stop_flag #stop thenews
    try:
        print(f"Raw command received: {c}")
        print(f"Type of c: {type(c)}")  # Debugging: Check the type of c
        print(f"Lowercase command: {c.lower()}")  # Debugging: Ensure .lower() works

        if "open google" in c.lower():  # Correct use of .lower()
            speak("Opening Google...")
            webbrowser.open("https://www.google.com")
        elif "open chat gpt" in c.lower():
            print("Matched 'open chat gpt' condition.")
            speak("Opening ChatGPT...")
            try:
                webbrowser.open("https://chat.openai.com/")
            except Exception as e:
                speak("Failed to open ChatGPT.")
                print(f"Error: {e}")
            else:
                print("Did not match 'open chat gpt'.")


        elif "open facebook" in c.lower():
            speak("Opening Facebook...")
            webbrowser.open("https://www.facebook.com")
        elif "open youtube" in c.lower():
            speak("Opening YouTube...")
            webbrowser.open("https://www.youtube.com")
        elif "open linkedin" in c.lower():
            speak("Opening LinkedIn...")
            webbrowser.open("https://www.linkedin.com")

        elif c.lower().startswith("play"):
            song = c.lower().split(" ")[1]
            link = musiclibrary.music[song]
            webbrowser.open(link)


        elif "news" in c.lower():
            stop_flag = False
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
            if r.status_code == 200:
    # Parse the JSON response
                data = r.json()
                
                # Extract the articles
                articles = data.get('articles', [])
            
                # Print the headlines
                for article in articles:
                    if stop_flag:
                            speak("Stopping the news.")
                            break
                    speak(article['title'])
                    print(article['title'])
                    time.sleep(1)
            else:
                speak("Sorry, I couldn't fetch the news.")
        elif "stop" in c.lower():
            stop_flag = True
            speak("Stopping current task.")

        # elif c.lower().startswith("play"):
        #     song= c.lower().split(" ")[1]
        #     link= musiclibrary.music[song]
        #     webbrowser.open(link)
    
        elif():
            speak("Sorry, I couldn't find the song in your music library.")

        else:
             speak("Sorry, I couldn't process your request.")

    except Exception as e:
            print(f"Error: {e}")
       
if __name__ == "__angry_bird__":
    recognizer = sr.Recognizer()
    speak("Initializing Angry Bird...")
    while True:
        try:
            print("Waiting for the wake word: 'angry bird'")
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Listening...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                word = recognizer.recognize_google(audio)
                print(f"Wake word received: {word}")

            if word.lower() == "angry bird":
                speak("Yes?")
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    print("Angry Bird active. Listening for command...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)
                    print(f"Command received: {command}")

                    commandprocess(command)

        except sr.WaitTimeoutError:
            print("Listening timed out. Please speak again.")
        except sr.UnknownValueError:
            print("Could not understand the audio. Please try again.")
        except sr.RequestError as e:
            print(f"Request error from Google Speech Recognition: {e}")
        except Exception as e:
            print(f"Error: {e}")
