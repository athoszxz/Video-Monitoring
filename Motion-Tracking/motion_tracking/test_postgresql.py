# You can run directly this code with: poetry run python test_postgresql.py
# But you need to have a PostgreSQL installed and running.
# You can download it from: https://www.postgresql.org/download/
# And you can install it with: pip install psycopg2 or poetry add psycopg2
# You don't need to create the database, the code will do it for you.
import psycopg2
import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit,\
    QLabel, QMessageBox, QTableWidget, QTableWidgetItem, QFileDialog
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QImage, QPixmap


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt6 - Primeira Tela'
        self.left = 500
        self.top = 300
        self.width = 400
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.label_user = QLabel("Usuário", self)
        self.label_user.move(20, 20)
        self.label_password = QLabel("Sobrenome", self)
        self.label_password.move(20, 60)

        self.textbox_user = QLineEdit(self)
        self.textbox_user.move(80, 20)
        self.textbox_password = QLineEdit(self)
        self.textbox_password.move(80, 60)

        self.button_submit = QPushButton('Enviar', self)
        self.button_submit.clicked.connect(self.on_click_submit)
        self.button_submit.resize(80, 30)
        self.button_submit.move(200, 120)

        self.check_file_exists()

    def check_file_exists(self):
        if os.path.exists("data.txt"):
            with open("data.txt", "r") as f:
                user, password = f.read().split(" ")
            self.open_second_window(user, password)
        else:
            self.show()

    @pyqtSlot()
    def on_click_submit(self):
        user = self.textbox_user.text()
        password = self.textbox_password.text()
        with open("data.txt", "w") as f:
            f.write(user + " " + password)
        self.open_second_window(user, password)
        self.close()

    def open_second_window(self, user="", password=""):
        self.second_app = SecondApp(user, password)
        self.second_app.show()


