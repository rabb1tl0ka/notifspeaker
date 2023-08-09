# Notification Speech Reader

notifspeaker.py is a versatile Python program designed to enhance your Linux desktop experience by seamlessly integrating speech synthesis for notifications. This lightweight and user-friendly tool empowers you to listen for notification alerts using various speech synthesis engines, including AWS Polly, espeak, and say.

## Features


- **Cross-Speech Synthesis Engine Compatibility:** Support for multiple speech synthesis engines, allowing you to choose the one that best suits your preferences and system setup.

- **Notification Queueing:** Bye bye overlapping notifications that create chaos. notifspeaker.py queues incoming notifications no matter how fast they come your way.

- **Notification Skipping:** Take control of your workflow. Choose to bypass lengthy notifications with notifspeaker.py. Maintain uninterrupted efficiency by effortlessly skipping long notifications.

- **Selective Notification Filtering:** Stay focused! notifspeaker.py empowers you to cherry-pick which notification summaries and body text to exclude. Tailor your experience to focus on what truly matters.

- **Customizable Alerts:** Easily configure the speech rate, pitch, volume, and language to ensure notifications are delivered just the way you want them.

- **Efficient and Lightweight:** Designed with efficiency in mind, ensuring minimal resource consumption by even removing any mp3 files created (eg. in the case of Polly) after it is done playing them.

- **Open-Source and Extendable:** Help make it better by contributing and expanding this from Linux to other OS.


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
   slack_server_names = slackserver_name1, slackserver_name2
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

## Usage

Run the program using the following command:

```
python3 notifspeaker.py polly
```

**Notes**: Change python3 for the python version installed on your system.


## Contributing

Contributions are welcome! If you find a bug or want to suggest an improvement, please create an issue or submit a pull request.

## License

This project is licensed under the MIT License.