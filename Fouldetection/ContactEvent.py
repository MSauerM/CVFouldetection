
class ContactEvent:
    frameCountBegin = -1
    frameCountEnd = -1
    isFoul = False
    # involved PlayerBoundingBox
    # sequence which is the corresponding one to this event

    def __init__(self, frameCountBegin, frameCountEnd):
        self.frameCountBegin = frameCountBegin
        self.frameCountEnd = frameCountEnd

    def __str__(self):
        print("Here goes something with the information about a contact event")

    def __repr__(self):
        return self.__str__()
