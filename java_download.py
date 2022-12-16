#!/usr/bin/env python
# Author Sunil Sankar
#Date 16-Dec-2022
import requests
import re
def get_java_latest_version(version):
    url = 'https://javadl-esd-secure.oracle.com/update/baseline.version'
    x = requests.get(url)
    output = x.text
    #print(output)
    pattern = r'{}.*'.format(version)
    x = re.findall(pattern, output)
    x = [i.strip() for i in x]
    return x[0]
version = get_java_latest_version(1.8)
print(version)

url = 'https://www.oracle.com/java/technologies/downloads/#java8'
x = requests.get(url)
download = x.text
r1 = re.findall(r'Java SE Development Kit 8.*',download)
#r1 = [i.strip() for i in r1]
output = r1[0]
r2 = re.findall(r'8.\w.\w',output)
LATEST_VERSION = r2[0]
LATEST_PATCH = LATEST_VERSION.strip('8u')
LATEST_DOWNLOAD = re.findall(r'data-file=.*', download)
r =  re.compile("data-file=.*jdk.*-linux.*x64.tar.gz.")
newlist = list(filter(r.match, LATEST_DOWNLOAD))
LATEST_URL = newlist[0].strip('data-file=')
FILE = 'jdk-{}-linux-x64.tar.gz'.format(LATEST_VERSION)
VER = LATEST_URL.split('/')
HASH = VER[7]
VERSION = VER[6].strip('8u')
URL="https://javadl.oracle.com/webapps/download/GetFile/1.8.0_{}/{}/linux-i586/{}".format(VERSION,HASH,FILE)

cookies = {
    'oraclelicense': 'accept-securebackup-cookie',
}

headers = {
    # 'Cookie': 'oraclelicense=accept-securebackup-cookie',
}

response = requests.get(URL, cookies=cookies, headers=headers, verify=False)
filename = FILE
print(filename)
with open(filename,'wb') as output_file:
     output_file.write(response.content)
print('Downloading Completed')