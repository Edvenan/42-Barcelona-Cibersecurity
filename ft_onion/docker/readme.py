
#########################
# CHECK OS TYPE
#########################
# cat /etc/os-release\

#########################
# SSH CONTAINER
#########################
# move to folder with 'Dockerfile'
# docker build -t nginx-ssh .

# docker run -d -p 80:80 -p 4242:22 --name TOR nginx-ssh
# docker run -d -p 80:80 -p 4242:22 --device=/dev/dri -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --name TOR nginx-ssh


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
