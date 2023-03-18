# You can run directly this code with: poetry run python face_cam_detection.py
import cv2

# Carrega o modelo de detecção de faces treinado
face_recognizer = cv2.CascadeClassifier(cv2.data.haarcascades +
                                        "haarcascade_frontalface_default.xml")

# Inicia a captura de vídeo da webcam
webcam = cv2.VideoCapture(0)

# Loop infinito para capturar novas imagens
while True:
    # Lê a imagem da webcam
    ret, frame = webcam.read()

    # Executa a detecção de faces
    faces = face_recognizer.detectMultiScale(frame)

    # Desenha um retângulo ao redor das faces detectadas
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Exibe a imagem com as faces detectadas
    cv2.imshow("Faces detectadas", frame)

    # Finaliza o loop quando a tecla 'q' é pressionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Finaliza a captura de vídeo da webcam
webcam.release()

# Fecha todas as janelas abertas
cv2.destroyAllWindows()
