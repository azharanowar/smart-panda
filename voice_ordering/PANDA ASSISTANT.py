import speech_recognition as sr
import pyttsx3

# Initialize the speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 0.9)  # Volume level

def speak(text):
    """Converts text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen(greet):
    """Listens for voice input and converts it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        if greet:
            speak("Hello, I am Panda. Your voice assistant.")
        else:
            speak("how I can assist you.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, could you please repeat?")
        return None
    except sr.RequestError:
        speak("There seems to be an issue with the speech recognition service.")
        return None

def handle_command(command):
    """Handles voice commands specific to restaurant management."""
    if command:
        if "menu" in command:
            speak("Here is today's menu. We have pasta, burgers, and pizza.")
        elif "reservation" in command:
            speak("Please provide the name and time for the reservation.")
        elif "bill" in command:
            speak("Sure, generating the bill for you.")
        elif "order" in command:
            speak("What would you like to order?")
        elif "exit" in command or "quit" in command:
            speak("Thank you for using the system. Goodbye!")
            return False
        else:
            speak("I'm sorry, I didn't understand your command.")
    return True

# Main loop
if __name__ == "__main__":
    speak("Welcome to Panda restaurant management system!")
    running = True
    first_interaction = True  # To track if it's the first interaction
    while running:
        user_command = listen(first_interaction)
        first_interaction = False  # After the first interaction, stop greeting
        running = handle_command(user_command)
