import os
import configparser
import argparse
import dbus
import subprocess
import threading
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop
import queue
from pynput import keyboard
import pygame
import os
import hashlib

ignore_notif_summary = [] # array of summary strings to ignore
ignore_notif_from = [] # array of origin strings to ignore
notification_queue = queue.Queue()  # Queue to hold notification strings
slack_server_names = None

def hash_string(input_string):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_string.encode('utf-8'))
    return sha256_hash.hexdigest()

def play_mp3(mp3file):
    # Play the generated MP3 file
    pygame.mixer.init()
    pygame.mixer.music.load(mp3file)
    pygame.mixer.music.play()

    # Wait for playback to finish
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Delete the file after playback
    os.remove(mp3file)

lastmsg_summary = ""

def msg_cb(bus, msg):
    # Don't try to print 'msg'. It's impossible and it will break the program.
    if msg.get_interface() == 'org.freedesktop.Notifications' and msg.get_member() == 'Notify':
        args = msg.get_args_list()

        # If there's no PID then just forget about it. Read this in NYC Mafia style tone for extra impact.
        pid = args[6].get("sender-pid")
        if pid == None:
            return

        notification_from = args[0]
        summary = args[3]
        body = args[4]

        global ignore_notif_summary
        if summary in ignore_notif_summary:
            return
        
        global ignore_notif_from
        if notification_from in ignore_notif_from:
            return
        
        if args[6].get("x-shell-sender") != None:
            print(f"Notification is from x-shell-sender, likely a duplicate. Detail [{summary}: {body}]")
            return
        
        print(f"PID: {pid}\nF: {notification_from}\nS: {summary}\nB: {body}")

        global slack_server_names
        global lastmsg_summary

        if notification_from == "Slack":
            for slack_server in slack_server_names:
                slack_server_from = f"[{slack_server}] from "
                slack_server_in = f"[{slack_server}] in "

                if slack_server_from in summary:
                    summary = summary.replace(slack_server_from, "").strip()
                    
                elif slack_server_in in summary:
                    summary = summary.replace(slack_server_in, "").strip()

                if lastmsg_summary != summary: 
                    notification_str = f"{summary} says: {body}"
                else:
                    notification_str = body
                    
                
        elif "Spotify" in notification_from:
            notification_str = f"You are listening to {body} {summary}"
        elif "calendar.google.com" in body:
            notification_str = f"{summary} is coming up! From {body}"
        elif "mail.google.com" in body:
            # Google Chat
            body = body.replace("mail.google.com", "").strip()
            notification_str = f"{summary} says: {body}"
        else:
            notification_str = f"{body} via {notification_from} {summary}."


        # Put the notification string in the queue
        notification_queue.put(notification_str)

        # saving last summary
        lastmsg_summary = args[3]


def process_notification(notification_str, speechapp):
    mp3filename = ""

    if speechapp == "say":
        speak_command = ["say", notification_str]
    elif speechapp == "polly":
        mp3filename = hash_string(notification_str) + "output.mp3"
        
        speak_command = [
            'aws', 'polly', 'synthesize-speech',
            '--output-format', 'mp3',
            '--text', notification_str,
            '--voice-id', voice_id,
            mp3filename
        ]
    elif speechapp == "espeak":
        espeak_parameters = ["-s", "200", "-g", "2", "-p", "40"]
        speak_command = ["espeak", *espeak_parameters, notification_str]

    print(f"opening a subprocess: {speak_command}")
    speak_process = subprocess.Popen(
        speak_command,
        stdout=subprocess.DEVNULL,  # Suppress stdout
        stderr=subprocess.DEVNULL   # Suppress stderr
    )

    # Create a keyboard listener to detect when the ESC key is pressed
    def on_press(key):
        if key == keyboard.Key.esc:
            print("Reader interrupt!")
            if speechapp == "polly":
                # There's no thread here. Just stop the mp3 player.
                print("Stopping polly player")
                pygame.mixer.music.stop()
            else:
                print("Terminate the speak process if the ESC key is pressed")
                # Terminate the speak process if the ESC key is pressed
                speak_process.terminate()
                speak_process.wait()

    # Start the keyboard listener in a separate thread
    keyboard_listener = keyboard.Listener(on_press=on_press)
    keyboard_listener.start()

    # Wait for the speak process to finish
    # so we don't play more than 1 notification at a time.
    print("waiting for the speak process to finish")
    speak_process.wait()

    if speechapp == "polly":
        # In the case of polly, the speak_process just creates the mp3 file. 
        # now we have to play it!
        play_mp3(mp3filename)

    print("Stopping the keyboard listener")
    keyboard_listener.stop()

    print("process_notification done")

def speak_processor(speechapp):
    while True:
        try:
            # Get the notification string from the queue
            notification_str = notification_queue.get(timeout=1)  # Timeout to avoid blocking indefinitely
            # Process the notification
            process_notification(notification_str, speechapp)
            # Mark the task as done in the queue
            notification_queue.task_done()
        except queue.Empty:
            # If the queue is empty, sleep for a short duration
            # to avoid busy waiting
            pass
    

def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')

    global slack_server_names
    slack_server_names = config.get('Settings', 'slack_server_names').split(', ')
    print(slack_server_names)

    global ignore_notif_summary
    ignore_notif_summary = config.get('Settings', 'ignore_notif_summary').split(', ')
    print(ignore_notif_summary)

    global ignore_notif_from
    ignore_notif_from = config.get('Settings', 'ignore_notif_from').split(', ')
    print(ignore_notif_from)

    global voice_id 
    voice_id= config.get('Settings', 'voice_id', fallback="Brian")


def main(speechapp):
    read_config()

    DBusGMainLoop(set_as_default=True)
    bus = dbus.SessionBus()

    obj_dbus = bus.get_object('org.freedesktop.DBus',
                              '/org/freedesktop/DBus')

    obj_dbus.BecomeMonitor(["interface='org.freedesktop.Notifications'"],
                           dbus.UInt32(0),
                           interface='org.freedesktop.Notifications')

    bus.add_message_filter(msg_cb)

    # Start the speak thread to process the notification queue
    speak_thread = threading.Thread(target=speak_processor, args=(speechapp,), daemon=True)
    speak_thread.start()

    mainloop = GLib.MainLoop()
    mainloop.run()
    print("Done")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Read notifications using espeak or say.')
    parser.add_argument(
        'speechapp',
        choices=['espeak', 'say', 'polly'],
        nargs='?',
        default='polly',
        help='Choose the speech synthesis utility (espeak, say, or Amazon Polly). Default is polly.'
    )
    args = parser.parse_args()

    main(args.speechapp)
