from BasicFramework.Sequence import Sequence
from Fouldetection.DataStructures.BoundingBoxInformationChain import BoundingBoxInformationChain


class ContactEvent:
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
        #print("Here goes something with the information about a contact event")
        return """ 
        sequence_info = {info}
        isFoul= {isFoul}
        Wahrscheinlichkeiten = {foul_probabilities}
        \n""".format(info= str(self.sequence),isFoul=self.isFoul, foul_probabilities = self.foul_probabilities)

    def __repr__(self):
        return self.__str__()
