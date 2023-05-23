# Use the official Nginx base image
FROM nginx

# Expose port 80
EXPOSE 80

# Install SSH server
RUN apt-get update && apt-get install -y openssh-server

# Configure SSH
RUN mkdir /var/run/sshd
RUN echo 'root:Pa55w.rd' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Expose SSH port 4242
EXPOSE 4242

# Start SSH server and Nginx
CMD service ssh start && nginx -g 'daemon off;'
