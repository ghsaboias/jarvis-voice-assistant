# Mac Voice Assistant

This project is a simple voice assistant designed for macOS. It uses speech recognition and text-to-speech to interact with your computer. The assistant can perform tasks such as:

- Telling the current time
- Opening applications (e.g., Brave Browser, Safari, Google Chrome, Finder)
- Performing web searches using your default browser
- Adjusting system volume via AppleScript
- Logging activity for debugging purposes

## Requirements

- **Operating System:** macOS
- **Python Version:** 3.6 or higher

### Python Libraries

- `speech_recognition`
- `pyttsx3`
- `pyaudio` *(or an alternative for handling audio input)*
- Standard libraries: `datetime`, `webbrowser`, `subprocess`, etc.

## Installation

Install the required Python packages using:

```bash
pip install speechrecognition pyttsx3 pyaudio
```

*Note: You might need to use `pip3` instead of `pip` depending on your system configuration.*

## Running the Voice Assistant

To start the voice assistant, simply run the following command in your terminal:

```bash
python main.py
```

*Note: Replace `python` with `python3` if necessary.*

## Configuration

The main configuration for the assistant is located in the `MacVoiceAssistant` class within `main.py`. You can adjust parameters such as:

- **Wake Word:** Default is `"computer"`.
- **Voice Speed:** Controlled by the `voice_speed` setting.
- **Volume:** Controlled by the `volume` setting.
- **Voice ID:** Change the TTS voice if desired.

During startup, the assistant adjusts for ambient noise and begins listening for commands. For testing purposes, all non-empty voice input is processed without requiring the wake word.

## Logging

The assistant logs detailed information to both the console and a file named `voice_assistant.log`. These logs include debugging, error messages, and activity details.

## Notes

- This assistant is tailor-made for macOS and uses system-specific scripts (e.g., `osascript`) to control applications and adjust volume.
- Make sure your microphone is connected and properly configured.
- If you encounter issues with voice recognition or text-to-speech, check your network connection and library installations.

## Troubleshooting

- **Microphone Issues:** Ensure your microphone is working and accessible.
- **Text-to-Speech Problems:** Verify that `pyttsx3` is installed and properly configured.
- **Application Launch Failures:** Confirm that the application names in your voice commands match those recognized by the assistant.
- **Volume Control:** The volume adjustment uses AppleScript, so ensure your system permits these operations.

## License

This project is open-source. Feel free to modify and distribute it.