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

#How to retrieve an Meraki api key: https://developer.cisco.com/meraki/api-v1/#!getting-started/find-your-organization-id 
#Meraki Dashboard API call documentation: https://developer.cisco.com/meraki/api-v1/#!overview/api-key

# Import Section
import meraki
import os
from dotenv import load_dotenv
from prettyprinter import pprint
import json
import traceback


# load all environment variables
load_dotenv()


class Meraki:
    def __init__(self, api_key, base_url="https://api.meraki.com/api/v1"):

        self.__DASHBOARD = meraki.DashboardAPI(
            api_key=api_key,
            base_url=base_url,
            print_console=False,
            suppress_logging=True)
        for org in self.__DASHBOARD.organizations.getOrganizations():
            if org['name'] == os.environ['MERAKI_ORGANIZATION']:
                self.__org_id = org['id']



    #API calls
    #Organizations
    def getOrganizations(self):
        response = self.__DASHBOARD.organizations.getOrganizations()
        print(response)
        return response

    #Networks
    def getNetworks(self):
        response = self.__DASHBOARD.organizations.getOrganizationNetworks(
            self.__org_id, total_pages='all'
        )
        return(response)

    def getOrganzationSSIDS(self):
        ssids = {'enabled':{}, 'disabled':{}}

        for network in self.getNetworks():
            try:
                for ssid in self.__DASHBOARD.wireless.getNetworkWirelessSsids(network['id']):
                    if ssid['enabled'] == True:

                        ssid['network_id'] = network['id']
                        if network['name'] in ssids['enabled']:
                            ssids['enabled'][network['name']].append(ssid)
                        else:
                            ssids['enabled'][network['name']] = []
                            ssids['enabled'][network['name']].append(ssid)

                    else:
                        ssid['network_id'] = network['id']
                        if network['name'] in ssids['disabled']:
                            ssids['disabled'][network['name']].append(ssid)
                        else:
                            ssids['disabled'][network['name']] = []
                            ssids['disabled'][network['name']].append(ssid)

            except Exception as e:
                continue

        return ssids

    def getNetworkSSID(self, network_id, ssid_number):
        return self.__DASHBOARD.wireless.getNetworkWirelessSsid(network_id,ssid_number)


    def getDashboard(self):
        return self.__DASHBOARD

    def updateAllSsidConfigurations(self, golden_config_network_id, golden_config_ssid_number, demo_config=False, targeted_networks = {}, selected_configs=[]):
        if demo_config:
            try: 
                with open("demo_configurations.txt") as f:
                    ssids = json.loads(f.read())
                    pprint(ssids)

                for network, value in ssids['enabled'].items():
                    for ssid in value:
                        ssid_copy = ssid.copy()
                        del ssid_copy['number']
                        self.__DASHBOARD.wireless.updateNetworkWirelessSsid(networkId=ssid['network_id'], number=ssid['number'], **ssid_copy)
                        print("success")

                for network, value in ssids['disabled'].items():
                    for ssid in value:
                        ssid_copy = ssid.copy()
                        del ssid_copy['number']
                        self.__DASHBOARD.wireless.updateNetworkWirelessSsid(networkId=ssid['network_id'], number=ssid['number'], **ssid_copy)
                        print("success")


                return True

            except Exception as e:
                print("ERROR")
                print(str(e))

                return False


        else:
            if targeted_networks and selected_configs:
                golden_config = self.getNetworkSSID(golden_config_network_id, golden_config_ssid_number)
                new_golden_config = {k: golden_config[k] for k in selected_configs if k in golden_config}
                try:
                    for network, value in self.getOrganzationSSIDS()['enabled'].items():
                        if network in targeted_networks:
                            for ssid in value:
                                try:
                                    if ssid['name'] in targeted_networks[network]:
                                        self.__DASHBOARD.wireless.updateNetworkWirelessSsid(networkId=ssid['network_id'],
                                                                                            number=ssid['number'],
                                                                                            **new_golden_config)
                                except Exception as e:
                                    if "Each enabled SSID must have a unique name" in str(e):
                                        continue


                    return True

                except Exception as e:
                    print("ERROR in TARGETED NETWORKS STATEMENT")
                    traceback.print_exc()


                    return False
            else:
                print("No targeted networks given.")
                return False


    def createNewSsidConfigurationAllNetworks(self, golden_config_network_id, golden_config_ssid_number, targeted_networks = []):
        golden_config = self.getNetworkSSID(golden_config_network_id, golden_config_ssid_number)
        del golden_config['number']

        try:
            if targeted_networks:
                for network, value in self.getOrganzationSSIDS()['disabled'].items():
                    if network in targeted_networks:
                        for ssid in value:
                                try:
                                    self.__DASHBOARD.wireless.updateNetworkWirelessSsid(networkId=ssid['network_id'], number=ssid['number'], **golden_config)
                                    break
                                except Exception as e:
                                    if "Each enabled SSID must have a unique name" in str(e):

                                        continue
                                    else:
                                        return False

                return True

            else:
                print("No targeted networks given.")
                return False

        except Exception as e:
            print(str(e))
            return False









