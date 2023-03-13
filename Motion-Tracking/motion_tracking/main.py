import cv2
import sys
from PyQt6.QtWidgets import QMainWindow, QLabel, QApplication,\
    QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QToolBar, QFileDialog
from PyQt6.QtCore import QTimer
from PyQt6 import QtCore, QtGui, QtWidgets
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
        self.setGeometry(0, 0, 600, 760)
        # Define o tamanho mínimo da janela
        self.setFixedSize(600, 760)

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
        # Amplia o video com pyqt6 para o tamanho do label se necessário
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                 QtWidgets.QSizePolicy.Policy.Expanding)
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

        # cria uma barra de ferramentas
        self.toolbar = QToolBar('Barra de Ferramentas')
        # adiciona a barra de ferramentas à janela
        self.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolbar)

        # cria a ação "Abrir"
        self.actionOpen = QtGui.QAction(QtGui.QIcon(
            'icons/open.svg'), 'Abrir', self)
        # define a tecla de atalho
        self.actionOpen.setShortcut('Ctrl+O')
        # define o que acontece quando a ação é acionada
        self.actionOpen.triggered.connect(self.open_file)

        # adiciona a ação à barra de ferramentas
        self.toolbar.addAction(self.actionOpen)

        # cria a ação "Webcam"
        self.actionWebcam = QtGui.QAction(QtGui.QIcon(
            'icons/webcam.svg'), 'Webcam', self)
        # define a tecla de atalho
        self.actionWebcam.setShortcut('Ctrl+W')
        # define o que acontece quando a ação é acionada
        self.actionWebcam.triggered.connect(self.set_webcam)

        # adiciona a ação à barra de ferramentas
        self.toolbar.addAction(self.actionWebcam)

        # Cria um timer
        self.timer = QTimer()
        # Conecta o timer ao método update_frame
        self.timer.timeout.connect(self.update_frame)

        # Reduz a frequência do timer para 1 frame por segundo
        self.timer.setInterval(int(1000/40))

        # self.timer.start(1) se quiser iniciar o timer já na inicialização

        # Conecta o botão iniciar ao timer
        self.button.clicked.connect(self.timer.start)
        # Conecta o botão parar ao timer
        self.button2.clicked.connect(self.timer.stop)

    def set_webcam(self):
        # define a webcam como a fonte de vídeo
        motion_tracking.set_video_source(0)

    def open_file(self):
        # abre uma caixa de diálogo para selecionar o arquivo
        filename = QFileDialog.getOpenFileName(
            self, 'Abrir arquivo', '', 'Vídeos (*.mp4 *.avi)')[0]
        # se o usuário selecionou um arquivo
        if filename:
            # define o arquivo como a fonte de vídeo
            motion_tracking.set_video_source(filename)

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
