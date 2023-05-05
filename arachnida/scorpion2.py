from tkinter import *
from tkinter import filedialog, scrolledtext
from PIL import Image, ExifTags
import re

class App:
    def __init__(self):
        self.ventana = Tk()
        self.ventana.title("EXIF DATA VIEWER")
        self.ventana.configure(bg="light blue")
        self.ventana.geometry("800x800")
    
        self.file_label = Label(self.ventana,text="NO FILE SELECTED",bg="light green")
        self.file_label.pack(side=TOP)

        self.display = scrolledtext.ScrolledText(self.ventana,bg="black",fg="light green",width=100,height=20)
        self.display.pack(side=TOP)

        self.btn_search = Button(self.ventana,text="SEARCH FILE",bg="orange",width=30,command=self.open_file)
        self.btn_search.pack(side=LEFT)

        self.btn_edit_meta = Button(self.ventana, text="EDIT META", bg="yellow", width=30, command=self.edit_meta)
        self.btn_edit_meta.pack(side=LEFT)

        self.btn_quit = Button(self.ventana, text="QUIT", bg="red", width=30, command=self.quit)
        self.btn_quit.pack(side=LEFT)

        self.dropdown = None
        self.radio_var = StringVar()

        self.ventana.mainloop()

    def open_file(self):
        file = filedialog.askopenfilename(initialdir="/",title="SELECT FILE",
                                          filetypes=(("jpeg files","*.jpg"),("all files","*.*")))
        if file != "":
            self.file_label.configure(text=(file).split("/")[-1])
            self.extract_data(file)

    def extract_data(self,f):
        self.display.delete('1.0',END)
        try:
            image = Image.open(f)
            exifdata = image._getexif()
            if exifdata is not None:
                self.display.insert(END,"-"*26+"METADATA INFO"+"-"*26+"\n")
                for tag_id in exifdata:
                    self.tag = ExifTags.TAGS.get(tag_id, tag_id)
                    data = exifdata.get(tag_id)
                    if isinstance(data, bytes):
                        data = data.decode('UTF8','replace')
                    try:
                        self.display.insert(END,f"{self.tag:26}: {data}"+"\n")
                    except:
                        data = re.sub('[^a-zA-Z0-9 \n\.]', '', data)
                        self.display.insert(END,f"{self.tag:26}: {data}"+"\n")
                self.display.insert(END,"-"*65)
            else:
                self.display.insert(END,'NO DATA')
        except:
            self.display.insert(END,'ERROR')

    def edit_meta(self):
        self.dropdown = OptionMenu(self.ventana, self.radio_var, *ExifTags.TAGS)
        self.dropdown.pack(side=LEFT)
        self.radio_var.set(ExifTags.TAGS[0])
        self.radio_modify = Radiobutton(self.ventana, text='Modify', variable=self.radio_var, value='modify')
        self.radio_modify.pack(side=LEFT)
        self.radio_delete = Radiobutton(self.ventana, text='Delete', variable=self.radio_var, value='delete')
        self.radio_delete.pack(side=LEFT)

    def quit(self):
        self.ventana.destroy()

 
if __name__=="__main__":
    App()