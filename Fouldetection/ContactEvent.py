from BasicFramework.Sequence import Sequence


class ContactEvent:
    sequence: Sequence = None
    isFoul = False

    def __init__(self, sequence:Sequence):
       self.sequence = sequence

    def __str__(self):
        print("Here goes something with the information about a contact event")

    def __repr__(self):
        return self.__str__()
