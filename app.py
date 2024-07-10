from flask import Flask, render_template, request
import pyttsx3
import speech_recognition as sr
from datetime import datetime
import threading

app = Flask(__name__)
engine = pyttsx3.init()  # Initialize once
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Set voice (female)

# Create a lock for the speak function
speak_lock = threading.Lock()

# Function to speak
def speak(text):
    def speak_in_thread(text):
        with speak_lock:
            engine.say(text)
            engine.runAndWait()
        
    threading.Thread(target=speak_in_thread, args=(text,)).start()

# Function to listen
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print("You said:", text)
            return text.lower()  # Convert to lowercase for easier comparison
        except sr.UnknownValueError:
            print("Sorry, I could not understand what you said.")
            return ""
        except sr.RequestError:
            print("Sorry, my speech service is currently down.")
            return ""

# Function to respond based on user input
def respond(user_input):
    greetings = ["hello", "hi", "hey", "howdy", "greetings"]
    tech_keywords = ["tech", "technology", "computer", "AI", "machine learning"]

    # Recognize user's name
    if "shedrack" in user_input:
        return "Hello, Shedrack! How can I assist you today?"

    # Check for tech-related conversation
    if any(keyword in user_input for keyword in tech_keywords):
        return "Sure, let's talk about tech! What specific topic are you interested in?"

    # Greet based on time of day
    current_time = datetime.now()
    if current_time.hour < 12:
        return "Good morning!"
    elif 12 <= current_time.hour < 18:
        return "Good afternoon!"
    else:
        return "Good evening!"

    # Default response
    return "I'm sorry, I didn't catch that. Could you repeat?"

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    user_input = request.form['user_input']
    response = respond(user_input)
    speak(response)
    return render_template('index.html', response=response)

if __name__ == '__main__':
    app.run(debug=True)
