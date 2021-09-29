from registry.access.redhat.com/ubi8/ubi-init
# RUN update yum
RUN yum -y update
#Install OpenSSL
RUN yum -y install openssl
# RUN yum install python3
RUN yum -y install python3-devel
#RUN yum install gcc
RUN yum -y install gcc
# Install python3-pip
RUN yum -y install python3-pip
# CREATE Directory as Work Directory
WORKDIR /app
# Add Requirements.txt file to current directory
copy requirements.txt .
# Install PIP Requirements
RUN pip3 install -r ./requirements.txt
#Install GUNICORN
RUN pip3 install gunicorn
# Copy Code from context to image
COPY . .
# Create OpenSSL Certs
RUN openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365 -subj "/C=GB/ST=London/L=London/O=Global Security/OU=IT Department/CN=example.com"

#Run Application
CMD ["gunicorn","-w", "4", "-b", ":443", "--certfile", "cert.pem", "--keyfile", "key.pem", "wsgi:app"] 
