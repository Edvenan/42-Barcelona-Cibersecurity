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
RUN apt-get update && apt-get install -y lsb-release
RUN apt-get update && apt-get install -y wget
RUN apt-get update && apt-get install -y gpg


# Install SSH server
RUN apt-get update && apt-get install -y openssh-server

# Install OpenSSL
RUN apt-get update && apt-get install -y openssl

# Install TOR
RUN apt-get update && apt-get install -y apt-transport-https
RUN echo "deb     [signed-by=/usr/share/keyrings/tor-archive-keyring.gpg] https://deb.torproject.org/torproject.org bullseye main" >> /etc/apt/sources.list.d/tor.list
RUN echo "deb-src [signed-by=/usr/share/keyrings/tor-archive-keyring.gpg] https://deb.torproject.org/torproject.org bullseye main" >> /etc/apt/sources.list.d/tor.list
RUN wget -qO- https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc | gpg --dearmor | tee /usr/share/keyrings/tor-archive-keyring.gpg >/dev/null
RUN apt-get update && apt-get install -y tor deb.torproject.org-keyring
RUN echo 'HiddenServiceDir /var/lib/tor/hidden_service/' >> /etc/tor/torrc
RUN echo 'HiddenServicePort 80 127.0.0.1:80' >> /etc/tor/torrc


# Generate self-signed SSL/TLS certificates 
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
RUN openssl dhparam -out /etc/nginx/dhparam.pem 2048


# Set the user and password variables
ARG USERNAME=eduard
ARG PASSWORD=Pa55w.rd

# Create the user
RUN useradd -m ${USERNAME} \
    && echo "${USERNAME}:${PASSWORD}" | chpasswd \
    && usermod -aG sudo ${USERNAME}


# Configure SSH access
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config \
    && echo "AllowUsers ${USERNAME}" >> /etc/ssh/sshd_config
#RUN mkdir /var/run/sshd
#RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
#RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Create a custom network and assign a static IP address
#RUN docker network create my_network && \
#    docker network connect --ip 10.11.2.10 my_network TOR

# Set ssh port to 4242
RUN sed -i 's/#Port 22/Port 4242/' /etc/ssh/sshd_config

# Expose SSH port 4242
EXPOSE 4242

# Configure Nginx server to use SSL/TLS:
COPY nginx.conf /etc/nginx/nginx.conf

# Start SSH server, TOR and Nginx
CMD service ssh start && service tor restart && nginx -g 'daemon off;'