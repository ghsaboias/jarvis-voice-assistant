import logging
import sys
from src.voice.voice_assistant import MacVoiceAssistant

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("voice_assistant.log"),
    ],
)


def main():
    try:
        logging.info("Starting application")
        assistant = MacVoiceAssistant(wake_word="jarvis")
        assistant.run()
    except Exception as e:
        logging.critical(f"Application failed: {e}")
        raise


if __name__ == "__main__":
    main()
