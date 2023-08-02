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

ignore_notif_summary = [] # array of summary strings to ignore

notification_queue = queue.Queue()  # Queue to hold notification strings

def msg_cb(bus, msg):
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
            print(f"!ignoring {summary}")
            return

        if notification_from == "Slack":
            summary = summary.replace("[lokahq] from ", "").strip()
            notification_str = f"{summary} says. {body}"
        if "Spotify" in notification_from:
            notification_str = f"You are listening to {body} {summary}"
        if "google.calendar.com" in body:
            body = body.replace("calendar.google.com").strip()
        else:
            notification_str = f"via {notification_from}. {summary}. {body}"

        print(f"PID: {pid}\nF: {notification_from}\nS: {summary}\nB: {body}")

        # Put the notification string in the queue
        notification_queue.put(notification_str)

def process_notification(notification_str, speechapp):
    if speechapp == "say":
        speak_command = ["say", notification_str]
    elif speechapp == "espeak":
        espeak_parameters = ["-s", "200", "-g", "2", "-p", "40"]
        speak_command = ["espeak", *espeak_parameters, notification_str]

    speak_process = subprocess.Popen(speak_command)

    # Create a keyboard listener to detect when the ESC key is pressed
    def on_press(key):
        if key == keyboard.Key.esc:
            # Terminate the speak process if the ESC key is pressed
            speak_process.terminate()
            speak_process.wait()

    # Start the keyboard listener in a separate thread
    keyboard_listener = keyboard.Listener(on_press=on_press)
    keyboard_listener.start()

    # Wait for the speak process to finish
    # so we don't play more than 1 notification at a time.
    speak_process.wait()

    keyboard_listener.stop()

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
    # Check if the config file exists
    if os.path.exists('config.ini'):
        # Read the config file
        config = configparser.ConfigParser()
        config.read('config.ini')

    global ignore_notif_summary
    # Get the string array from the config file and assign it to the global variable
    ignore_notif_summary = config.get('Settings', 'ignore_notif_summary').split(', ')
    print(ignore_notif_summary)

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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Read notifications using espeak or say.')
    parser.add_argument('speechapp', choices=['espeak', 'say'], help='Choose the speech synthesis utility (espeak or say).')
    args = parser.parse_args()

    main(args.speechapp)
