from tkinter import *
from tkinter.simpledialog import askstring
from tkinter import messagebox as msgbox
from tkinter import filedialog as fd
import json
from PIL import Image, ImageTk
from datetime import datetime
import img_utils
import PIL
import os
import utils


def show_enc_help():
    """
    Shows the information about encryption strictness levels

    :return: None
    """
    msg = ("Security Level 0 : \nThe encryption key will be included in image, any user having this tool can extract from such images.\n\n"
           "Security Level 1 : \nKey will not be included in image. While extracting from image, user will be prompted to enter the key, this key will be used to decrypt the text even if the key is incorrect. \n"
           "Needless to state: if the key is incorrect, the extracted text will look like garbage text\n\n"
           "Security Level 2 : \nKey will not be included in image, but in this case encryption key should be entered correctly while extracting, otherwise user will not be provided any extracted text.\n\n"
           "Note : \nWhile manually entering key, you need not enter numbers separated by commas (like in auto generated key), you are supposed to use the key like a \"password\" for the image,"
           " you can just enter the text in that area.")
    msgbox.showinfo(title="Security Levels",message=msg)


def hide_text(img_path_var:StringVar,txtarea:Text,keyvar:StringVar,enc_strc:IntVar):
    """
    Takes the text from txtarea, key from keyvar, encryption strictness level from enc_strc
    and embeds the data in image and saves it

    :param txtarea:
    :param keyvar:
    :param enc_strc:
    :return: None
    """
    text = txtarea.get(1.0,END)
    text = text[:-1] if text[-1]=='\n' else text
    key_val = keyvar.get()
    enc_val = enc_strc.get()
    encst_tup = tuple()

    if text == '' or key_val == '':
        return msgbox.showerror(title="Fields empty",message="Please fill all the required fields")

    match enc_val:
        case 0:
            encst_tup = (0,0)
        case 1:
            encst_tup = (1,0)
        case 2:
            encst_tup = (1,1)

    file = img_path_var.get()
    if file:
        img = Image.open(file)
    else:
        return msgbox.showinfo(title="File not selected",message="You haven't selected any image file. please select an image file first")

    if not msgbox.askyesno(title="Confirmation",message=f"Security Level {enc_val} ?\nSelected image : {file}\nare you sure you want to proceed?"):
        return

    try:
        img = img_utils.hide_data(img=img,message=text,key=key_val,enc_tup=encst_tup)
    except OverflowError as err:
        return msgbox.showerror(title="Text is too long",message=err.args[0])

    file = fd.asksaveasfilename(title="Save the created image as",initialdir=os.getcwd(),initialfile=f"Steganos_{str(datetime.now().timestamp()).split('.')[0]}")
    if file!='':
        sf = file.split(".")
        if len(sf)==1:
            sf.append('')
        sf[-1] = 'png'
        file = f"{''.join(sf[:-1])}.{sf[-1]}"
        img.save(file,'png')
        msgbox.showinfo(title="Image created and saved",message=f"Successfully created and saved image at : {file}")

def open_image(textarea:Text,stego_img_path:StringVar):
    """
    Opens image and extracts the image's data and writes it in textarea

    :param textarea:
    :return: None
    """
    data = textarea.get(1.0,END)
    file = fd.askopenfile(title="Open image to extract text")
    if file:
        try:
            img = Image.open(file.name,'r')
            _orient,*enctup = img_utils.get_enc_tup(img)
            enctup = tuple(enctup)
            inpkey = ''
            rawtext = img_utils.extract_data(img)
            stego_img_path.set(file.name)
            if enctup == (0,0):
                text = ' '.join(rawtext.split(" ")[1:-1])
                textarea.config(state=NORMAL)
                textarea.delete(1.0,END)
                textarea.insert(END,text)
                textarea.config(state=DISABLED)
            elif enctup == (1,0):
                inpkey = askstring(title="Key required (level 1)",prompt="Enter the encryption key :\t\t\t")
                if inpkey=='' or (not inpkey):
                    return msgbox.showerror(title="Error",message="cannot extract text without key")
                inpkey = utils.get_key(inpkey)
                text = utils.deciph(text=rawtext,key=inpkey)
                tlist = text.split(' ')
                if tlist[0] == img_utils.SIGNATURE_TEXT and (tlist[0] == tlist[-1]):
                    text = ' '.join(text.split(" ")[1:-1])
                else:
                    text = text[len(img_utils.SIGNATURE_TEXT)+1:-(len(img_utils.SIGNATURE_TEXT)+1)]
                textarea.config(state=NORMAL)
                textarea.delete(1.0,END)
                textarea.insert(END,text)
                textarea.config(state=DISABLED)
            elif enctup == (1,1):
                inpkey = askstring(title="Key required (level 2)", prompt="Enter the encryption key :\t\t\t")
                if inpkey=='' or (not inpkey):
                    return msgbox.showerror(title="Error",message="cannot extract text without key")
                inpkey = utils.get_key(inpkey)
                text = utils.deciph(text=rawtext, key=inpkey)
                tlist = text.split(' ')
                if tlist[0] == img_utils.SIGNATURE_TEXT and (tlist[0] == tlist[-1]):
                    text = ' '.join(text.split(" ")[1:-1])
                else:
                    textarea.config(state=DISABLED)
                    return msgbox.showerror(title="Incorrect key",message="Provided key is incorrect, cannot extract data from image")
                textarea.config(state=NORMAL)
                textarea.delete(1.0,END)
                textarea.insert(END,text)
                textarea.config(state=DISABLED)
            return msgbox.showinfo(title="Success",message="Succesfully extracted text from image!")
        except Exception as err:
            if isinstance(err,PIL.UnidentifiedImageError):
                return msgbox.showerror(title="Invalid file type for image",message="Selected file is not an image file.")
            elif isinstance(err,TypeError):
                return msgbox.showerror(title="Error",message=err.args[0])
            elif isinstance(err,OSError):
                if "Truncated File Read" in err.args:
                    return msgbox.showerror(title="Error",message="Image file is corrupted")
                else:
                    raise err
            else:
                raise err

