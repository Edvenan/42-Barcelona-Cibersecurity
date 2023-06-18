# Stockholm Project

The **WannaCry ransomware** attack, which occurred in May 2017, targeted various file types by encrypting them and appending specific file extensions to the affected files.

The file extensions that were commonly associated with the WannaCry attack include:

**file_extensions** = ['.123', '.3dm', '.3ds', '.3g2', '.3gp', '.602', '.7z', '.accdb', '.aes', '.ai', '.arc', '.asc', '.asf', '.asm', '.asp', '.avi', '.backup', '.bak', '.bat', '.bmp', '.brd', '.bz2', '.c', '.cab', '.cc', '.cdr', '.cer', '.cfg', '.cfgx', '.chm', '.class', '.cmd', '.cpp', '.crt', '.cs', '.csr', '.csv', '.db', '.dbf', '.dch', '.dif', '.dip', '.djvu', '.doc', '.docb', '.docm', '.docx', '.dot', '.dotm', '.dotx', '.dsp', '.dvd', '.dwg', '.eml', '.fla', '.flv', '.frm', '.gif', '.gpg', '.h', '.hpp', '.htm', '.html', '.hwp', '.ibd', '.iso', '.jar', '.java', '.jpeg', '.jpg', '.js', '.jsp', '.key', '.lay', '.lay6', '.ldf', '.lic', '.lnk', '.m', '.m3u', '.m4u', '.max', '.mdb', '.mdf', '.mid', '.mkv', '.mml', '.mov', '.mp3', '.mp4', '.mpeg', '.mpg', '.ms11', '.ms11 (Security copy)', '.mscz', '.msg', '.myd', '.myi', '.nef', '.odb', '.odg', '.odp', '.ods', '.odt', '.onetoc2', '.ost', '.otg', '.otp', '.ots', '.ott', '.p12', '.paq', '.pas', '.pdf', '.pem', '.php', '.pl', '.png', '.pot', '.potm', '.potx', '.ppam', '.pps', '.ppsm', '.ppsx', '.ppt', '.pptm', '.pptx', '.ps1', '.psd', '.pst', '.pub', '.py', '.pyc', '.pyw', '.qcow2', '.rar', '.rb', '.rtf', '.sch', '.sh', '.sln', '.sql', '.sqlite3', '.sqlitedb', '.stc', '.std', '.sti', '.stw', '.svg', '.swf', '.sxc', '.sxd', '.sxi', '.sxm', '.sxw', '.tar', '.tbk', '.tgz', '.tif', '.tiff', '.txt', '.uop', '.uot', '.vb', '.vbs', '.vcd', '.vdi', '.vmdk', '.vmx', '.vob', '.vsd', '.vsdx', '.wav', '.wb2', '.wk1', '.wks', '.wma', '.wmv', '.wpd', '.wps', '.x11', '.x3f', '.xis', '.xla', '.xlam', '.xlk', '.xlm', '.xlr', '.xls', '.xlsb', '.xlsm', '.xlsx', '.xlt', '.xltm', '.xltx', '.xlw', '.xml', '.xps', '.xxx', '.zip']


Our script will walk through the target's /home/$USER/infection folder and subfolders looking for files that meet the target extentions, it will append to those files the '.ft' extension (unless they have it already) and it will then encrypt them using a 16-char (or longer) secret key.

We will convert our secret key to 32 URL-safe base64-encoded bytes:

A key that is 32 URL-safe base64-encoded bytes refers to a cryptographic key that is 32 bytes long and encoded using URL-safe base64 encoding.

In cryptography, keys are typically generated as random sequences of bytes, and they are used to encrypt and decrypt data. The length of the key is important for the security and strength of the encryption algorithm being used.

URL-safe base64 encoding is a variant of base64 encoding that ensures the resulting encoded string can be safely used in URLs without any encoding issues. It replaces certain characters (e.g., '+' and '/') with URL-safe alternatives (e.g., '-' and '_').

Then, using Fernet function from Python's Cryptography library, we will create a cipher that will allow us to encrypt and decrypt the target files.

The Fernet function is a part of the cryptography library in Python, specifically in the 'cryptography.fernet' module. It is used for symmetric encryption and decryption using the Fernet symmetric encryption scheme.

Fernet is a high-level cryptographic symmetric encryption scheme that provides a simple and secure way to encrypt and decrypt data. It uses symmetric key encryption, which means the same key is used for both encryption and decryption.

The Fernet function provides a simple interface to encrypt and decrypt data using the Fernet symmetric encryption scheme. It takes a key as input and returns a Fernet object that can be used for encryption and decryption operations.

Fernet is built on top of a number of standard cryptographic primitives. Specifically it uses:

-AES in CBC mode with a 128-bit key for encryption; using PKCS7 padding.
-HMAC using SHA256 for authentication.
-Initialization vectors are generated using os.urandom().

**Limitations**
Fernet is ideal for encrypting data that easily fits in memory. As a design feature it does not expose unauthenticated bytes. This means that the complete message contents must be available in memory, making Fernet generally unsuitable for very large files at this time.

**"stockholm.py"** This is a script aimed to infect the user's '/home/$USER/infection' folder causing the same effects as WannaCry virus did to thousands of users back in 2017. Basically, the script renames and encrypts using symmetric key encryption all files matching certain extensions.
Fortunately, this timearound the script includes also the vaccine. (2023, Eduard Vendrell)")

## Instructions
usage: stockholm.py [-h] [-help] [-version] [-infect "Secret Key"] [-reverse "Secret Key"] [-silent]

options:
  -h, --help            show this help message and exit
  -version, -v          prints application version.
  -infect "Secret Key", -i "Secret Key"
                        Ruin somebody's world by infecting critical folder files.
  -reverse "Secret Key", -r "Secret Key"
                        Save somebody's world by recovering all infected folder files.
  -silent, -s           infects target folder files in silence, with no print outs.