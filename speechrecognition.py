import pyttsx3
import speech_recognition as sr
import subprocess

recognizer = sr.Recognizer()
mic = sr.Microphone()

def speak(text):
    if text:
        engine = pyttsx3.init()   # re-init each time to avoid stuck queue
        engine.say(text.strip())
        engine.runAndWait()
        engine.stop()

def listen():
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
        return None
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
        return None

def chat_response(user_input):
    try:
        prompt = "Answer in one sentence: " + user_input + "\n"
        result = subprocess.run(
            ["ollama", "run", "llama3:latest"],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=10
        )
        resp = result.stdout.strip()
        if not resp:
            return "I didn't get a response."
        return resp
    except Exception as e:
        return f"Error using Ollama: {e}"

# MAIN
print("I am your AI voice assistant. How can I help you?")
while True:
    command = listen()
    if command is None:
        continue
    if "exit" in command.lower():
        speak("Goodbye!")
        break
    response = chat_response(command)
    print("AI:", response)
    speak(response)
