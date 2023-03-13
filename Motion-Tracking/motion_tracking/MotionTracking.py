import numpy as np
import cv2
import sys
from typing import List, Union, Tuple


class MotionTracking:
    def __init__(self, video_source: str, BGS_TYPE: str):
        self.cap = cv2.VideoCapture(video_source)
        self.minArea = 250
        self.bg_subtractor = self.getBGSubtractor(BGS_TYPE)

    def set_video_source(self, video_source: str):
        self.cap = cv2.VideoCapture(video_source)

    def getKernel(self, KERNEL_TYPE: str) -> List[List[int]]:
        if KERNEL_TYPE == "dilation":
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        if KERNEL_TYPE == "opening":
            kernel = np.ones((3, 3), np.uint8)
        if KERNEL_TYPE == "closing":
            kernel = np.ones((3, 3), np.uint8)

        return kernel

    def getFilter(self, img: List[List[int]], filter: str) -> List[List[int]]:
        if filter == 'closing':
            return cv2.morphologyEx(img, cv2.MORPH_CLOSE,
                                    self.getKernel("closing"), iterations=2)

        if filter == 'opening':
            return cv2.morphologyEx(img, cv2.MORPH_OPEN,
                                    self.getKernel("opening"), iterations=2)

        if filter == 'dilation':
            return cv2.dilate(img, self.getKernel("dilation"), iterations=2)

        if filter == 'combine':
            closing = cv2.morphologyEx(
                img, cv2.MORPH_CLOSE, self.getKernel(
                    "closing"), iterations=2)
            opening = cv2.morphologyEx(
                closing, cv2.MORPH_OPEN, self.getKernel(
                    "opening"), iterations=2)
            dilation = cv2.dilate(opening, self.getKernel(
                "dilation"), iterations=2)

            return dilation
        return img

    def getBGSubtractor(self, BGS_TYPE: str):
        if BGS_TYPE == "GMG":
            return cv2.bgsegm.createBackgroundSubtractorGMG()
        if BGS_TYPE == "MOG":
            return cv2.bgsegm.createBackgroundSubtractorMOG()
        if BGS_TYPE == "MOG2":
            return cv2.createBackgroundSubtractorMOG2()
        if BGS_TYPE == "KNN":
            return cv2.createBackgroundSubtractorKNN()
        if BGS_TYPE == "CNT":
            return cv2.bgsegm.createBackgroundSubtractorCNT()
        print("Detector inválido")
        sys.exit(1)

    def runFromImshow(self, FONT: int, TEXT_COLOR: Tuple[int, int, int],
                      TRACKER_COLOR: Tuple[int, int, int]):
        while (self.cap.isOpened()):
            ok, frame = self.cap.read()
            if not ok:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            frame = cv2.resize(frame, (0, 0), fx=0.50, fy=0.50)

            fgmask = self.bg_subtractor.apply(frame)
            fgmask = self.getFilter(fgmask, 'combine')
            fgmask = cv2.medianBlur(fgmask, 5)

            contours, hierarchy = cv2.findContours(
                fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for c in contours:
                if cv2.contourArea(c) < self.minArea:
                    continue

                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (10, 30), (250, 55), (255, 0, 0), -1)
                cv2.putText(frame, "Rastreando Objetos", (10, 50),
                            FONT, 0.8, TEXT_COLOR, 2, cv2.LINE_AA)
                cv2.drawContours(frame, c, -1, TRACKER_COLOR, 3)
                cv2.drawContours(frame, c, -1, (255, 255, 255), 1)
                cv2.rectangle(frame, (x, y), (x+w, y+h), TRACKER_COLOR, 3)
                cv2.rectangle(frame, (x, y), (x + w, y + h),
                              (255, 255, 255), 1)

            result = cv2.bitwise_and(frame, frame, mask=fgmask)
            cv2.imshow('frame', frame)
            cv2.imshow('fgmask', result)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def run(self, FONT: int, TEXT_COLOR: Tuple[int, int, int],
            TRACKER_COLOR: Tuple[int, int, int]) -> \
            Union[Tuple[None, None], Tuple[bool, List[List[int]]]]:
        while (self.cap.isOpened()):
            ok, frame = self.cap.read()
            if not ok:
                print("Can't receive frame (stream end?). Exiting ...")
                # reiniciar o video
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                break

            frame = cv2.resize(frame, (580, 300), fx=0.50, fy=0.50)

            fgmask = self.bg_subtractor.apply(frame)
            fgmask = self.getFilter(fgmask, 'combine')
            fgmask = cv2.medianBlur(fgmask, 5)

            contours, hierarchy = cv2.findContours(
                fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for c in contours:
                if cv2.contourArea(c) < self.minArea:
                    continue

                (x, y, w, h) = cv2.boundingRect(c)
                # cv2.rectangle(frame, (10, 30), (258, 55), (255, 0, 0), -1)
                # cv2.putText(frame, "Rastreando Objetos", (10, 50),
                #            FONT, 0.8, TEXT_COLOR, 2, cv2.LINE_AA)
                cv2.drawContours(frame, c, -1, TRACKER_COLOR, 3)
                cv2.drawContours(frame, c, -1, (255, 255, 255), 1)
                cv2.rectangle(frame, (x, y), (x+w, y+h), TRACKER_COLOR, 3)
                cv2.rectangle(frame, (x, y), (x + w, y + h),
                              (255, 255, 255), 1)

            result = cv2.bitwise_and(frame, frame, mask=fgmask)
            return (frame, result)

        return (None, None)
