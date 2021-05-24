from CVUtility.BoundingBoxInformation import BoundingBoxInformation
from Fouldetection.TeamColorCalibration import TeamColorCalibration

from cv2 import cv2 as cv

class ContactBoxChecker:

    team_color_calibration = None

    # set statt list wegen besserer Performance
    image_cache = set()

    def __init__(self, team_color_calbration: TeamColorCalibration):
        self.team_color_calibration = team_color_calbration

    """
    :param img Ganzes Bild 
    :param playermask Binäre Maske der identifzierten Spieler
    :param boundingBox Bounding Box, welche zum Croppen benutzt wird
    """
    def check_for_contact(self, img, playermask, boundingBox:BoundingBoxInformation):
        # search for an image in the image_cache
        cutting_image = None
        search_item = [item for item in self.image_cache if boundingBox.get_frame_index() in item]
        if self.image_cache and search_item:
            cutting_image = search_item
        else:
            cutting_image = cv.bitwise_and(img, img , mask=playermask)
            self.image_cache.add((boundingBox.get_frame_index(), cutting_image))
        #getDimensions
        x, y, w, h = boundingBox.get_bounds()
        # crop img
        img_crop = cutting_image[y:y+h, x:x+w]
        
        # check if all team colors are contained in the img_crop
        # testen welche crop herauskommen