class SecondApp(QWidget):
    def __init__(self, user="", password=""):
        super().__init__()
        self.title = 'PyQt6 - Segunda Tela'
        self.left = 500
        self.top = 300
        self.width = 340
        self.height = 760
        self.user_postgresql = user
        self.password_postgresql = password
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Criar os campos do formulário

        # Nome
        self.first_name_label = QLabel("Nome", self)
        self.first_name_label.move(20, 20)
        self.first_name_textbox = QLineEdit(self)
        self.first_name_textbox.move(90, 20)

        # Sobrenome
        self.last_name_label = QLabel("Sobrenome", self)
        self.last_name_label.move(20, 60)
        self.last_name_textbox = QLineEdit(self)
        self.last_name_textbox.move(90, 60)

        # Idade
        self.age_input_label = QLabel("Idade", self)
        self.age_input_label.move(20, 100)
        self.age_input_textbox = QLineEdit(self)
        self.age_input_textbox.move(90, 100)

        # Cria o botão de Adicionar imagem
        self.open_image_button = QPushButton("Adicionar imagem", self)
        self.open_image_button.move(20, 140)
        self.open_image_button.clicked.connect(self.open_image)

        # Cria o botão de enviar
        self.submit_button = QPushButton("Enviar", self)
        self.submit_button.move(100, 180)
        self.submit_button.clicked.connect(self.submit_data)

        # Criar a tabela
        self.table = QTableWidget(self)
        self.table.move(20, 250)
        self.table.resize(300, 200)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Nome", "Sobrenome", "Idade"])

        # Cria um local para exibir a imagem com o tamanho de 300x300
        self.image_label = QLabel(self)
        self.image_label.move(20, 470)
        self.image_label.resize(150, 150)
        # faz a imagem caber no label
        self.image_label.setScaledContents(True)

        # Cria uma caixa de texto para pegar o id
        self.id_textbox = QLineEdit(self)
        self.id_textbox.move(20, 650)
        self.id_textbox.resize(100, 30)

        # Cria o botão de buscar imagem
        self.search_image_button = QPushButton("Buscar imagem", self)
        self.search_image_button.move(20, 680)
        self.search_image_button.clicked.connect(self.search_image)

        # Pegar o nome de todos os databases
        connection = psycopg2.connect(host="localhost", database="postgres",
                                      user=self.user_postgresql,
                                      password=self.password_postgresql)
        cursor = connection.cursor()
        cursor.execute("SELECT datname FROM pg_database")
        databases = [database[0] for database in cursor.fetchall()]
        connection.close()

        # Se não existir, criar o database "db_alphas_sentinels_2023_144325"
        if "db_alphas_sentinels_2023_144325" not in databases:
            print("Database 'db_alphas_sentinels_2023_144325' não " +
                  "encontrado. Criando...")
            connection = psycopg2.connect(host="localhost",
                                          database="postgres",
                                          user=self.user_postgresql,
                                          password=self.password_postgresql)
            cursor = connection.cursor()
            connection.autocommit = True
            cursor.execute("CREATE DATABASE db_alphas_sentinels_2023_144325")
            connection.close()

        # Criar as tabelas
        connection = psycopg2.connect(host="localhost", database="db_alphas_" +
                                      "sentinels_2023_144325",
                                      user=self.user_postgresql,
                                      password=self.password_postgresql)
        cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, first" +
            "_name VARCHAR(50), last_name VARCHAR(50)," +
            " age INTEGER, photo BYTEA)")
        connection.commit()
        connection.close()

        # Executar a consulta SQL para recuperar os dados
        connection = psycopg2.connect(host="localhost", database="db_alphas_" +
                                      "sentinels_2023_144325",
                                      user=self.user_postgresql,
                                      password=self.password_postgresql)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        self.table.setRowCount(len(rows))
        # Preencher a tabela com os dados ignorando o ID
        for i, row in enumerate(rows):
            for j, field in enumerate(row[1:]):
                self.table.setItem(i, j, QTableWidgetItem(str(field)))

        self.show()

    def search_image(self):
        # Pegar o ID do usuário
        user_id = self.id_textbox.text()
        # Executar a consulta SQL para recuperar os dados
        connection = psycopg2.connect(host="localhost", database="db_alphas_" +
                                      "sentinels_2023_144325",
                                      user=self.user_postgresql,
                                      password=self.password_postgresql)
        cursor = connection.cursor()
        cursor.execute("SELECT photo FROM users WHERE id = %s", (user_id,))
        photo = cursor.fetchone()[0]
        # Criar um objeto de imagem
        image = QImage()
        # Carregar a imagem
        image.loadFromData(photo)
        # Exibir a imagem
        self.image_label.setPixmap(QPixmap(image))

    def open_image(self):
        # Abrir a janela de seleção de arquivo
        file_name = QFileDialog.getOpenFileName(self, "Abrir imagem", "",
                                                "Imagens (*.png *.jpg)")[0]
        if file_name:
            # Ler o arquivo binário
            with open(file_name, "rb") as f:
                self.image = f.read()

    def submit_data(self):
        first_name = self.first_name_textbox.text()
        last_name = self.last_name_textbox.text()
        age = self.age_input_textbox.text()
        photo = self.image
        connection = psycopg2.connect(host="localhost", database="db_alphas_" +
                                      "sentinels_2023_144325",
                                      user=self.user_postgresql,
                                      password=self.password_postgresql)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (first_name, last_name, age, photo) "
                       "VALUES (%s, %s, %s, %s)", (
                           first_name, last_name, age, psycopg2.Binary(photo)))
        connection.commit()
        connection.close()
        self.show_message_box("Dados enviados com sucesso!")

        # Limpar a tabela
        self.table.setRowCount(0)

        # Executar a consulta SQL para recuperar os dados
        connection = psycopg2.connect(host="localhost", database="db_alphas_" +
                                      "sentinels_2023_144325",
                                      user=self.user_postgresql,
                                      password=self.password_postgresql)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        self.table.setRowCount(len(rows))
        # Preencher a tabela com os dados ignorando o ID
        for i, row in enumerate(rows):
            for j, field in enumerate(row[1:]):
                self.table.setItem(i, j, QTableWidgetItem(str(field)))

        # Limpar os campos de texto
        self.first_name_textbox.setText("")
        self.last_name_textbox.setText("")
        self.age_input_textbox.setText("")

    @pyqtSlot()
    def on_click_hello_world(self):
        self.show_message_box('Hello World')

    def show_message_box(self, message):
        msg_box = QMessageBox()
        msg_box.setText(message)
        msg_box.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())
