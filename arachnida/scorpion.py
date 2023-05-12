from tkinter import *
from tkinter import filedialog, scrolledtext, ttk, messagebox
from tkinter.filedialog import asksaveasfile
from PIL import Image, ExifTags, TiffImagePlugin
import re
import os
import sys
import humanize
from datetime import datetime

import pikepdf
from typing import Dict
import docx
from docx.document import Document
from docx.opc.coreprops import CoreProperties
# python -m pip install python-docx
#  python .\scorpion.py .\data\foto1.jpg .\data\Arachnida.pdf .\data\Documento.docx

from functions import *

import xml
import exif
import zipfile

class App:
    
    
    ###############
    # MAIN WINDOW
    ###############
    def __init__(self, file=None):
        
        if file:
            self.file = file
            
            self.extract_and_print_on_screen()
       
            
        else:
            self.ventana = Tk()
            self.ventana.title("SCORPION 2023 - EXIF DATA EDITOR")
            self.ventana.configure()
            #self.ventana.geometry("900x475")
        
            #self.file_label = Label(self.ventana,text="NO FILE SELECTED",bg="light green")
            self.file_label = Label(self.ventana,text="NO FILE SELECTED")
            self.file_label.grid(row=0, column=3, sticky="n")

            self.display = scrolledtext.ScrolledText(self.ventana,bg="black", wrap=NONE,fg="light green",height=20)
            self.display.grid(row=1, column=0, columnspan=7,sticky="we")

            # Add a Scrollbar(horizontal)
            self.bar=Scrollbar(self.ventana, orient='horizontal', command=self.display.xview)
            self.bar.grid(row=2, column=0, columnspan=7,sticky="swe")
            self.display.config(xscrollcommand=self.bar.set)
            
            self.btn_search = Button(self.ventana,text="SEARCH FILE",width=30, bg="orange",command=self.open_file)
            self.btn_search.grid(row=3, column=0, sticky="we", columnspan=3)

            self.btn_quit = Button(self.ventana, text="QUIT",width=30, bg="red", command=self.quit)
            self.btn_quit.grid(row=3, column=4, sticky="we", columnspan=3)

            # Variables & widgets declaration
            self.tags = []
            self.data = {'choose metadata':"choose metadata from list"}    

            self.image = 0
            self.file = 0
            self.exifdata = 0

            self.dropdown_var = StringVar()
            self.radio_var = StringVar()
            self.valores = StringVar()

            self.button_edit_meta = False
            self.dropdown = False
            self.radio_modify = False
            self.radio_delete = False
            self.edit_label = False
            self.edit_entry = False
            self.ok_btn = False
            self.btn_save = False
            
            self.ventana.mainloop()


    ###############################################
    # OPEN FILE + EXTRACT DATA + DISPLAY DATA ON APP
    ###############################################
    def open_file(self):
        
        # ask for file to process
        self.file = filedialog.askopenfilename(initialdir="./data/",title="SELECT FILE", filetypes=([("",".jpg .jpeg .png .bmp .gif .docx .pdf")]))
        if self.file != "":
            
             # remove any widget relative to file editing
            self.display.delete('1.0',END)
            if self.dropdown:
                self.dropdown.destroy()
            if self.radio_modify:
                self.radio_modify.destroy()
            if self.radio_delete:
                self.radio_delete.destroy()
            if self.edit_label:
                self.edit_label.destroy()
            if self.edit_entry:
                self.edit_entry.destroy()
            if self.ok_btn:
                self.ok_btn.destroy()
            if self.btn_save:
                self.btn_save.destroy()
            
            # print file name at the top of the window
            self.file_label.configure(text="File to be processed: "+self.file.split("/")[-1])
            
            # call to extract_data function
            self.extract_data()
            self.display_data()

            
    ###############################################
    # EXTRACT DATA + DISPLAY DATA ON SCREEN
    ###############################################
    def extract_and_print_on_screen(self):
            self.extract_data()
            
            # display file info
            print('\n    '+'-'*26+'FILE INFO'+'-'*26)
            print(f"    {'File_Name':26}: {self.file}")
            for tag, data in self.data.items():
                if isinstance(tag, str) and tag != "choose metadata" :
                    if tag[:5] == 'File_':
                        print(f'    {tag:26}: {data}')
            
            # get file extension
            ext = self.file.split(".")[-1]
            
            # if file has valid image extension, process it
            if ext in ['jpg','jpeg','png','bmp','gif']:
                # display EXIF metadata if any
                print('    '+'-'*26+'EXIF INFO'+'-'*26)
                if len(self.data) > 4:
                    for tag, data in self.data.items():
                        if isinstance(tag, int) or (tag != "choose metadata" and tag[:5] != 'File_'):
                            try:
                                print(f'    {str(tag):26}: {data}')
                            except:
                                data = re.sub('[^a-zA-Z0-9 \n\.]', '', data)
                                self.data[tag] = data
                                print(f'    {str(tag):26}: {data}')
                    # print final line
                    print('    '+'-'*61)
                else:
                    print("    No metadata\n")
            
            # if file has pdf extension, process it
            elif ext == 'pdf':
                print('    '+'-'*26+'PDF INFO'+'-'*26)
                # read the pdf file
                pdf = pikepdf.Pdf.open(self.file)
                docinfo = pdf.docinfo
                for key, value in docinfo.items():
                    if str(value).startswith("D:"):
                        # pdf datetime format, convert to python datetime
                        value = transform_date(str(pdf.docinfo["/CreationDate"]))
                    print(f'    {key[1:]:26}: {value}')
                # print final line
                print('    '+'-'*61)    
            # if file has doc, docx extension, process it
            elif  ext == 'docx':
                print('    '+'-'*23+' DOCX INFO '+'-'*23)
                # read the doc/docx file
                filename = os.path.basename(self.file)
                doc:Document = docx.Document(self.file)
                props:CoreProperties = doc.core_properties
                metadata={}
                #metadata['Filepath'] = self.file
                #metadata['Filename'] = filename
                metadata.update({str(p):getattr(props, p) for p in dir(props) if not str(p).startswith('_')})
                for key, value in metadata.items():
                    print(f'    {key.capitalize():26}: {value}')
                # print final line
                print('    '+'-'*61)
            else:
                print(f"    Wrong file extension: .{ext}. Only valid extensions are .jpg, .jpeg, .png, .bmp, .gif, .docx, .pdf")
                print('    '+'-'*61)

    ###############
    # EXTRACT DATA
    ###############
    def extract_data(self):

        encod = ['ascii', 'latin_1', 'iso8859_2', 'iso8859_3', 'iso8859_4', 'iso8859_5', 'iso8859_6', 'iso8859_7', 'iso8859_8', 'iso8859_9', 'iso8859_10', 'iso8859_11', 'iso8859_13', 'iso8859_14', 'iso8859_15', 'iso8859_16', 'johab', 'koi8_r', 'koi8_t', 'koi8_u', 'kz1048', 'mac_cyrillic', 'mac_greek', 'mac_iceland', 'mac_latin2', 'mac_roman', 'mac_turkish', 'ptcp154', 'shift_jis', 'shift_jis_2004', 'shift_jisx0213', 'utf_7', 'utf_8', 'utf_8_sig']
        
        # extract basic file data
        self.data = {}
        self.data['choose metadata'] = "choose metadata from list"
        self.data['File_size'] = humanize.naturalsize(os.path.getsize(self.file))
        self.data['File_creation_time'] = datetime.fromtimestamp(os.path.getctime(self.file))
        self.data['File_modification_time'] = datetime.fromtimestamp(os.path.getmtime(self.file))
        #self.data['File_stats'] = os.stat(f)
        
        # extract exif metadata
        
        self.tags=[]

        try:
            self.image = Image.open(self.file)
            self.exifdata = self.image.getexif()
            
            if self.exifdata != {}:
                
                for tag_id,data in self.exifdata.items():
                    
                    tag = str(ExifTags.TAGS.get(tag_id, tag_id))
                    
                    if isinstance(data, bytes):
                        self.data[tag] = data.decode(encoding="utf_8", errors="replace")
                    else:
                        self.data[tag] = data
                    self.tags.append(tag)            
                
    
                for ifd_id in ExifTags.IFD:

                    try:
                        ifd = self.exifdata.get_ifd(ifd_id)
                        
                        if ifd_id == ExifTags.IFD.GPSInfo:
                            resolve = ExifTags.GPSTAGS
                        else:
                            resolve = ExifTags.TAGS

                        for k, data in ifd.items():
                            tag = str(resolve.get(k, k))
                            
                            if tag in self.data.keys():
                                break
                            
                            if isinstance(data, bytes):
                                self.data[tag] = data.decode(encoding="utf_8", errors="replace")
                            else:
                                self.data[tag] = data
                            self.tags.append(tag)
                            
                    except KeyError:
                        pass



                    """
                    try:
                        self.display.insert(END,f"    {tag:26}: {data}"+"\n")
                    except:
                        data = re.sub('[^a-zA-Z0-9 \n\.]', '', data)
                        self.data[tag] = data
                        self.display.insert(END,f"    {tag:26}: {data}"+"\n")
                self.display.insert(END,"    "+"-"*65)"""

                #self.display_data()
            else:
                pass
                #self.display.insert(END,'NO DATA')
        except:
            pass
            #self.display.insert(END,'ERROR')
            #self.display_data()


    ###############
    # DISPLAY  DATA
    ###############
    
    def display_file_info(self):
         # display file info
        self.display.insert(END,'    '+'-'*26+'FILE INFO'+'-'*26+"\n")
        
        for tag, data in self.data.items():
            if isinstance(tag, str) and tag != "choose metadata" :
                if tag[:5] == 'File_':
                    self.display.insert(END,f'    {tag:26}: {data}'+"\n")
        
    def display_exif_info(self):
        # display EXIF metadata if any
        self.display.insert(END,'    '+'-'*26+'EXIF INFO'+'-'*26+"\n")
        if len(self.data) > 4:
            for tag, data in self.data.items():
                if isinstance(tag, int) or (tag != "choose metadata" and tag[:5] != 'File_'):
                    try:
                        self.display.insert(END,f'    {str(tag):26}: {data}'+"\n")
                    except:
                        data = re.sub('[^a-zA-Z0-9 \n\.]', '', data)
                        self.data[tag] = data
                        self.display.insert(END,f'    {str(tag):26}: {data}'+"\n")
        else:
            self.display.insert(END,"    No metadata\n")
          
    def display_pdf_info(self):
        
        # if file has pdf extension, process it
        if self.file.split(".")[-1] == 'pdf':
            self.display.insert(END,'    '+'-'*26+'PDF INFO'+'-'*26+"\n")
            # read the pdf file
            pdf = pikepdf.Pdf.open(self.file)
            docinfo = pdf.docinfo
            for key, value in docinfo.items():
                if str(value).startswith("D:"):
                    # pdf datetime format, convert to python datetime
                    value = transform_date(str(pdf.docinfo["/CreationDate"]))
                self.display.insert(END,f'    {key[1:]:26}: {value}'+"\n")
        else:
            return
        
    def display_doc_info(self):
        
        # if file has doc, docx extension, process it
        ext = self.file.split(".")[-1]
        if  ext == 'docx':
            self.display.insert(END,'    '+'-'*23+' DOCX INFO '+'-'*23+"\n")
            # read the doc/docx file
            filename = os.path.basename(self.file)
            doc:Document = docx.Document(self.file)
            props:CoreProperties = doc.core_properties
            metadata={}
            #metadata['Filepath'] = self.file
            #metadata['Filename'] = filename
            metadata.update({str(p):getattr(props, p) for p in dir(props) if not str(p).startswith('_')})
            for key, value in metadata.items():
                self.display.insert(END,f'    {key.capitalize():26}: {value}'+"\n")
        else:
            return
 
    def display_data(self):
        
        #print(self.exifdata)
        #print(self.data)

        # clean scrolledText window
        self.display.delete('1.0',END)
        
        # display file info
        self.display_file_info()
        
        # display pdf file info
        self.display_pdf_info()
        
        # display doc/docx file info
        self.display_doc_info()
        
        # display EXIF metadata
        self.display_exif_info()
        
        # print final line
        self.display.insert(END,'    '+'-'*61)
        
        # if there is exif info, show button 'EDIT EXIF DATA'
        if len(self.data) > 4:
                # show Edit Metadata button
                self.btn_edit_meta = Button(self.ventana, text="EDIT EXIF", bg="yellow", command=self.edit_meta)
                self.btn_edit_meta.grid(row=3, column=3, sticky="we", columnspan=1)
        

    ###############
    # MODIFY - DELETE
    ###############
    def submit(self):
            if self.valores.get() != "choose metadata from list":
            
                if self.radio_var.get() == 'modify':
                    
                    
                    tag_tb_changed = self.dropdown_var.get() if self.dropdown_var.get() != "59932" else 59932
                    
                    for tag_id in self.exifdata:
                        if ExifTags.TAGS.get(tag_id, tag_id) == tag_tb_changed:
                            #print(type(self.exifdata.get(tag_id)))
                            if isinstance(self.exifdata.get(tag_id), bytes):
                                self.exifdata[tag_id] = bytes(self.valores.get(), 'utf-8')
                            elif isinstance(self.exifdata.get(tag_id), int):
                                self.exifdata[tag_id] = int(self.valores.get())
                            elif isinstance(self.exifdata.get(tag_id), float):
                                self.exifdata[tag_id] = float(self.valores.get())
                            elif isinstance(self.exifdata.get(tag_id), TiffImagePlugin.IFDRational):
                                self.exifdata[tag_id] = TiffImagePlugin.IFDRational(self.valores.get())
                            elif isinstance(self.exifdata.get(tag_id), tuple):
                                if isinstance(self.exifdata.get(tag_id)[0], TiffImagePlugin.IFDRational):
                                    self.exifdata[tag_id] = tuple([TiffImagePlugin.IFDRational(i) for i in self.valores.get().split(" ")])
                                elif isinstance(self.exifdata.get(tag_id)[0], int):
                                    self.exifdata[tag_id] = tuple([int(i) for i in self.valores.get().split(" ")])
                            else:
                                self.exifdata[tag_id] = self.valores.get()
                            self.data[self.dropdown_var.get()] = self.valores.get()
                            print(f"MODIFIED METADATA {self.dropdown_var.get()} = {self.valores.get()}")
                            messagebox.showinfo(message=f"EXIF data '{self.dropdown_var.get()}' value modified to '{self.valores.get()}'", title="Modified EXIF data")
                            self.display_data()
                            break
                    #Save button
                    self.btn_save = Button(self.ventana, text= "Save changes to file", command= self.save_file)
                    self.btn_save.grid(pady=10, row=5, column=5, sticky="w", columnspan=2)
                            
                    
                  
                    
                elif self.radio_var.get() == 'delete':
                    print(f"DELETE {self.dropdown_var.get()}")
                    if messagebox.askokcancel(message=f"Are you sure you want to delete the {self.dropdown_var.get()} metadata?", title="Delete EXIF data"):
                        pass
                else:
                    messagebox.showinfo(message=f"Please chose an option (Modify or Delete).")
            else:    
                messagebox.showinfo(message=f"Please chose an EXIF data to {self.radio_var.get()}.")
    
    ####################
    # SAVE FILE
    ####################
    def save_file(self):
        f = asksaveasfile(initialfile = self.file.split('/')[-1] ,filetypes=[("Image files",".jpg .jpeg .png .bmp .gif"),("Document files",".docx .pdf .doc")])
        if f and f != "":
            print(self.exifdata)
            self.image.info["exif"] = self.exifdata
            try:
                self.image.save(f)
                self.image.close()
                messagebox.showinfo(message=f"Modified EXIF data saved.")
            except:
                messagebox.showerror(title="Error saving changes to file", message=f"Modified EXIF data NOT saved. Something went wrong.")
                self.image.close()
            self.btn_save.destroy()
    
    
    ##################################################
    # CHECK DROP DOWN LIST STATUS & UPDATE ENTRY FIELD
    ##################################################
    def check(self,*args):
            self.valores.set(self.data[self.dropdown_var.get()])
    
    
    #########################
    # EDIT EXIF MENU WINDOW
    #########################
    def edit_meta(self):

        if len(self.data) >4:
            self.btn_edit_meta.destroy()
            
            self.dropdown_var.set('choose metadata')
            self.dropdown_var.trace_add("write", self.check)

            self.valores.set("choose metadata from list")
            
            #list available tags only
            self.dropdown = OptionMenu(self.ventana, self.dropdown_var, *sorted(list(dict.fromkeys(self.tags))))
            # Lists all possible tags
            #self.dropdown = OptionMenu(self.ventana, self.dropdown_var, *sorted(ExifTags.TAGS.values()))
            
            self.dropdown.grid(padx=10, pady=10,row=4, column=0, sticky='we', rowspan=2)

            self.radio_var.set("modify metadata")

            self.radio_modify = Radiobutton(self.ventana, text='Modify',  variable=self.radio_var, value='modify')
            self.radio_modify.grid(row=4, column=2, sticky="w")
            
            self.radio_delete = Radiobutton(self.ventana, text='Delete',  variable=self.radio_var, value='delete')
            self.radio_delete.grid(row=5, column=2, sticky="w")
                
            self.edit_label = Label(self.ventana, text="New Value:")
            self.edit_label.grid(row=4, column=3, sticky="e")
            
            self.edit_entry = Entry(self.ventana,textvariable=self.valores,  width= 40)
            self.edit_entry.grid(row=4, column=5, sticky="w", columnspan=2)
            
            self.ok_btn = Button(self.ventana,text="SUBMIT MODIFY or DELETE",command=self.submit)
            self.ok_btn.grid(padx=10, pady=10, row=6, column=0, sticky="we", columnspan=7)


    ###############
    # QUIT
    ###############
    def quit(self):
        if self.image:
            self.image.close()
        self.ventana.destroy()

 
if __name__=="__main__":
     # Store input arguments in a list
    arguments = sys.argv
    
    # If arguments are provided, encode. Else, do nothing
    if len(arguments) > 1:
        
        for file in arguments[1:]:
            App(file)       
        
    else:
        App()
