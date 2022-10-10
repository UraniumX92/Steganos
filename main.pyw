"""
    Steganography Project
    Project Name : Steganos

    > Functionality:
        for each character in given string:
            character will be converted into ascii number
            then the number will be converted to 8-bit binary
            set of 3 bits will be stored in each pixel, third pixel will have 1 empty place left,
            this empty place will be used to signal the stoppage of message.

    Features:
        > Manually enter encryption key?
            Yes : only encrypted text will be stored, receiving user will have to enter key manually to extract message.
            No : encryption key will be randomly generated and will be stored in picture with metadata
        > file for messages:
            save the extracted message to a .txt file
            read the text file and store the content of file as message.
"""

from tkinter import *
from tkinter import filedialog as fd
from PIL import Image as Img
import commands
import random
import img_utils
import utils
import os

# CONSTANTS
green_Tcolor = '#10AD14'
BACKGROUND = '#2F3136'
darker_BG = '#222222'
lighter_BG = '#55585E'
xs_padding = 3
s_padding = 5
m_padding = 10
header_font_tuple = ('consolas',20,'bold')
header_font_tuple2 = ('consolas',18,'bold')
txt_font_tuple = ('consolas',12)
label_font_tuple = ('Segoe UI Symbol',12,'bold')
btn_font_tuple = ('Segoe UI Symbol', 10)
label_text_color = 'white'

# root window configurations
root = Tk()
root.geometry("1200x700")
root.resizable(width=False,height=False)
root.config(background=BACKGROUND)
root.title("Steganos : Application by Syed Usama")

# Variables
enc_strictness = IntVar()
key = StringVar()
img_to_be_used = StringVar()
img_to_extract = StringVar()

# ---- creating and packing GUI elements ---- #

# Title Label
t_label = Label(text="Steganos : Secretly hide your text in an image", font=header_font_tuple, background=BACKGROUND, foreground=label_text_color)
t_label.pack(side=TOP,pady=m_padding,padx=m_padding,ipady=s_padding,ipadx=s_padding)

# Input Frame
inpFrame = Frame(master=root,background=BACKGROUND)
inpFrame.pack(side=TOP,anchor=N)

# Input text area
inp_label = Label(master=inpFrame, text="Enter the text :", font=label_font_tuple, background=BACKGROUND, foreground=label_text_color)
inp_label.grid(row=0,column=0,pady=s_padding,padx=s_padding,sticky=NE)
inp_field = Text(master=inpFrame,insertbackground=green_Tcolor,font=txt_font_tuple,wrap=NONE,foreground=green_Tcolor, background=darker_BG, height=10, width=110)
inp_field.grid(row=0,column=1,padx=s_padding,pady=s_padding)


# Key Label Entry
key_label = Label(master=inpFrame, text="Enter the key :", font=label_font_tuple, background=BACKGROUND, foreground=label_text_color)
key_label.grid(row=1,column=0,pady=s_padding,padx=s_padding,sticky=NE)
key_entry =Entry(master=inpFrame,textvariable=key,width=110,background=darker_BG,font=txt_font_tuple,foreground=green_Tcolor,insertbackground=green_Tcolor,readonlybackground=BACKGROUND)
key_entry.grid(row=1,column=1,padx=s_padding,pady=s_padding,ipady=xs_padding)

radio_label = Label(master=inpFrame, text="Encryption method: ", font=label_font_tuple, background=BACKGROUND, foreground=label_text_color)
radio_label.grid(row=2,column=0,sticky=NE)

# Radio Frame for storing radio buttons
btnFrame = Frame(master=inpFrame, background=BACKGROUND, width=110)
btnFrame.grid(row=2, column=1)

ran_key_btn = Button(master=btnFrame, text="Generate random key", activebackground=lighter_BG, font=btn_font_tuple, relief=RAISED, foreground=label_text_color, background=darker_BG, command=lambda: commands.get_random_key(key))
ran_key_btn.grid(row=0,column=0,padx=s_padding,pady=s_padding)

# Radio buttons for encryption strictness levels
r0 = Radiobutton(master=btnFrame, text="Security Level 0", variable=enc_strictness, font=label_font_tuple, background=BACKGROUND, activebackground=lighter_BG, value=0)
r0.grid(row=0,column=1,padx=s_padding,pady=s_padding)

r1 = Radiobutton(master=btnFrame, text="Security Level 1", variable=enc_strictness, font=label_font_tuple, background=BACKGROUND, activebackground=lighter_BG, value=1)
r1.grid(row=0,column=2,padx=s_padding,pady=s_padding)

r2 = Radiobutton(master=btnFrame, text="Security Level 2", variable=enc_strictness, font=label_font_tuple, background=BACKGROUND, activebackground=lighter_BG, value=2)
r2.grid(row=0,column=3,padx=s_padding,pady=s_padding)

