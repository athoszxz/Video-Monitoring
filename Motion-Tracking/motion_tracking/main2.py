import cv2
import sys
from PyQt6.QtWidgets import QMainWindow, QLabel, QApplication,\
    QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import QTimer
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import QImage, QPixmap
from MotionTracking import MotionTracking

TEXT_COLOR = (0, 255, 0)
TRACKER_COLOR = (255, 0, 0)
FONT = cv2.FONT_HERSHEY_SIMPLEX
VIDEO_SOURCE = "videos/Cars.mp4"

BGS_TYPES = ["GMG", "MOG", "MOG2", "KNN", "CNT"]
BGS_TYPE = BGS_TYPES[2]


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Inicializa a janela e define seu título
        self.setWindowTitle("Captura de Movimento")
        # Define o tamanho da janela
        self.setGeometry(0, 0, 600, 720)
        # Define o tamanho mínimo da janela
        self.setFixedSize(600, 720)

        # Cria um layout vertical
        self.layout = QVBoxLayout()
        # Define o espaçamento entre os widgets
        self.layout.setSpacing(3)

        # Cria um widget para conter o layout
        self.widget = QWidget()
        # Define o layout do widget
        self.widget.setLayout(self.layout)
        # Define o widget como a janela principal
        self.setCentralWidget(self.widget)

        # Cria outro widget para conter os dois botões
        self.widgetButtons = QWidget()
        # Cria um layout horizontal
        self.layoutButtons = QHBoxLayout()
        # Define o espaçamento entre os widgets
        self.layoutButtons.setSpacing(3)
        # Define o layout do widget
        self.widgetButtons.setLayout(self.layoutButtons)

        # Cria um botão
        self.button = QPushButton("Iniciar")
        # Define o tamanho do botão
        self.button.setFixedSize(100, 50)
        # Remove as margens do botão
        self.button.setContentsMargins(0, 0, 0, 0)
        # Estiliza a fonte do botão
        self.button.setFont(QtGui.QFont(
            "Arial", 12, QtGui.QFont.Weight.Bold))

        # Adiciona o botão ao layout
        self.layoutButtons.addWidget(
            self.button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # Cria um outro botão
        self.button2 = QPushButton("Parar")
        # Define o tamanho do botão
        self.button2.setFixedSize(100, 50)
        # Remove as margens do botão
        self.button2.setContentsMargins(0, 0, 0, 0)
        # Estiliza a fonte do botão
        self.button2.setFont(QtGui.QFont(
            "Arial", 12, QtGui.QFont.Weight.Bold))

        # Adiciona o botão ao layout
        self.layoutButtons.addWidget(
            self.button2, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # Adiciona o widget dos botões ao layout
        self.layout.addWidget(
            self.widgetButtons, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # Cria um label para exibir a imagem
        self.label = QLabel()
        # Define o tamanho do label
        self.label.setFixedSize(580, 300)
        # Define o espaçamento entre os labels
        self.label.setContentsMargins(1, 1, 1, 1)

        # Define a cor de fundo do label
        self.label.setStyleSheet("background-color: black;")
        # Adiciona o label ao layout
        self.layout.addWidget(
            self.label, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # Cria outro label para exibir a imagem
        self.label2 = QLabel()
        self.label2.setFixedSize(580, 320)
        self.label2.setStyleSheet("background-color: black;")
        self.layout.addWidget(self.label2,
                              alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # Cria um timer
        self.timer = QTimer()
        # Conecta o timer ao método update_frame
        self.timer.timeout.connect(self.update_frame)

        # self.timer.start(1) se quiser iniciar o timer já na inicialização

        # Conecta o botão iniciar ao timer
        self.button.clicked.connect(self.timer.start)
        # Conecta o botão parar ao timer
        self.button2.clicked.connect(self.timer.stop)

    def update_frame(self):
        frame, result = motion_tracking.run(FONT, TEXT_COLOR, TRACKER_COLOR)
        if frame is None or result is None:
            return
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
    motion_tracking = MotionTracking(VIDEO_SOURCE, BGS_TYPE)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
