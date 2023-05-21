import cv2
import imutils
import pytesseract

# Inicializar la cámara
captura = cv2.VideoCapture(0)

while True:
    # Capturar el fotograma de la cámara
    _, fotograma = captura.read()
    print('llega al for')
    # Redimensionar el fotograma para facilitar el procesamiento
    fotograma = imutils.resize(fotograma, width=600)

    # Convertir el fotograma a escala de grises
    gris = cv2.cvtColor(fotograma, cv2.COLOR_BGR2GRAY)

    # Aplicar un filtro de suavizado para reducir el ruido
    suavizado = cv2.bilateralFilter(gris, 11, 17, 17)

    # Detectar los bordes en el fotograma utilizando Canny
    bordes = cv2.Canny(suavizado, 30, 200)

    # Encontrar los contornos en el fotograma
    contornos, _ = cv2.findContours(bordes.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contornos = sorted(contornos, key=cv2.contourArea, reverse=True)[:10]

    # Inicializar la variable que almacenará la patente
    patente = None

    for contorno in contornos:
        # Aproximar el contorno a un polígono
        perimetro = cv2.arcLength(contorno, True)
        approx = cv2.approxPolyDP(contorno, 0.018 * perimetro, True)

        # Si el contorno tiene cuatro vértices, se considera una posible patente
        if len(approx) == 4:
            patente = approx
            break

    if patente is not None:
        # Dibujar el contorno de la patente en el fotograma
        cv2.drawContours(fotograma, [patente], -1, (0, 255, 0), 3)

        # Recortar la región del fotograma que contiene la patente
        (x, y, w, h) = cv2.boundingRect(patente)
        patente_recortada = suavizado[y:y + h, x:x + w]

        # Aplicar OCR a la región de la patente
        texto_patente = pytesseract.image_to_string(patente_recortada, lang='eng')

        # Imprimir el texto de la patente
        print('Patente:', texto_patente)

    # Mostrar el fotograma resultante
    cv2.imshow('Fotograma', fotograma)

    # Detener el bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar los recursos y cerrar las ventanas
captura.release()
cv2.destroyAllWindows()
