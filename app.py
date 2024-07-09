from flask import Flask, render_template, request
import pyttsx3
import speech_recognition as sr

app = Flask(__name__)
engine = pyttsx3.init()  # Initialize once

# Function to speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

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
    
    if any(greeting in user_input for greeting in greetings):
        return "Hello!"
    else:
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
