
class ContactEvent:
    frameCountBegin = -1
    frameCountEnd = -1
    isFoul = False

    def __init__(self, frameCountBegin, frameCountEnd):
        self.frameCountBegin = frameCountBegin
        self.frameCountEnd = frameCountEnd

