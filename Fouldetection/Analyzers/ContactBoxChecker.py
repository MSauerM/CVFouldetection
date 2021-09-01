from Fouldetection.DataStructures.BoundingBoxInformation import BoundingBoxInformation
from Fouldetection.Analyzers.TeamColorCalibration import TeamColorCalibration


class ContactBoxChecker:
    """
    Class for checking if a certain bounding box contains multiple players of different
    teams and is relevant because of this
    ......

    Attributes
    -----------------
        team_color_calibration : TeamColorCalibration
            instance of the color calibration to get the main colors of the two contending
            teams
        pixel_amount_threshold
            specified amount of pixels, which has to be exceeded by both team colors
            inside a bounding box, to have a relevant contact bounding box

    Methods
    -----------------
        check_for_contact(img, mask, boundingBox)
            checks the given boundingBox based on img and mask for the relevant amount
            of pixels for both team colors
    """

    team_color_calibration = None
    pixel_amount_threshold = 100
    #image_cache = dict()

    def __init__(self, team_color_calbration: TeamColorCalibration):
        self.team_color_calibration = team_color_calbration

    def check_for_contact(self, img, mask, boundingBox: BoundingBoxInformation):
        x, y, w, h = boundingBox.get_bounds()
        # crop img & mask
        img_crop = img[y:y+h, x:x+w] #cutting_image[y:y+h, x:x+w]
        mask_crop = mask[y:y+h, x:x+w]
        # check if all team colors are contained in the img_crop
        first_color = self.team_color_calibration.colors_list[0]
        second_color = self.team_color_calibration.colors_list[1]

        pixel_count_one = self.team_color_calibration.count_hue_pixel(img_crop, first_color[0], 15)
        pixel_count_two = self.team_color_calibration.count_hue_pixel(img_crop, second_color[0], 15)

        if pixel_count_one > self.pixel_amount_threshold and pixel_count_two > self.pixel_amount_threshold:
            return True
        else:
            return False