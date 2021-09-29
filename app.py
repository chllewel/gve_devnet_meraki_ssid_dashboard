""" Copyright (c) 2020 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied. 
"""

# Import Section
from flask import Flask, render_template, request, url_for, redirect, session
from collections import defaultdict
import datetime
import requests
import json
from dotenv import load_dotenv
import os
from merakiAPI import Meraki
from prettyprinter import pprint
from flask_session import Session


# load all environment variables
load_dotenv()




# Global variables
app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)



# Methods
# Returns location and time of accessing device
def getSystemTimeAndLocation():
    # request user ip
    userIPRequest = requests.get('https://get.geojs.io/v1/ip.json')
    userIP = userIPRequest.json()['ip']

    # request geo information based on ip
    geoRequestURL = 'https://get.geojs.io/v1/ip/geo/' + userIP + '.json'
    geoRequest = requests.get(geoRequestURL)
    geoData = geoRequest.json()

    #create info string
    location = geoData['country']
    timezone = geoData['timezone']
    current_time=datetime.datetime.now().strftime("%d %b %Y, %I:%M %p")
    timeAndLocation = "System Information: {}, {} (Timezone: {})".format(location, current_time, timezone)

    return timeAndLocation



##Routes
#Login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        try:
            #Page without error message and defined header links
            return render_template('login.html', hiddenLinks=True, timeAndLocation=getSystemTimeAndLocation())
        except Exception as e:
            print(e)
            #OR the following to show error message
            return render_template('login.html', error=False, errormessage=e, errorcode=e, timeAndLocation=getSystemTimeAndLocation())
    elif request.method == 'POST':
        try:
            session["meraki"] = request.form['api-key']
            meraki = Meraki(api_key=request.form['api-key'])
            del meraki

            return redirect(url_for('viewSsids'))
        except Exception as e:
            print("Login Error")
            print(e)
            return render_template('login.html', error=False, errormessage=str(e), errorcode=e, timeAndLocation=getSystemTimeAndLocation())

    else:

        return render_template('login.html', error=False, errormessage="Invalid Method", timeAndLocation=getSystemTimeAndLocation())


#Table of Ssids
@app.route('/ssids', methods=['GET', 'POST'])
def viewSsids():
    try:
        meraki = Meraki(api_key=session["meraki"])
        ssids = meraki.getOrganzationSSIDS()['enabled']
        del meraki

        #Show table with all devices
        if request.method == 'GET':
            return render_template('tablemenu.html', hiddenLinks=False, ssids = ssids, timeAndLocation=getSystemTimeAndLocation())


    except Exception as e: 
        print(e)  
        #OR the following to show error message 
        return render_template('tablemenu.html', error=True,errormessage=str(e), errorcode=e, timeAndLocation=getSystemTimeAndLocation())


@app.route('/ssids/<golden_network>/<golden_ssid>/update', methods=['POST'])
def updateAllSsids(golden_network, golden_ssid):
    sent_data = json.loads(request.get_data().decode("UTF-8"))
    selected_networks = sent_data["selectedNetworks"]
    selected_configs = sent_data["selectedConfigs"]

    meraki = Meraki(api_key=session["meraki"])
    success = meraki.updateAllSsidConfigurations(golden_network,golden_ssid, targeted_networks=selected_networks, selected_configs=selected_configs)
    del meraki

    print("Update Successful: %s"%success)
    if success:
        return "True"
    else:
        return "False"

@app.route('/ssids/<golden_network>/<golden_ssid>/create', methods=['POST'])
def createNewSsids(golden_network, golden_ssid):
    selected_networks = json.loads(request.get_data().decode("UTF-8"))

    meraki = Meraki(api_key=session["meraki"])
    success = meraki.createNewSsidConfigurationAllNetworks(golden_network, golden_ssid, targeted_networks=selected_networks)
    del meraki

    print("SSID Creation Successful: %s"%success)

    if success:
        return "True"
    else:
        return "False"

#Edit page for table entry
@app.route('/ssids/<golden_network>/<golden_ssid>/<network>/<ssid>/view', methods=['GET', 'POST'])
def viewSsidDetails(golden_network, golden_ssid, network, ssid):
    try:
        if request.method == 'GET':

            meraki = Meraki(api_key=session["meraki"])
            ssid = meraki.getDashboard().wireless.getNetworkWirelessSsid(network,ssid)
            golden_ssid = meraki.getDashboard().wireless.getNetworkWirelessSsid(golden_network, golden_ssid)

            del meraki

            return render_template('editTableEntry.html', ssid=ssid, golden_ssid = golden_ssid, timeAndLocation=getSystemTimeAndLocation())



    except Exception as e: 
        print(e)  
        #OR the following to show error message 
        return render_template('editTableEntry.html', error=True, errormessage=str(e), errorcode=e, ssid = ssid, timeAndLocation=getSystemTimeAndLocation())

#Ajax Calls
@app.route('/ssids/all/json', methods=['GET'])
def getAllSsidsJson():
    try:
        meraki = Meraki(api_key=session["meraki"])
        return json.dumps(meraki.getOrganzationSSIDS()['enabled'])
        del meraki

    except Exception as e:
        print(e)
        return False

if __name__ == "__main__":
    app.run(host="0.0.0.0")
