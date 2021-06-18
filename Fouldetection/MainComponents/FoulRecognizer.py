from Fouldetection.ContactEvent import ContactEvent


class FoulRecognizer:

    def __init__(self):
        print("FoulRecognizer")

    def analyze(self, contact_events: ContactEvent):
        print("Checking for possible fouls")