# help button which shows information about different encryption methods.
help_btn = Button(master=btnFrame, text="What are these security levels?", activebackground=lighter_BG, font=btn_font_tuple, relief=RAISED, foreground=label_text_color, background=darker_BG, command=lambda: commands.show_enc_help())
help_btn.grid(row=0,column=4,padx=s_padding,pady=s_padding)
# -- End of Radio Frame -- #

# Buttons
cpy_key_btn = Button(master=btnFrame, text="Copy key to clipboard", activebackground=lighter_BG, font=btn_font_tuple, relief=RAISED, foreground=label_text_color, background=darker_BG, command=lambda: commands.copy_key(key, root))
cpy_key_btn.grid(row=1, column=0, pady=s_padding, padx=s_padding)

opntxt_btn = Button(master=btnFrame, text="Open a file to load text", activebackground=lighter_BG, font=btn_font_tuple, relief=RAISED, foreground=label_text_color, background=darker_BG, command=lambda: commands.get_file_data(inp_field))
opntxt_btn.grid(row=1, column=1, pady=s_padding, padx=s_padding)

opn_img_btn = Button(master=btnFrame, text="Select Image", activebackground=lighter_BG, font=btn_font_tuple, relief=RAISED, foreground=label_text_color, background=darker_BG, command=lambda:commands.select_img(img_to_be_used))
opn_img_btn.grid(row=1,column=2,pady=s_padding,padx=s_padding)

show_img_btn = Button(master=btnFrame, text="Show Image", activebackground=lighter_BG, font=btn_font_tuple, relief=RAISED, foreground=label_text_color, background=darker_BG, command=lambda:commands.show_img(root, img_to_be_used))
show_img_btn.grid(row=1,column=3,padx=s_padding,pady=s_padding)

embedtxt_btn = Button(master=btnFrame, text="Hide text in an image", activebackground=lighter_BG, font=btn_font_tuple, relief=RAISED, foreground=label_text_color, background=darker_BG, command=lambda: commands.hide_text(img_to_be_used,inp_field, key, enc_strictness))
embedtxt_btn.grid(row=1, column=4, pady=s_padding, padx=s_padding)

# ---- End of Input Frame ---- #

# Frame for extracting operations
extFrame = Frame(master=root,background=BACKGROUND)
extFrame.pack(side=TOP,anchor=N)

ext_title_label = Label(master=extFrame, text="Extract hidden text from image :", font=header_font_tuple2, background=BACKGROUND, foreground=label_text_color)
ext_title_label.grid(row=0,column=1,pady=xs_padding,padx=xs_padding,sticky=N)

ext_label = Label(master=extFrame, text="Extracted text :", font=label_font_tuple, background=BACKGROUND, foreground=label_text_color)
ext_label.grid(row=1,column=0,pady=s_padding,padx=s_padding,sticky=NE)
ext_field = Text(master=extFrame,state=DISABLED,wrap=NONE,insertbackground=green_Tcolor,font=txt_font_tuple, foreground=green_Tcolor, background=darker_BG, height=10, width=110)
ext_field.grid(row=1,column=1,padx=s_padding,pady=s_padding,sticky=N)

e_btnFrame = Frame(master=extFrame,background=BACKGROUND)
e_btnFrame.grid(row=2,column=1)

copyext_btn = Button(master=e_btnFrame, text="Copy extracted text to clipboard", font=btn_font_tuple, foreground=label_text_color, background=darker_BG, relief=RAISED, command=lambda : commands.copy_text(ext_field, root))
copyext_btn.grid(row=0, column=0, pady=s_padding, padx=s_padding)

opnimg_btn = Button(master=e_btnFrame, text="Open image file to extract text", font=btn_font_tuple, foreground=label_text_color, background=darker_BG, relief=RAISED, command=lambda : commands.open_image(ext_field,img_to_extract))
opnimg_btn.grid(row=0, column=1, pady=s_padding, padx=s_padding)

show_eimg_btn = Button(master=e_btnFrame, text="Show Image", activebackground=lighter_BG, font=btn_font_tuple, relief=RAISED, foreground=label_text_color, background=darker_BG, command=lambda:commands.show_img(root, img_to_extract))
show_eimg_btn.grid(row=0,column=2,pady=s_padding,padx=s_padding)

savetxt_btn = Button(master=e_btnFrame, text="Save extracted text in a file", font=btn_font_tuple, foreground=label_text_color, background=darker_BG, relief=RAISED, command=lambda : commands.save_txt_file(ext_field))
savetxt_btn.grid(row=0, column=3, pady=s_padding, padx=s_padding)

# ---- End of Extracting frame ---- #

root.mainloop()