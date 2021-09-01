from BasicFramework.Sequence import Sequence
from Fouldetection.DataStructures.BoundingBoxInformationChain import BoundingBoxInformationChain


class ContactEvent:
    """
    Class for aggregating information about a contact
    ......

    Attributes
    -----------------
        sequence
            the corresponding sequence instance
        bounding_box_chain
            the corresponding bounding box chaing
        isFoul
            flag for the decision foul or no foul
        foul_probabilities
            percentage dictionary for 0 (no foul) and 1 (foul)

    Methods
    -----------------

    """
    sequence: Sequence = None
    bounding_box_chain: BoundingBoxInformationChain = None
    isFoul = None
    foul_probabilities = None

    def __init__(self, sequence: Sequence, bounding_box_chain: BoundingBoxInformationChain):
        self.sequence = sequence
        self.bounding_box_chain = bounding_box_chain
        self.isFoul = False
        self.foul_probabilities = {0: 0.00,   # stands for fair
                                   1: 0.00}   # stands for foul

    def __str__(self):
        return """ 
        sequence_info = {info}
        isFoul= {isFoul}
        probabilities = {foul_probabilities}
        """.format(info= str(self.sequence),isFoul=self.isFoul, foul_probabilities = self.foul_probabilities)

    def __repr__(self):
        return self.__str__()
