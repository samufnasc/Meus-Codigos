import cv2
import numpy as np

def get_pixel_color(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        bgr_color = frame[y, x]
        hsv_color = cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)[0][0]
        #print("Pixel color (BGR): ", bgr_color)
        print("Pixel color (HSV): ", hsv_color)

# Inicia a captura de vídeo da câmera
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

cap.set(3, 640)
cap.set(4, 360)
cap.set(5, 25)  #set frame
cap.set(cv2.CAP_PROP_BRIGHTNESS, 128)
cap.set(cv2.CAP_PROP_CONTRAST, 32)
cap.set(cv2.CAP_PROP_AUTO_WB, 1)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)
#cap.set(cv2.CAP_PROP_EXPOSURE, -1)

# Define a função de retorno de chamada de mouse para capturar as coordenadas do clique
cv2.namedWindow("image")
cv2.setMouseCallback("image", get_pixel_color)

while True:
    # Captura um quadro de vídeo
    ret, frame = cap.read()
    
    # Verifica se o quadro foi capturado com sucesso
    if not ret:
        print("Erro ao capturar quadro de vídeo")
        break
    
    # Exibe o quadro de vídeo em uma janela
    cv2.imshow("image", frame)
    
    # Verifica se a tecla 'q' foi pressionada para sair do loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a câmera e fecha a janela
cap.release()
cv2.destroyAllWindows()