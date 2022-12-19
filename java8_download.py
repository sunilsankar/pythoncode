#!/usr/bin/env python
# Author Sunil Sankar
#Date 16-Dec-2022
#Purpose Download Oracle Java 8
import requests
import re
import sys
import argparse
import os
import shutil
from os import path
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
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

parser = argparse.ArgumentParser(description='Oracle jdk 8downloader')
parser.add_argument(
    '--version',
    default='latest',
    help='provide the version number in this format 8u<version> or latest  example 8u341'
)
my_namespace = parser.parse_args()
if my_namespace.version == "latest":
    url = 'https://www.oracle.com/java/technologies/downloads/#java8'
    print(url)
    x = requests.get(url)
    download = x.text
    r1 = re.findall(r'Java SE Development Kit 8.*',download)
    #r1 = [i.strip() for i in r1]
    output = r1[0]
    r2 = re.findall(r'8.\w.\w',output)
    LATEST_VERSION = r2[0]
    print(LATEST_VERSION)
    LATEST_PATCH = LATEST_VERSION.strip('8u')
    LATEST_DOWNLOAD = re.findall(r'data-file=.*', download)
    r =  re.compile("data-file=.*jdk.*-linux.*x64.tar.gz.")
    newlist = list(filter(r.match, LATEST_DOWNLOAD))
    LATEST_URL = newlist[0].strip('data-file=')
    FILE = 'jdk-{}-linux-x64.tar.gz'.format(LATEST_VERSION).replace(" data-license=141 href=","")
    VER = LATEST_URL.split('/')
    HASH = VER[7]
    VERSION = VER[6].strip('8u')
    URL="https://javadl.oracle.com/webapps/download/GetFile/1.8.0_{}/{}/linux-i586/{}".format(VERSION,HASH,FILE)
    print(URL)

    cookies = {
        'oraclelicense': 'accept-securebackup-cookie',
    }

    headers = {
        # 'Cookie': 'oraclelicense=accept-securebackup-cookie',
    }
    response = requests.get(URL, cookies=cookies, headers=headers, verify=False)
    filename = FILE
    print(filename)
    print('##vso[task.setvariable variable=FILENAME;]%s' % (filename))
    print('##vso[task.setvariable variable=LATEST_VERSION;]%s' % (LATEST_VERSION))

    with open(filename,'wb') as output_file:
         output_file.write(response.content)
    print('Downloading Completed')
elif int(my_namespace.version.strip('8u')) >= 211:
     url = 'https://www.oracle.com/java/technologies/javase/javase8u211-later-archive-downloads.html'
     x = requests.get(url)
     download = x.text
     search_regex = r'data-file=.*jdk-{}-linux.*x64.tar.gz.'.format(my_namespace.version)
     LATEST_DOWNLOAD = re.findall(search_regex, download)
     LATEST_URL = LATEST_DOWNLOAD[0].strip('data-file=')
     print(LATEST_URL)
     VER = LATEST_URL.split('/')
     HASH = VER[7]
     VERSION = VER[6].strip('8u')
     F = VER[8].replace("'","")
     FILE =  re.findall(r'jdk.*.gz', F)
     FILE = FILE[0]
     URL="https://javadl.oracle.com/webapps/download/GetFile/1.8.0_{}/{}/linux-i586/{}".format(VERSION,HASH,FILE)
     print(URL)
     cookies = {
        'oraclelicense': 'accept-securebackup-cookie',
     }

     headers = {
            # 'Cookie': 'oraclelicense=accept-securebackup-cookie',
        }
     response = requests.get(URL, cookies=cookies, headers=headers, verify=False)
     filename = FILE
     print(filename)
     print('##vso[task.setvariable variable=FILENAME;]%s' % (filename))
     print('##vso[task.setvariable variable=LATEST_VERSION;]%s' % (my_namespace.version))

     with open(filename,'wb') as output_file:
        output_file.write(response.content)
     print('Downloading Completed')
elif int(my_namespace.version.strip('8u')) < 211:     
     url = 'https://www.oracle.com/nl/java/technologies/javase/javase8-archive-downloads.html'
     x = requests.get(url)
     download = x.text
     search_regex = r'data-file=.*jdk-{}-linux.*x64.tar.gz.'.format(my_namespace.version)
     LATEST_DOWNLOAD = re.findall(search_regex, download)
     LATEST_URL = LATEST_DOWNLOAD[0].strip('data-file=')
     VER = LATEST_URL.split('/')
     print(VER)
     HASH = VER[7]
     VERSION = VER[6].replace("8u","")
     F = VER[8].replace("'","")
     FILE =  re.findall(r'jdk.*.gz', F)
     print(FILE)
     FILE = FILE[0]
     print(HASH)
     print(FILE)
     print(VERSION)
     URL="https://javadl.oracle.com/webapps/download/GetFile/1.8.0_{}/{}/linux-i586/{}".format(VERSION,HASH,FILE)
     print(URL)
     cookies = {
        'oraclelicense': 'accept-securebackup-cookie',
     }

     headers = {
            # 'Cookie': 'oraclelicense=accept-securebackup-cookie',
        }
     response = requests.get(URL, cookies=cookies, headers=headers, verify=False)
     filename = FILE
     print(filename)
     print('##vso[task.setvariable variable=FILENAME;]%s' % (filename))
     print('##vso[task.setvariable variable=LATEST_VERSION;]%s' % (my_namespace.version))

     with open(filename,'wb') as output_file:
        output_file.write(response.content)
     print('Downloading Completed')
