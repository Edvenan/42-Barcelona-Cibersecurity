#!/home/edvenan/anaconda3/envs/42/bin/ python

import PySimpleGUI as sg
import os.path
from ft_otp import *

#  Widget example: sg.In(expand_x=True, enable_events=True, key="-TXT_KEY-")

##########################
# window construction: 
##########################

# Main colum 1
key_column_1 = [
    [sg.Text("Enter Shared Secret Key:")],
    [sg.Text("Plain Text", size=(9,1)), sg.In(size=(35, 1), enable_events=True, key="-TXT_KEY-"), sg.Button('x', key='-X1-'), sg.Text("min 32 chars", font=('Arial', 8),text_color='yellow',visible=False, key='-ERR1-')],
    [sg.Text("HEX", size=(9,1)), sg.Input(size=(35, 1), enable_events=True, key="-HEX_KEY-"), sg.Button('x', key='-X2-'), sg.Text("", font=('Arial', 8), text_color='yellow',visible=False, key='-ERR2-')],
    [sg.Text("Generate random 32-Byte key:")],
    [sg.Button(' Generate', key='-GEN_RND-'), sg.Text(text="XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX", auto_size_text=True, size=(39, 1), key='-RAND_KEY-')],
    
    [sg.HSeparator()],
    
    [sg.Text("Algorithm: "), sg.Radio("SHA-1", "ALG", default=True, key="-SHA1-"), 
        sg.Radio("SHA-256", "ALG", key="-SHA256-"), sg.Radio("SHA-512", "ALG", key="-SHA512-"),
        sg.Text("Digits: "), sg.Spin(values=[str(i) for i in [6,7,8]], initial_value="6", key="-DIGITS-")],
    
    [sg.HSeparator()],
    
    [sg.Text("Issuer:", size=(4,1)), sg.Input(size=(20, 1), enable_events=True, key="-ISSUER-"), sg.Button('x', key='-X3-'),
    sg.Text("User:", size=(4,1)), sg.Input(size=(20, 1), enable_events=True, key="-USER-"), sg.Button('x', key='-X4-')],
    
    
    [sg.HSeparator()],
    
    [sg.Column( [[sg.Button("Generate TOTP", key='-TOTP-', font=('Arial Bold', 15), expand_x=True, pad=((0,0),(10,0)))],
                 [sg.Text(text='Please enter a Shared Secret Key (Text, Hex, Random)', key='-ERR3-', visible=False, text_color='yellow', expand_x=True, justification='center', pad=((0,0),(10,0)))]
                 ],expand_x= True, expand_y= True,  vertical_alignment='center')]
]

key_column_2 = [
    [sg.Text(text="- Please enter shared secret key -", expand_x=True, key="-TOUT-")],
    [sg.Image(key="-IMAGE-", filename="", subsample=4, expand_x = True, expand_y= True)],
    [sg.Text(key='-FT_OTP-',text='--- ---', font=('Arial Bold', 20), size=17, expand_x=True, justification='center')],
    
    [sg.HSeparator()],
    
    [sg.Text(text="Output from OathTool:")],
    [sg.Text(key='-OATH_TOTP-', text='--- ---', font=('Arial Bold', 20),  expand_x=True, justification='center')]
]

##########################
# ----- Full layout -----
##########################
layout = [ [ sg.Column(key_column_1, vertical_alignment='top', size=(450, 325)), 
            sg.VSeperator(), 
            sg.Column(key_column_2, vertical_alignment='center', size=(300, 325))] ]
window = sg.Window("TOTP Generator", layout)


#####################################################
# function that does the following:
# 1) process Shared Secret Key chosen by user
# 2) generate TOTP based on chosen paramenters
# 3) generate URI based on user input
# 4) generate QR code for sharing Shared Secret Key
# 5) verify TOTP vs the one produced by OathTool
#####################################################
def do_the_magic(key):
    
    # read and assign chosen algorithm 
    crypto = 'sha1' if values['-SHA1-'] else ('sha256' if values['-SHA256-'] else 'sha512')
    # read and assign chosen digits 
    returnDigits = values['-DIGITS-']
    # read and assign issuer & user 
    issuer = values['-ISSUER-']
    user = values['-USER-']
    
    # convert key to HEX 
    hex_key=string2hex(key)
    
    # add header title to QR and TOTP section
    window['-TOUT-'].update("Generated TOTP and QR:")
    
    # generate URI
    uri = create_URI(issuer, user, hex_key)
    
    # create QR from URI and visualize it
    create_QR(uri)
    window['-IMAGE-'].update(filename="qr.png", subsample=3)
    
    # generate TOTP
    otp = generateTOTP(hex_key, returnDigits, crypto)
    
    # generate TOPT with OathTool
    oath_totp = get_oathtool_totp(hex_key, crypto, returnDigits)

    # Visualize both generated and OathTool's TOTPs
    if returnDigits == '6':
        final_otp = f"{otp[:3]} {otp[3:]}"
        final_oath_totp = f"{oath_totp[:3]} {oath_totp[3:]}"
    elif returnDigits == '7':
        final_otp = f"{otp[:3]} {otp[3:4]} {otp[4:]}"
        final_oath_totp = f"{oath_totp[:3]} {oath_totp[3:4]} {oath_totp[4:]}"
    elif returnDigits == '8':
        final_otp = f"{otp[:3]} {otp[3:5]} {otp[5:]}"
        final_oath_totp = f"{oath_totp[:3]} {oath_totp[3:5]} {oath_totp[5:]}"
    
    window['-FT_OTP-'].update(final_otp)
    window['-OATH_TOTP-'].update(final_oath_totp)


