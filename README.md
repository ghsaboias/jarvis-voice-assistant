# Mac Voice Assistant

This project is a simple voice assistant designed for macOS. It uses speech recognition and text-to-speech to interact with your computer. The assistant can perform tasks such as:

- Opening new tabs in Brave Browser
- Navigating to websites
- Performing web searches using your default search engine
- Searching YouTube directly
- Managing browser tabs
- Logging activity for debugging purposes

## Project Structure

```
mac-voice-assistant/
├── src/                      # Source code
│   ├── browser/             # Browser control
│   │   ├── __init__.py
│   │   └── brave_controller.py
│   ├── commands/            # Command parsing
│   │   ├── __init__.py
│   │   └── command_parser.py
│   ├── handlers/            # System interactions
│   │   ├── __init__.py
│   │   └── apple_script_handler.py
│   └── voice/              # Voice assistant core
│       ├── __init__.py
│       └── voice_assistant.py
├── main.py                  # Entry point
├── requirements.txt         # Dependencies
├── USER_FLOWS.md           # Command documentation
└── voice_assistant.log     # Activity logs
```

## Requirements

- **Operating System:** macOS
- **Python Version:** 3.11 or higher
- **Browser:** Brave Browser

### Python Dependencies

Install the required Python packages using:

```bash
pip install -r requirements.txt
```

## Running the Voice Assistant

To start the voice assistant:

```bash
python main.py
```

## Usage

The assistant responds to voice commands prefixed with the wake word "Jarvis". See `USER_FLOWS.md` for a complete list of available commands and their variations.

Example commands:

- "Jarvis navigate to youtube"
- "Jarvis search python tutorials"
- "Jarvis youtube search cats"
- "Jarvis new tab"
- "Jarvis close tab"

## Configuration

The assistant is configured through several components:

- `CommandTriggers`: Defines command patterns
- `BraveController`: Manages browser interactions
- `MacVoiceAssistant`: Core assistant functionality

## Logging

The assistant logs to both console and `voice_assistant.log`, including:

- Command processing
- Speech recognition
- Error handling
- System interactions

## Notes

- Uses AppleScript for system interaction
- Requires microphone access
- Network connection needed for speech recognition
- Brave Browser must be installed

## Troubleshooting

- **Speech Recognition Issues:** Check microphone and network connection
- **Browser Control:** Ensure Brave Browser is installed and accessible
- **Permission Issues:** Grant necessary system permissions
- **Import Errors:** Verify all dependencies are installed

## License

This project is open-source. Feel free to modify and distribute it.
