import logging
import speech_recognition as sr
import pyttsx3
from src.commands.command_parser import CommandParser
from src.browser.brave_controller import BraveController


class MacVoiceAssistant:
    def __init__(self, wake_word="jarvis"):
        logging.info("Initializing Voice Assistant...")
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.wake_word = wake_word.lower()
        self.is_listening = True
        self.command_parser = CommandParser()
        self.brave = BraveController()
        self._init_text_to_speech()
        self._adjust_for_ambient_noise()

    def _init_text_to_speech(self):
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", 180)
            self.engine.setProperty("volume", 1.0)
            logging.info("Text-to-speech engine initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize text-to-speech: {e}")
            raise

    def _adjust_for_ambient_noise(self):
        try:
            with self.microphone as source:
                logging.info("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source)
                logging.info("Ambient noise adjustment complete")
        except Exception as e:
            logging.error(f"Failed to adjust for ambient noise: {e}")

    def speak(self, text: str) -> None:
        logging.info(f"Speaking: {text}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logging.error(f"Failed to speak: {e}")

    def listen(self) -> str:
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

    def process_command(self, command: str) -> None:
        logging.info(f"Processing command: {command}")
        command_type, parameter = self.command_parser.normalize_command(command)

        try:
            if command_type == "navigation":
                if self.brave.navigate_to(parameter):
                    self.speak(f"Opening {parameter}")
                else:
                    self.speak(f"Sorry, I couldn't navigate to {parameter}")

            elif command_type == "search":
                if parameter:
                    if self.brave.search(parameter):
                        self.speak(f"Searching for {parameter}")
                    else:
                        self.speak("Sorry, I couldn't perform the search")
                else:
                    self.speak("What would you like me to search for?")

            elif command_type == "new_tab":
                if self.brave.new_tab():
                    self.speak("Opening new tab")
                else:
                    self.speak("Sorry, I couldn't open a new tab")

            elif command_type == "close_tab":
                if self.brave.close_tab():
                    self.speak("Closing tab")
                else:
                    self.speak("Sorry, I couldn't close the tab")

            elif command_type == "stop":
                self.speak("Goodbye!")
                self.is_listening = False

            elif command_type == "youtube_search":
                if parameter:
                    if self.brave.youtube_search(parameter):
                        self.speak(f"Searching YouTube for {parameter}")
                    else:
                        self.speak("Sorry, I couldn't search YouTube")
                else:
                    self.speak("What would you like to search for on YouTube?")

            elif command_type == "youtube_select":
                try:
                    position = int(parameter)
                    if self.brave.select_youtube_result(position):
                        self.speak(f"Playing video {parameter}")
                    else:
                        self.speak("Sorry, I couldn't play that video")
                except ValueError:
                    self.speak("I didn't understand which video to play")

            else:
                self.speak("I'm not sure how to help with that command")

        except Exception as e:
            logging.error(f"Error processing command: {e}")
            self.speak("Sorry, I encountered an error processing that command")

    def run(self) -> None:
        logging.info("Starting voice assistant")
        self.speak("Jarvis is ready")
        logging.info(f"Wake word is set to: {self.wake_word}")

        while self.is_listening:
            text = self.listen()
            if text.startswith(self.wake_word):
                command = text.replace(self.wake_word, "").strip()
                logging.info(f"Wake word detected, processing command: {command}")
                self.process_command(command)
