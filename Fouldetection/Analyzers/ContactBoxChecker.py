from Fouldetection.DataStructures.BoundingBoxInformation import BoundingBoxInformation
from Fouldetection.Analyzers.TeamColorCalibration import TeamColorCalibration


class ContactBoxChecker:

    team_color_calibration = None
    pixel_amount_threshold = 100#100 #200
    # set statt list wegen besserer Performance
    #image_cache = set()
    image_cache = dict()

    def __init__(self, team_color_calbration: TeamColorCalibration):
        self.team_color_calibration = team_color_calbration

    """
    :param img Ganzes Bild 
    :param playermask Binäre Maske der identifzierten Spieler
    :param boundingBox Bounding Box, welche zum Croppen benutzt wird
    """
    def check_for_contact(self, img, mask, boundingBox: BoundingBoxInformation):
        #def check_for_contact(self, img, playermask, boundingBox:BoundingBoxInformation):
        # search for an image in the image_cache
       # cutting_image = None
       # search_item = boundingBox.get_frame_index() #[item for item in self.image_cache if boundingBox.get_frame_index() in item]
       # if self.image_cache and search_item in self.image_cache:
       #     cutting_image = self.image_cache[search_item]#search_item
       # else:
        #    cutting_image = cv.bitwise_and(img, img , mask=playermask)
        #    #self.image_cache.add((boundingBox.get_frame_index(), tuple(cutting_image)))
        #    self.image_cache[boundingBox.get_frame_index()] = cutting_image
        #getDimensions
        x, y, w, h = boundingBox.get_bounds()
        # crop img & mask
        img_crop = img[y:y+h, x:x+w] #cutting_image[y:y+h, x:x+w]
        mask_crop = mask[y:y+h, x:x+w]
        # downsampling of img_crop (maybe for better performance)
        #utility.showResizedImage("Crop", img_crop, 0.4)

        #colorHistogram = ColorHistogram(img_crop, mask_crop)
        #colorHistogram.show_histogram()

        # check if all team colors are contained in the img_crop
        first_color = self.team_color_calibration.colors_list[0]
        second_color = self.team_color_calibration.colors_list[1]

        pixel_count_one = self.team_color_calibration.count_hue_pixel(img_crop, first_color[0], 15)
        pixel_count_two = self.team_color_calibration.count_hue_pixel(img_crop, second_color[0], 15)

        #pixel values anpassen an downgesampelte pixelmenge
        if pixel_count_one > self.pixel_amount_threshold and pixel_count_two > self.pixel_amount_threshold:
            #utility.showResizedImage("Crop", img_crop, 0.4)
            return True
        else:
            return False