import numpy as np
import cv2
import sys
from PyQt6.QtWidgets import QMainWindow, QLabel, QApplication,\
    QVBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import QTimer
from PyQt6 import QtCore
from PyQt6.QtGui import QImage, QPixmap

TEXT_COLOR = (0, 255, 0)
TRACKER_COLOR = (255, 0, 0)
FONT = cv2.FONT_HERSHEY_SIMPLEX
VIDEO_SOURCE = "videos/Cars.mp4"

BGS_TYPES = ["GMG", "MOG", "MOG2", "KNN", "CNT"]
BGS_TYPE = BGS_TYPES[2]


class MotionTracking:
    def __init__(self, video_source):
        self.cap = cv2.VideoCapture(video_source)
        self.minArea = 250
        self.bg_subtractor = self.getBGSubtractor(BGS_TYPE)

    def getKernel(self, KERNEL_TYPE):
        if KERNEL_TYPE == "dilation":
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        if KERNEL_TYPE == "opening":
            kernel = np.ones((3, 3), np.uint8)
        if KERNEL_TYPE == "closing":
            kernel = np.ones((3, 3), np.uint8)

        return kernel

    def getFilter(self, img, filter):
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

    def getBGSubtractor(self, BGS_TYPE):
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

    def runFromImshow(self):
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

    def run(self):
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
                cv2.rectangle(frame, (10, 30), (258, 55), (255, 0, 0), -1)
                cv2.putText(frame, "Rastreando Objetos", (10, 50),
                            FONT, 0.8, TEXT_COLOR, 2, cv2.LINE_AA)
                cv2.drawContours(frame, c, -1, TRACKER_COLOR, 3)
                cv2.drawContours(frame, c, -1, (255, 255, 255), 1)
                cv2.rectangle(frame, (x, y), (x+w, y+h), TRACKER_COLOR, 3)
                cv2.rectangle(frame, (x, y), (x + w, y + h),
                              (255, 255, 255), 1)

            result = cv2.bitwise_and(frame, frame, mask=fgmask)
            return (frame, result)


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Captura de Movimento")
        self.setGeometry(0, 0, 600, 720)
        self.setFixedSize(600, 720)

        # Cria um layout vertical
        self.layout = QVBoxLayout()
        # self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(1)
        # self.layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)

        # Cria um widget para conter o layout
        self.widget = QWidget()
        # Define o layout do widget
        self.widget.setLayout(self.layout)
        # Define o widget como a janela principal
        self.setCentralWidget(self.widget)

        # Cria um botão
        self.button = QPushButton("Iniciar")
        # Define o tamanho do botão
        self.button.setFixedSize(100, 50)
        # Remove as margens do botão
        self.button.setContentsMargins(0, 0, 0, 0)


# QtCore.Qt.AlignmentFlag.AlignCenter
        # self.button.clicked.connect(self.start)
        # Adiciona o botão ao layout
        self.layout.addWidget(
            self.button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # Cria um label para exibir a imagem
        self.label = QLabel()
        self.label.setFixedSize(580, 320)

        # Define o alinhamento do texto no label
        self.label.setStyleSheet("background-color: black;")
        # Adiciona o label ao layout
        self.layout.addWidget(
            self.label, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label2 = QLabel()
        self.label2.setFixedSize(580, 320)
        # self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setStyleSheet("background-color: black;")
        self.layout.addWidget(self.label2,
                              alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        # self.timer.start(1)
        self.button.clicked.connect(self.timer.start)

    def update_frame(self):
        frame, result = motion_tracking.run()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        height, width, channel = frame.shape
        step = channel * width
        qImg = QImage(frame.data, width, height, step,
                      QImage.Format.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(qImg))

        height, width, channel = result.shape
        step = channel * width
        qImg = QImage(result.data, width, height, step,
                      QImage.Format.Format_RGB888)
        self.label2.setPixmap(QPixmap.fromImage(qImg))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    motion_tracking = MotionTracking(VIDEO_SOURCE)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
