import subprocess

def send_notification(title, message):
    try:
        subprocess.run(['notify-send', title, message])
        print("Notification sent successfully.")
    except FileNotFoundError:
        print("Error: 'notify-send' command not found. Make sure libnotify-bin package is installed.")

if __name__ == "__main__":
    title = "Test Notification"
    message = "This is a test notification sent via D-Bus."
    send_notification(title, message)

