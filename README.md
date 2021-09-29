# GVE_DevNet_Meraki_SSID_Golden_Config
Compares, updates, and creates Meraki SSID Configurations based on a selected 'Golden Config'


## Contacts
* Charles Llewellyn

## Solution Components
* Python
*  Meraki
*  Flask
* Podman/Docker

## Installation/Configuration

Running Podman/Docker container was tested on CentOS/RHEL8 - (optional: replace podman commands with docker).

```
git clone https://wwwin-github.cisco.com/gve/GVE_DevNet_Meraki_SSID_Golden_Config.git

cd GVE_DevNet_Meraki_SSID_Golden_Config

vi .env

 > Change value of "MERAKI_ORGANIZATION=" to EXACT (Captialization matters) Organization name.
 > save changes and close file
 
podman build . -t meraki-ssid-app:1 -f container_file

podman run -dit -p 443:443 IMAGE_ID

```

**Application can be accessed at x.x.x.x, where x.x.x.x is the IP address of the server running podman(Not the container).**

**If running on local machine, default address is https://0.0.0.0**

Running without podman/docker:

```
cd GVE_DevNet_Meraki_SSID_Golden_Config

vi .env

 > Change value of "MERAKI_ORGANIZATION=" to EXACT (Captialization matters) Organization name.
 > save changes and close file
 
pip3 install -r requirements.txt

gunicorn -w 4 wsgi:app

```


# Screenshots

![/images/app.png](/images/app.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
