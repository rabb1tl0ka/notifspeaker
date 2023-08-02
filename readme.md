# Notification Speech Reader

This is a Python program that reads out notifications using speech synthesis on Linux.

## Features

- Reads out incoming notifications using speech synthesis.
- Choose between espeak and say for speech synthesis
- Press ESC if you can to stop reading the notification (good for long notifications...)
- Ignore notifications based on a summary list


## Installation

1. Ensure you have Python and pip installed on your system.

2. Clone this repository:

   ```
   git clone https://github.com/rabb1tl0ka/notification-speech-reader.git
   ```

3. Navigate to the cloned directory:

   ```
   cd notification-speech-reader
   ```

4. Install the required Python dependencies:

   ```
   pip install -r requirements.txt
   ```

   **Note**: The program also relies on external command-line utilities `espeak` and `festival` for speech synthesis. Make sure these utilities are installed on your system.

## Usage

Run the program using the following command:

```
python3 main.py say
```

or

```
python3 main.py espeak
```

**Notes**: Change python3 for the python version installed on your system.
    
Create a config.ini file if you want to configure the summaries to be ignored.

```
[Settings]
ignore_notif_summary = summary1, summary2
```

## Contributing

Contributions are welcome! If you find a bug or want to suggest an improvement, please create an issue or submit a pull request.

## License

This project is licensed under the MIT License.