# Notification Speech Reader

This is a Python program that reads out notifications using speech synthesis on Linux.
It supports AWS Polly, espeak and say.

## Features

- Reads out incoming notifications using speech synthesis.
- Choose between espeak and say for speech synthesis
- Press ESC if you can to stop reading the notification (good for long notifications...)
- Ignore notifications based on a summary list
- Support AWS Polly. It saves an mp3 file in the local folder so no need to use an S3 bucket!


## Installation

1. Ensure you have Python and pip installed on your system.

2. Clone this repository:

   ```
   git clone https://github.com/rabb1tl0ka/notifspeaker.git
   ```

3. Navigate to the cloned directory:

   ```
   cd notifspeaker
   ```

4. Install the required Python dependencies:

   ```
   pip install -r requirements.txt
   ```

5. Create a config.ini file

   ```
   [Settings]
   ignore_notif_summary = some summary, another summary
   ignore_notif_from = Spotify
   polly_voice_id = "Brian"
   ```
6. If you want to use AWS Polly (https://aws.amazon.com/polly/)

   You have to install AWS CLI and then create a user, give it access to AWS Polly and also access keys.

   Here's an example:

   ```
   aws configure

   AWS Access Key ID [****************SYUH]: 
   AWS Secret Access Key [****************vPA4]: 
   Default region name [eu-west-1]: 
   Default output format [JSON]: None
   ```

   After you run aws configure, you have to 

## Usage

Run the program using the following command:

```
python3 main.py polly 
```

**Notes**: Change python3 for the python version installed on your system.


## Contributing

Contributions are welcome! If you find a bug or want to suggest an improvement, please create an issue or submit a pull request.

## License

This project is licensed under the MIT License.