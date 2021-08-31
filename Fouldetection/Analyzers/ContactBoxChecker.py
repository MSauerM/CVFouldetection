from Fouldetection.DataStructures.BoundingBoxInformation import BoundingBoxInformation
from Fouldetection.Analyzers.TeamColorCalibration import TeamColorCalibration


class ContactBoxChecker:
    """
    Class for ....
    ......

    Attributes
    -----------------



    Methods
    -----------------

    """

    team_color_calibration = None
    pixel_amount_threshold = 100
    image_cache = dict()

    def __init__(self, team_color_calbration: TeamColorCalibration):
        self.team_color_calibration = team_color_calbration

    def check_for_contact(self, img, mask, boundingBox: BoundingBoxInformation):
        """

        :param img:
        :param mask:
        :param boundingBox:
        :return: True, if counted pixel for both colors are above the threshold, else False
        """
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