#!/usr/bin/env python
#Author Sunil Sankar
#Date 16-Aug-2022
import requests
import sys
import argparse
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
parser = argparse.ArgumentParser(description='Azure Devops Agent downloader')
parser.add_argument(
    '--version',
    default='latest',
    help='provide the version number'
)
my_namespace = parser.parse_args()
#print(my_namespace.version)

GITHUB_URL = 'https://api.github.com/repos/Microsoft/azure-pipelines-agent/releases'
if my_namespace.version == "latest":
    url = "{}/latest".format(GITHUB_URL)
    #latest = requests.get(url,  verify=False)
    latest = requests.request("GET", url, verify=False)
    output = latest.json()['name'].replace('v','')
    print(output)
    download_url = 'https://vstsagentpackage.azureedge.net/agent/{0}/vsts-agent-linux-x64-{0}.tar.gz'.format(output)
    print(f'##vso[task.setvariable variable=azureagentVersion]{output}')
else:
    print(f'##vso[task.setvariable variable=azureagentVersion]{my_namespace.version}')
    download_url = 'https://vstsagentpackage.azureedge.net/agent/{0}/vsts-agent-linux-x64-{0}.tar.gz'.format(my_namespace.version)
#response = requests.get("https://api.github.com/repos/Microsoft/azure-pipelines-agent/releases/latest")
#print(latest.json()['name'].replace('v',''))
print(download_url)
#req = requests.get(download_url,  verify=False)
req = requests.request("GET", download_url,  verify=False)
filename = download_url.split('/')[-1]
print(filename)
with open(filename,'wb') as output_file:
     output_file.write(req.content)
print('Downloading Completed')
