import tkinter.messagebox
import customtkinter
from tkinter import *
import cv2 
from PIL import Image
import string
import pytesseract
from pytesseract import pytesseract



customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "green" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        

        # configure window
        self.title("TEXT DETECTOR")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=170, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="TEXT DETECTOR", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command= self.webcam1)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.imagemat)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        #self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        #self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)                                                      
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        #self.entry = customtkinter.CTkEntry(self, placeholder_text="Enter the filename: ")
        #self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        #self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),command=input(path))
        #self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

       
       

       

       
        # set default values
        #self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
        self.sidebar_button_1.configure(text="Webcam mode")
        self.sidebar_button_2.configure(text="Image mode")
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        
        self.textbox.insert("0.0", "TEXT DETECTOR" + "\n\nGeneral Instructions for use of the app: \n\n1.Two modes of operation i.e webcam and input image \n\n2.Webcam captures the image and displays results on terminal \n\n3.Input image mode opens up a window and detects individual characters \n\n4.Images other than webcam input can also be added by either specifying path or input image filename \n\n5. Press 's' to capture images using Webcam Mode")  
                                                                                            
       

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)


    def webcam1(self):

        camera=cv2.VideoCapture(0)
        while True:
            _,image=camera.read()
            cv2.imshow('text detection',image)
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


    def imagemat(self):
        
        
        # To Read the image 
        image = cv2.imread("test1.jpg")

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

           


if __name__ == "__main__":
    app = App()
    app.mainloop()