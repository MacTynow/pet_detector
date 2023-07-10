from Classifier import Classifier
import time
import pyttsx3
import os
import http.client
import urllib


tts_engine = pyttsx3.init()
time_since_last_detection = [0]
announcement_timeout_seconds = 10


def found_item_callback(label, confidence, coordinates):
    """Callback function for when an item is found"""
    print('{} found, {} confident'.format(label, confidence))
    current_time = int(time.time())
    if (current_time - time_since_last_detection[0]) > announcement_timeout_seconds:
        announce_item_found(label)
        send_push_notification_item_found(label)
        time_since_last_detection[0] = int(time.time())


def announce_item_found(label):
    """Announce out loud that an item was found"""
    speech = "There's a {} at the door.".format(label)
    cmd = 'say "{}"'.format(speech)
    os.system(cmd)


def send_push_notification_item_found(label):
    """Send a push notification that an item was found"""
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
                 urllib.parse.urlencode({
                     "token": os.environ['PUSHOVER_TOKEN'],
                     "user": os.environ['PUSHOVER_USER'],
                     "message": "There's a {} at the door.".format(label),
                 }), {"Content-type": "application/x-www-form-urlencoded"})
    conn.getresponse()


def main():
    """Run the application"""
    c = Classifier()
    try:
        allowed_labels = [
            'dog',
            'cat',
        ]
        c.set_allowed_labels(allowed_labels)
        c.set_callback_item_found(found_item_callback)
        c.classify_from_live_stream()
    except KeyboardInterrupt:
        print('Exiting...')


if __name__ == '__main__':
    main()
