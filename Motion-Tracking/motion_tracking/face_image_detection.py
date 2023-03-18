# You can run directly this code with:
# poetry run python face_image_detection.py
import cv2

# Carrega a imagem de entrada
input_image = cv2.imread("test_images/input_image.png")

# Carrega o modelo de detecção de faces treinado
face_recognizer = cv2.CascadeClassifier(cv2.data.haarcascades +
                                        "haarcascade_frontalface_default.xml")

# Executa a detecção de faces
faces = face_recognizer.detectMultiScale(input_image)

# Desenha um retângulo ao redor das faces detectadas
for (x, y, w, h) in faces:
    cv2.rectangle(input_image, (x, y), (x + w, y + h), (255, 0, 0), 2)

# Exibe a imagem com as faces detectadas
cv2.imshow("Faces detectadas", input_image)
cv2.waitKey(0)
