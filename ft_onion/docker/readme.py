
#########################
# CHECK OS TYPE
#########################
# cat /etc/os-release\

#########################
# SSH CONTAINER
#########################
# move to folder with 'Dockerfile'
# docker build -t nginx-ssh-ssl-tsl .

# docker run -d -p 80:80 -p 4242:4242 --name TOR nginx-ssh-ssl-tsl
# docker run -d -p 80:80 -p 4242:4242 --device=/dev/dri -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --name TOR nginx-ssh-ssl-tsl
# docker run -d -p 80:80 -p 4242:4242 -p 443:443 --name TOR nginx-ssh-ssl-tsl


#########################
# SSH CONTAINER
#########################
# ssh root@localhost -p 4242


#########################
# CONTAINER INSTALLS
#########################
# apt update
# apt install bash-completion, sudo, nano, iputils-ping, dnsutils, lsb-release, wget, gpg

# SET LOCAL TIME ZONE
#ln -sf /usr/share/zoneinfo/Europe/Madrid /etc/localtime

#########################
# NGINX www folder
#########################
# cd /usr/share/nginx/html/

#########################
# INSTALLING TOR BROWSER (not needed -> we can do it on the mac to test it works)
#########################
# apt install apt-transport-https


# apt install xz-utils

#  tar -xf tor.tar.xz

# cd /usr/home/tor-browser

##################################################
# INSTALLING TOR in container
##################################################
# https://community.torproject.org/onion-services/setup/install/

# https://support.torproject.org/apt/tor-deb-repo/

    # apt install apt-transport-https
    # cd /etc/apt/sources.list.d# 
    # nano tor.list
    #    deb     [signed-by=/usr/share/keyrings/tor-archive-keyring.gpg] https://deb.torproject.org/torproject.org bullseye main
    #    deb-src [signed-by=/usr/share/keyrings/tor-archive-keyring.gpg] https://deb.torproject.org/torproject.org bullseye main
    # wget -qO- https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc | gpg --dearmor | tee /usr/share/keyrings/tor-archive-keyring.gpg >/dev/null
    # apt install tor deb.torproject.org-keyring
    # torrc location:  cd /etc/tor
    
# EDIT /etc/tor/torrc file:
#       HiddenServiceDir /var/lib/tor/hidden_service/
#       HiddenServicePort 80 127.0.0.1:80

# Now save your torrc and restart Tor.
#   sudo systemctl restart tor /// service tor restart
#                              /// service tor status
#                              /// service --status-all

# cd /var/lib/tor/hidden_service/
# ls
#   total 24
#   -rw------- 1 debian-tor debian-tor   96 May 23 23:59 hs_ed25519_secret_key
#   -rw------- 1 debian-tor debian-tor   64 May 23 23:59 hs_ed25519_public_key
#   -rw------- 1 debian-tor debian-tor   63 May 23 23:59 hostname
#   drwx--S--- 2 debian-tor debian-tor 4096 May 23 23:59 authorized_clients
#   drwx--S--- 3 debian-tor debian-tor 4096 May 23 23:59 .
#   drwx--S--- 4 debian-tor debian-tor 4096 May 24 00:00 ..

# obtain the hash.onion
# cat var/lib/tor/hidden_service/hostname


##################################################
# SSH KEYS FOR SSH AUTHENTICATION
##################################################

# To implement strong passwords or SSH keys for SSH authentication, follow these steps:

# 1) Generate SSH Key Pair (if not already done):
#   Open a terminal or command prompt.
#   Use the ssh-keygen command to generate an SSH key pair.
#   Choose an appropriate location to save the key pair (e.g., ~/.ssh/id_rsa).
#   This will generate two files: id_rsa (private key) and id_rsa.pub (public key).
#   Set a strong passphrase for the private key when prompted.
"       ssh-keygen -t rsa -b 2048       "
    
# 2) Copy the public key to the server & Configure SSH Server:
#   Use the ssh-copy-id command to copy the public key to the server.
#   Enter your password when prompted. This command will copy the public key to the server and add it to
#   the authorized keys list.  
"    ssh-copy-id -i ~/.ssh/id_rsa.pub -p 4242 edvenan@172.18.0.2        "

"       https://www.ssh.com/academy/ssh/copy-id                         "
#   Test SSH connection without a password.
"       ssh username@server_ip                                          "
"       ssh -i ./ssh/id_rsa -p 4242 172.18.0.2                          "

#   After copying the public key, you should be able to SSH into the server without entering a password:
# 
# 3) Disable password authentication (optional):
#   Once you've confirmed that SSH key-based authentication is working, you may choose to disable password 
#   authentication for increased security.
#   Open the SSH server configuration file on the server using a text editor. The file location may vary, but 
#   common locations include /etc/ssh/sshd_config or /etc/sshd_config.
#   Look for the line #PasswordAuthentication yes and change it to PasswordAuthentication no. If the line 
#   doesn't exist, add it.
"       sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config     "
#   Save the file and exit the text editor.
#   Restart the SSH server for the changes to take effect. The command may vary depending on your Linux 
#   distribution. For example:
#   Copy code
"        sudo service ssh restart       "


# 4) Configure SSH Client ??
#   Copy the public key generated in Step 1 (usually located in ~/.ssh/id_rsa.pub).
#   Connect to the SSH client machine.
#   Open the authorized_keys file in the SSH user's home directory (e.g., ~/.ssh/authorized_keys) using a text
#   editor.
#   Paste the copied public key into a new line in the authorized_keys file.
#   Save the changes and exit the editor.

    sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config
    sed -i 's/#AuthorizedKeysFile/AuthorizedKeysFile/' /etc/ssh/sshd_config
    
# 4) Test SSH Key-Based Authentication:
#   Disconnect any existing SSH sessions.
#   Attempt to connect to the SSH server from the client machine using SSH.
#   If the key-based authentication is set up correctly, you should be prompted for the passphrase (if used) 
#   and successfully log in without entering a password.

# By following these steps, you will have implemented SSH key-based authentication, which provides stronger 
# security compared to password-based authentication. Ensure that you securely manage and protect the private 
# key and passphrase associated with the SSH key pair.


###########################
# nmap AGRESSIVE SCANNING
###########################
nmap -A -p- 172.18.0.2


###########################
# CREATE DOCKER IMAGE
###########################
"       https://www.dataset.com/blog/create-docker-image/                   "

" sudo docker commit --author Eduard_Vendrell onion onion_image       "
# will be stored in:   /var/lib/docker/images 

###########################
# PUSH DOCKER IMAGE to DOCKER HUB
###########################
"      https://docs.docker.com/get-started/04_sharing_app/             "
sudo docker tag onion_image:latest edvenan/nginx-ssh-tor:onion
sudo docker login -u edvenan
sudo docker push edvenan/nginx-ssh-tor:onion

"       https://hub.docker.com/repository/docker/edvenan/nginx-ssh-tor/general      "

##################################
# FIND PID USING A PORT
##################################
WINDOWS: netstat -ano | findstr :80
        kill the process (PID) in TaskManager_>Details-> PID
LINUX: netstat -tuln 

