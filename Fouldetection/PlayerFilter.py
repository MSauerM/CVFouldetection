from BasicFramework.Frame import Frame
from Fouldetection.Filter import Filter
import cv2 as cv
import CVUtility.ImageUtility as utility

class PlayerFilter(Filter):

    def __init__(self):
        super().__init__()

    def filter(self, frame: Frame, preprocessed_frames):
        # canny Edge detection
        frame_hsv = cv.cvtColor(frame.getPixels(), cv.COLOR_BGR2HSV)
        #frame_thresh = cv.cvtColor(preprocessed_frames, cv.Color_gray2)
        #edges = cv.Canny(frame_hsv, 100, 200)


        (contours, hierarchy) = cv.findContours(preprocessed_frames, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)


        player_img = cv.bitwise_and(frame.getPixels(), frame.getPixels(), mask=preprocessed_frames)
        edges = cv.Canny(player_img, 50, 150)

        cv.imshow("player Image", player_img)
        cv.waitKey(0)
        font = cv.FONT_HERSHEY_PLAIN

        for c in contours:
            x, y, w, h = cv.boundingRect(c)
            if ( (w > 15 and h > 20) and (w < 200 and h < 200)):
                #cv.drawContours(frame, cv.boundingRect(c), -1, (255, 0, 0),3)
                cv.rectangle(frame.getPixels(), (x, y), (x+w, y+h), (255, 0, 0), 3)
                cv.putText(frame.getPixels(), "{w}/ {h}".format(w= w, h=h), (x-2, y-2), font, 0.8, (0, 255, 0), 2, cv.LINE_AA)
        cv.drawContours(frame.getPixels(), contours, -1, (0, 0, 255), 3)

        cv.imshow("Edges", edges)
        cv.imshow("Output", frame.getPixels())
        cv.waitKey(0)