#######################
# Run the Event Loop
#######################

while True:
    event, values = window.read()
    print("Event= ",event," Values= ", values)
    
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    
    # Folder name was filled in, make a list of files in the folder
    if event == "-TXT_KEY-":
        # validate input
        # must be at least a 32-byte key
        if values['-TXT_KEY-']:
            window['-HEX_KEY-'].update('',disabled=True)
            window['-RAND_KEY-'].update('XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX')
            window['-ERR3-'].update(visible = False)
            if len(values['-TXT_KEY-']) < 32:
                window['-ERR1-'].update(visible=True)
            else:
                window['-ERR1-'].update(visible=False)
        else:
            window['-HEX_KEY-'].update(disabled=False)
            window['-ERR1-'].update(visible=False)
            window['-ERR3-'].update(visible=False)
 
    elif event == "-HEX_KEY-":
        # validate input
        # must be at least a 64-char HEX key
        if values['-HEX_KEY-']:
            window['-TXT_KEY-'].update('',disabled=True)
            window['-RAND_KEY-'].update('XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX')
            window['-ERR3-'].update(visible = False)
            if any([values['-HEX_KEY-'][i].lower() not in '1234567890abcdef' for i in range (len(values['-HEX_KEY-']))]):
                window['-ERR2-'].update('not a hex key', visible=True)
            elif len(values['-HEX_KEY-']) < 64:
                window['-ERR2-'].update('min 64 chars', visible=True)
            else:
                window['-ERR2-'].update(visible=False)
        else:
            window['-TXT_KEY-'].update(disabled=False)
            window['-ERR2-'].update(visible=False)
            window['-ERR3-'].update(visible=False)
            
    elif event == "-X1-":
        # erase text field and enable all others
        # erase also any error msg related to '-TXT_KEY-'
        window['-TXT_KEY-'].update('')
        window['-HEX_KEY-'].update(disabled=False)
        window['-ERR1-'].update(visible=False)
        window['-ERR3-'].update(visible=False)
        
    elif event == "-X2-":
        # erase text field and enable all others
        # erase also any error msg related to '-HEX_KEY-'
        window['-HEX_KEY-'].update('')
        window['-TXT_KEY-'].update(disabled=False)
        window['-ERR2-'].update(visible=False)
        window['-ERR3-'].update(visible=False)
    
    elif event == "-X3-":
        # erase text field 
        window['-ISSUER-'].update('')

    elif event == "-X4-":
        # erase text field 
        window['-USER-'].update('')

    elif event == "-GEN_RND-":
        # generate random 32-byte key
        # erase all other input fields and error msgs
        window['-HEX_KEY-'].update('',disabled=False)
        window['-TXT_KEY-'].update('',disabled=False)
        window['-ERR1-'].update(visible=False)
        window['-ERR2-'].update(visible=False)
        window['-ERR3-'].update(visible = False)
        key = generate_random_key()
        window['-RAND_KEY-'].update(f'{key[:4]}-{key[4:8]}-{key[8:12]}-{key[12:16]}-{key[16:20]}-{key[20:24]}-{key[24:28]}-{key[28:32]}')
            
    elif event == "-TOTP-":
        # if there is any error visible relative to the key
        # raise an error
        if window['-ERR1-'].visible or window['-ERR2-'].visible:
            window['-ERR3-'].update(visible=True)
        
        else:
        
            if values["-TXT_KEY-"] != '':
                key = values["-TXT_KEY-"]
                do_the_magic(key)
            
            elif values["-HEX_KEY-"] != '':
                key = hex2string(values["-HEX_KEY-"])
                do_the_magic(key)
            
            elif window["-RAND_KEY-"].get() != 'XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX':
                do_the_magic(key)
                
            else:
                window['-ERR3-'].update(visible=True)

window.close()