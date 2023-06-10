# Use the official Nginx base image
FROM nginx

# Expose port 80
EXPOSE 80

# SET LOCAL TIME ZONE
RUN ln -sf /usr/share/zoneinfo/Europe/Madrid /etc/localtime

# utils installs
RUN apt-get update && apt-get install -y bash-completion
RUN apt-get update && apt-get install -y sudo
RUN apt-get update && apt-get install -y nano
RUN apt-get update && apt-get install -y iputils-ping
RUN apt-get update && apt-get install -y dnsutils
RUN apt-get update && apt-get install -y net-tools
RUN apt-get update && apt-get install -y lsb-release
RUN apt-get update && apt-get install -y wget
RUN apt-get update && apt-get install -y gpg


# add SSH server
RUN apt-get update && apt-get install -y openssh-server


# Set the user and password variables
ARG USERNAME=edvenan
ARG PASSWORD=Pa55w.rd

# Create the user and add it to sudoers group
RUN useradd -m ${USERNAME} \
    && echo "${USERNAME}:${PASSWORD}" | chpasswd \
    && usermod -aG sudo ${USERNAME}

# Configure bash alias and PS1:
RUN echo "alias ls='ls -rtal'" >> /root/.bashrc
RUN echo "alias html='cd /usr/share/nginx/html/'" >> /root/.bashrc
RUN echo "alias hidden='cat /var/lib/tor/hidden_service/hostname'" >> /root/.bashrc
RUN echo "PS1='\[\e[31m\][\[\e[m\]\[\e[38;5;172m\]\u\[\e[m\]@\[\e[38;5;153m\]\h\[\e[m\] \[\e[38;5;214m\]\W\[\e[m\]\[\e[31m\]]\[\e[m\]\\$'" >> /root/.bashrc

RUN sed -i 's#edvenan:/bin/sh#edvenan:/bin/bash#' /etc/passwd

########################
# Configure SSH access
########################
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config \
    && echo "AllowUsers ${USERNAME}" >> /etc/ssh/sshd_config \
    && sed -i 's/X11Forwarding yes/X11Forwarding no/' /etc/ssh/sshd_config \
    && sed -i 's/#PermitEmptyPasswords no/PermitEmptyPasswords no/' /etc/ssh/sshd_config  \
    && sed -i 's/#MaxAuthTries 6/MaxAuthTries 3/' /etc/ssh/sshd_config

# Settings to disable password login once ssh key authentication is enabled
# sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config
# sed -i 's/#AuthorizedKeysFile/AuthorizedKeysFile/' /etc/ssh/sshd_config
# sed -i 's/#AuthorizedKeysCommandUser nobody/AuthorizedKeysCommandUser edvenan/' /etc/ssh/sshd_config
# sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
# service ssh restart

# Set ssh port to 4242
RUN sed -i 's/#Port 22/Port 4242/' /etc/ssh/sshd_config

# Expose SSH port 4242
EXPOSE 4242

# Transfer Nginx web content (hidden service):
COPY ./web/ /usr/share/nginx/html/

# add TOR
RUN apt-get update && apt-get install -y apt-transport-https
RUN echo "deb     [signed-by=/usr/share/keyrings/tor-archive-keyring.gpg] https://deb.torproject.org/torproject.org bullseye main" >> /etc/apt/sources.list.d/tor.list
RUN echo "deb-src [signed-by=/usr/share/keyrings/tor-archive-keyring.gpg] https://deb.torproject.org/torproject.org bullseye main" >> /etc/apt/sources.list.d/tor.list
RUN wget -qO- https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc | gpg --dearmor | tee /usr/share/keyrings/tor-archive-keyring.gpg >/dev/null
RUN apt-get update && apt-get install -y tor deb.torproject.org-keyring
#RUN apt-get update && apt-get install -y tor
RUN echo 'HiddenServiceDir /var/lib/tor/hidden_service/' >> /etc/tor/torrc
RUN echo 'HiddenServicePort 80 127.0.0.1:80' >> /etc/tor/torrc


# Start SSH server, TOR and Nginx.
CMD service ssh start && service tor restart && nginx -g 'daemon off;'