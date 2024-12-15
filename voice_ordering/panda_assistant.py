import speech_recognition as sr
import pyttsx3
import frontEnd.frontend as frontend_management
import utilities.common as common
import user_authentication.user_auth as user_auth_system

class PandaAssistant:
    def __init__(self):
        # Initialize the speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Speed of speech
        self.engine.setProperty('volume', 0.9)  # Volume level
        self.frontend = frontend_management.Frontend()

    def speak(self, text):
        """Converts text to speech and shows it as text."""
        print(f"Assistant: {text}")  # Display text while speaking
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self, greet=True):
        """Listens for voice input and converts it to text."""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            if greet:
                self.speak("How can I help you today?")
            else:
                self.speak("How can I help you today?")
            
            # Adjust for ambient noise and increase the energy threshold for distance listening
            recognizer.adjust_for_ambient_noise(source, duration=1)
            recognizer.energy_threshold = 4000  # Increase threshold for better distance listening
            
            # Listen for a long time (set timeout to 10 seconds)
            try:
                audio = recognizer.listen(source, timeout=10)
                command = recognizer.recognize_google(audio)
                print(f"You said: {command}")
                return command.lower()
            except sr.UnknownValueError:
                self.speak("Sorry, I didn't catch that. Could you please repeat?")
                return None
            except sr.RequestError:
                self.speak("There seems to be an issue with the speech recognition service.")
                return None
            except sr.WaitTimeoutError:
                self.speak("Listening timed out. Please try again.")
                return None

    def handle_command(self, command):
        """Handles voice commands specific to restaurant management."""
        import app
        if command:
            if "menu" in command:
                self.speak("Redirecting you to available menu page...")
                common.clear_console()
                common.loading_message_with_delay("Redirecting you to available menu page...", color='green')
                common.clear_console()
                self.frontend.new_order()

                common.wait_for_keypress()
                app.main() # Returning to main menu from here
            elif "place an order" in command or "order" in command:
                self.speak("What would you like to order? Redirecting to order page")
                common.clear_console()
                common.loading_message_with_delay("Redirecting you to available menu page...", color='green')
                common.clear_console()
                self.frontend.new_order()

                common.wait_for_keypress()
                app.main() # Returning to main menu from here

            elif "view my orders" in command or "view" in command:
                self.speak("Redirecting to your orders page")
                common.clear_console()
                common.loading_message_with_delay("Redirecting to your orders page...", color='green')
                common.clear_console()
                self.frontend.view_my_orders()

                common.wait_for_keypress()
                app.main() # Returning to main menu from here
            elif "update" in command:
                self.speak("Redirecting to your order update page")
                common.clear_console()
                common.loading_message_with_delay("Redirecting to your order update page...", color='green')
                common.clear_console()
                self.frontend.update_order()

                common.wait_for_keypress()
                app.main() # Returning to main menu from here
            elif "cancel" in command:
                self.speak("Redirecting to your order cancel page")
                common.clear_console()
                common.loading_message_with_delay("Redirecting to your order cancel page...", color='green')
                common.clear_console()
                self.frontend.cancel_order()

                common.wait_for_keypress()
                app.main() # Returning to main menu from here
                
            elif "exit" in command or "quit" in command:
                self.speak("Thank you for using Panda Restaurant Management System. Goodbye!")

                common.wait_for_keypress()
                app.main() # Returning to main menu from here
                return False  # Exit the loop
            else:
                self.speak("I'm sorry, I didn't understand your command.")
        return True

    def starting(self):
        """Main loop for the assistant."""
        self.speak("Welcome to Smart Panda Restaurant Management System!")
        running = True
        first_interaction = True  # To track if it's the first interaction
        while running:
            user_command = self.listen(first_interaction)
            first_interaction = False  # After the first interaction, stop greeting
            running = self.handle_command(user_command)