def show_img(root:Tk,img_path:StringVar):
    ipath = img_path.get()
    max_size = 600
    if ipath:
        img = Image.open(ipath)
        w,h = img.size
        img = img_utils.resizer(img=img,max_size=max_size)
        w1,h1 = img.size
        tkimg = ImageTk.PhotoImage(img)
        im_win = Toplevel(master=root)
        path_var = StringVar(value=f"{ipath} - ({w}x{h})")
        im_win.title(f"Steganos - Image Preview")
        im_win.resizable(width=False, height=False)
        im_win.geometry(f"{750}x{h1+100}")
        im_win.geometry(f"700x{h1+100}")
        im_win.config(background='#2F3136')
        im_label = Label(master=im_win,image=tkimg,background='#2F3136')
        im_path = Entry(master=im_win,textvariable=path_var,background='#2F3136',foreground='white',justify=CENTER,state='readonly',
                        readonlybackground='#2F3136',borderwidth=0,selectbackground='black',width=120)
        im_label.photo = tkimg
        im_label.pack(pady=10,padx=10,anchor=N)
        im_path.pack(anchor=N)
        im_win.grab_set()
        im_win.focus_set()
    else:
        msgbox.showinfo(title="File not selected",message="You haven't selected any image file. please select an image file first")


def select_img(img_path:StringVar):
    file = fd.askopenfile(title="Open image file")
    if file:
        try:
            Image.open(file.name)
        except PIL.UnidentifiedImageError:
            file.close()
            msgbox.showerror(title="Error", message="Selected file is not an image file.")
        else:
            img_path.set(file.name)
            file.close()
            msgbox.showinfo(title="Image selected",message="Image file selected successfully.")


def get_file_data(textarea:Text):
    """
    reads the data from selected file and sets the value of stringvar as the data

    :param textarea:
    :return: None
    """
    try:
        file = fd.askopenfile(title="Open file")
        if file:
            data = file.read()
            file.close()
            textarea.delete(1.0,END)
            textarea.insert(1.0,data)
    except UnicodeDecodeError:
        msgbox.showerror(title="Invalid file type",message="Selected file does not contain text data.")


def copy_text(txtarea:Text,root:Tk):
    """
    copies the text from txtarea to clipboard

    :param txtarea: Text
    :param root: Tk
    :return: None
    """
    txt = txtarea.get(1.0,END)
    txt = txt[:-1] if txt[-1]=='\n' else txt
    if txt:
        root.clipboard_clear()
        root.clipboard_append(txt)
        root.update()

def save_txt_file(txtarea:Text):
    """
    takes text from txtarea and writes it into a file and saves it

    :param txtarea:
    :return: None
    """
    text = txtarea.get(1.0,END)
    text = text[:-1] if text[-1] == '\n' else text
    if text == '':
        return msgbox.showerror(title="Error",message="Text area is empty")
    else:
        file = fd.asksaveasfilename(title="Save the created image as", initialdir=os.getcwd())
        if file:
            sf = file.split('.')
            if len(sf)==1:
                sf.append('')
            sf[-1] = 'txt'
            file = f"{''.join(sf[:-1])}.{sf[-1]}"
            with open(file,'w') as f:
                f.write(text)
            msgbox.showinfo(title="Success",message=f"Text file successfully saved at: {file}")

def copy_key(s_var:StringVar,root:Tk):
    """
    copies the text from StringVar variable and appends to clipboard

    :param val:
    :param root:
    :return: None
    """
    txt = s_var.get()
    if txt != "":
        root.clipboard_clear()
        root.clipboard_append(txt)
        root.update()

def get_random_key(entry_var:StringVar):
    """
    sets the value of given StringVar as randomly generated key.

    :param entry_var: StringVar
    :return: None
    """
    entry_var.set(f"{utils.random_KeyGen(20)}")
