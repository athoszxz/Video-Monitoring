# You can run directly this code with: poetry run python face_train.py
# But the training is already done, so you don't need to run this code.
# The training is done in the file:
# Motion-Tracking\motion_tracking\trainings\haarcascade_frontalface_default.xml
import cv2
import os
import numpy as np


# Carrega a base de dados de imagens de rostos
face_database_path = "data_faces/"
face_images = []
labels = []

# Encontra todas as imagens dentro da pasta
for i, file in enumerate(os.listdir(face_database_path)):
    # Carrega a imagem em uma Mat
    img = cv2.imread(os.path.join(face_database_path, file))
    # Converte a imagem em uma matriz contínua
    img = np.ascontiguousarray(img, dtype=np.uint8)
    # Adiciona a Mat na lista de imagens
    face_images.append(img)
    # Adiciona o rótulo da imagem na lista de rótulos
    labels.append(i)

# Inicializa o reconhecedor de faces
face_recognizer = cv2.face.FisherFaceRecognizer_create()

# Inicializa o treinamento
face_recognizer.train(face_images, np.array(labels))

# Salva os pesos do treinamento
face_recognizer.save("trainings/haarcascade_frontalface_default.xml")
