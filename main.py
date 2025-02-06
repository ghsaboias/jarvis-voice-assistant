import speech_recognition as sr
import os
import pyttsx3
import datetime
import webbrowser
import subprocess
from threading import Thread
import json
import logging
import sys

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('voice_assistant.log')
    ]
)

class MacVoiceAssistant:
    def __init__(self, wake_word="computer"):
        logging.info("Initializing Voice Assistant...")
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        try:
            self.engine = pyttsx3.init()
            logging.info("Text-to-speech engine initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize text-to-speech: {e}")
            raise
            
        self.wake_word = wake_word.lower()
        self.is_listening = True
        
        # Load configuration
        self.config = {
            "voice_speed": 180,
            "voice_id": None,
            "volume": 1.0
        }
        
        # Configure text-to-speech
        try:
            self.engine.setProperty('rate', self.config["voice_speed"])
            self.engine.setProperty('volume', self.config["volume"])
            logging.info("Text-to-speech configuration applied successfully")
        except Exception as e:
            logging.error(f"Failed to configure text-to-speech: {e}")
        
        # Adjust for ambient noise
        try:
            with self.microphone as source:
                logging.info("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source)
                logging.info("Ambient noise adjustment complete")
        except Exception as e:
            logging.error(f"Failed to adjust for ambient noise: {e}")
    
    def speak(self, text):
        """Convert text to speech"""
        logging.info(f"Speaking: {text}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logging.error(f"Failed to speak: {e}")
    
    def listen(self):
        """Listen for commands"""
        try:
            with self.microphone as source:
                logging.debug("Listening for input...")
                audio = self.recognizer.listen(source)
                logging.debug("Audio captured, attempting recognition")
                
                text = self.recognizer.recognize_google(audio).lower()
                logging.info(f"Recognized text: {text}")
                return text
        except sr.UnknownValueError:
            logging.debug("Speech not recognized")
            return ""
        except sr.RequestError as e:
            logging.error(f"Speech recognition service error: {e}")
            self.speak("Sorry, I'm having trouble with my speech recognition service.")
            return ""
        except Exception as e:
            logging.error(f"Unexpected error in listen(): {e}")
            return ""
    
    def run_system_command(self, command, args):
        """Run system command with error handling"""
        try:
            logging.info(f"Executing command: {command} with args: {args}")
            result = subprocess.run(args, capture_output=True, text=True, check=True)
            logging.debug(f"Command output: {result.stdout}")
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"Command failed with return code {e.returncode}")
            logging.error(f"Error output: {e.stderr}")
            return False
        except Exception as e:
            logging.error(f"Failed to execute command: {e}")
            return False

    def open_application(self, app_name):
        """Open macOS application with error handling"""
        logging.info(f"Attempting to open application: {app_name}")
        
        # First try using 'open' command
        success = self.run_system_command(f"open {app_name}", ["open", "-a", app_name])
        
        if not success:
            # Try alternative method using osascript
            logging.info("Trying alternative method with osascript")
            applescript = f'tell application "{app_name}" to activate'
            success = self.run_system_command(
                "osascript", 
                ["osascript", "-e", applescript]
            )
        
        if success:
            logging.info(f"Successfully opened {app_name}")
            self.speak(f"Opening {app_name}")
        else:
            logging.error(f"Failed to open {app_name}")
            self.speak(f"Sorry, I couldn't open {app_name}")
    
    def process_command(self, command):
        """Process voice commands"""
        logging.info(f"Processing command: {command}")
        logging.debug(f"Command type check - 'open' in command: {'open' in command}")
        
        if "time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The time is {current_time}")
            
        elif "open" in command:
            logging.debug("Detected 'open' command")
            if "brave" in command:
                self.open_application("Brave Browser")
            elif "safari" in command:
                self.open_application("Safari")
            elif "chrome" in command:
                self.open_application("Google Chrome")
            elif "finder" in command:
                self.open_application("Finder")
                
        elif "search" in command:
            # Handle direct searches and URL openings
            if "search for" in command:
                search_term = command.split("search for")[1].strip()
            else:
                # Try to get search term after "search"
                search_term = command.split("search")[1].strip()
                
            if search_term:
                logging.info(f"Searching for: {search_term}")
                self.speak(f"Searching for {search_term}")
                url = f"https://www.google.com/search?q={search_term.replace(' ', '+')}"
                try:
                    webbrowser.open(url)
                except Exception as e:
                    logging.error(f"Failed to open browser: {e}")
                    self.speak("Sorry, I couldn't perform the search")
            else:
                self.speak("What would you like me to search for?")
            
        elif "volume" in command:
            try:
                if "up" in command:
                    self.run_system_command(
                        "volume up",
                        ["osascript", "-e", 'set volume output volume (output volume of (get volume settings) + 10)']
                    )
                    self.speak("Volume increased")
                elif "down" in command:
                    self.run_system_command(
                        "volume down",
                        ["osascript", "-e", 'set volume output volume (output volume of (get volume settings) - 10)']
                    )
                    self.speak("Volume decreased")
            except Exception as e:
                logging.error(f"Failed to adjust volume: {e}")
                self.speak("Sorry, I couldn't adjust the volume")
                
        elif "stop listening" in command:
            logging.info("Stopping voice assistant")
            self.speak("Goodbye!")
            self.is_listening = False
            
        else:
            logging.warning(f"Unknown command: {command}")
            self.speak("I'm not sure how to help with that command")
    
    def run(self):
        """Main loop to run the assistant"""
        logging.info("Starting voice assistant")
        self.speak("Voice assistant is ready")
        logging.info(f"Wake word is set to: {self.wake_word}")
        
        while self.is_listening:
            text = self.listen()
            logging.debug(f"Received text: '{text}'")
            
            # For testing: temporarily process all commands without wake word
            if text:  # Process any non-empty text
                logging.info("Processing command without wake word (testing mode)")
                self.process_command(text)
            
            # Normal wake word behavior (commented out for testing)
            # if text.startswith(self.wake_word):
            #     command = text.replace(self.wake_word, "").strip()
            #     self.process_command(command)

def main():
    try:
        logging.info("Starting application")
        assistant = MacVoiceAssistant(wake_word="computer")
        assistant.run()
    except Exception as e:
        logging.critical(f"Application failed: {e}")
        raise

if __name__ == "__main__":
    main()