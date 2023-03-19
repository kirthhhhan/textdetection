import cv2 
import string
import pytesseract


def testdet():

    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    # To Read the image 
    image = cv2.imread("poem3.jpg")

    # To convert from BGR to RGB 
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # To detect text_from_image from image
    text_from_image = pytesseract.image_to_string(image)
    print(text_from_image)

    #conf = r'-c tessedit_char_whitelist='+string.ascii_letters   # uncomment if you want to detect alphabets only.
    conf = r'-c tessedit_char_whitelist='+string.digits
    conf = conf + string.ascii_letters   

    def draw_boxes_on_character(image):
        image_width = image.shape[1]
        image_height = image.shape[0]

        # To return each detected character and their bounding boxes.
        boxes = pytesseract.image_to_boxes(image, config =conf)

        print(boxes)
        for box in boxes.splitlines():
            box = box.split(" ")
            character = box[0]
            x = int(box[1])
            y = int(box[2])
            x2 = int(box[3])
            y2 = int(box[4])
            cv2.rectangle(image, (x, image_height - y), (x2, image_height - y2), (0, 255, 0), 1)
            cv2.putText(image, character, (x, image_height -y2), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 0, 255) , 1)
        return image

    def draw_boxes_on_text(image):
        # To return raw information about the detected text_from_image
        raw_data = pytesseract.image_to_data(image)

        print(raw_data)
        for count, data in enumerate(raw_data.splitlines()):
            if count > 0:
                data = data.split()
                if len(data) == 12:
                    x, y, w, h, content = int(data[6]), int(data[7]), int(data[8]), int(data[9]), data[11]
                    cv2.rectangle(image, (x, y), (w+x, h+y), (0, 255, 0), 1)
                    cv2.putText(image, content, (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255) , 1)
                    
        return image

    image = draw_boxes_on_character(image)     # uncomment if you want to detect individual characters

    #image = draw_boxes_on_text(image)    # Uncomment this if you want to detect text_from_image

    # To show the output
    cv2.imshow('output',image)
    cv2.WINDOW_FULLSCREEN 
    cv2.WINDOW_FREERATIO
    cv2.WINDOW_AUTOSIZE
    cv2.WINDOW_NORMAL
    cv2.WINDOW_GUI_EXPANDED
    cv2.waitKey(0)