#!/usr/bin/python
# Purpose to validate PAT token
# Author Sunil Sankar
# Date 23-Jan-2023
import base64
import requests
import re
import sys
import os
from requests.models import Response
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
pat = os.environ['USER_PAT']
authorization = str(base64.b64encode(bytes(':'+pat, 'ascii')), 'ascii')
organization_url = 'https://dev.azure.com/sunilsankar'
project = 'tempproj'
headers = {
    'Accept': 'application/json',
    'Authorization': 'Basic '+authorization
}
try:
    response = requests.get(
        url=f"{organization_url}/{project}/_apis/git/repositories?api-version=6.0", headers=headers)
    #print(response.status_code)
    if response.status_code == 200:
        print('Personal Access Token authentication Successful')
    else:
        print('Personal Access Token Invalid .Please Generate new one')
        print('##vso[task.logissue type=error] Personal Access Token Invalid .Please Generate new one')
        sys.exit('##vso[task.logissue type=error] Personal Access Token Invalid .Please Generate new one')

except requests.exceptions.JSONDecodeError:
    print('Personal Access Token Invalid .Please Generate new one')
    print('##vso[task.logissue type=error] Personal Access Token Invalid .Please Generate new one')
    sys.exit('##vso[task.logissue type=error] Personal Access Token Invalid .Please Generate new one')
