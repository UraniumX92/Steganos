# Steganos
### Hide your text in image

A Steganography project, steganós  meaning "covered or concealed", and - graphia  meaning "writing"


A GUI tool built using python, tkinter, PIL
 
* Hide your text in image using this tool
  * extra layer of encryption is used while hiding the data to ensure the security
  * there are 3 security levels from which a user can select during hiding the data
  * do not forget the encryption key you used if you selected security level 1 or 2
  * Image before hiding data and image after hiding data will look identical.
* Extract the text from images in which text was hidden using this very tool.
  * for security level 1 and 2, user will be prompted to enter the encryption key.
* For security level 2:
  * a special method is used to recognize the correctness of the provided key, this method cannot know the actual text which is hidden in image, but it only checks some signature text added by program automatically,
  * this signature text is kept private and secret for obvious reasons.
