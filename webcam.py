import cv2 
from PIL import Image
from pytesseract import pytesseract



def webcam3():
    camera=cv2.VideoCapture(0)
    while True:
        _,image=camera.read()
        cv2.imshow("Text detector",image)
        if cv2.waitKey(1)& 0xFF==ord('s'):
            cv2.imwrite('test1.jpg',image)
            break
    camera.release()
    cv2.destroyAllWindows()

    def tesseract():
        path_to_tesseract=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        Imagepath='test1.jpg'
        pytesseract.tesseract_cmd=path_to_tesseract
        text=pytesseract.image_to_string(Image.open(Imagepath))
        print(text[:-1])
    tesseract()


