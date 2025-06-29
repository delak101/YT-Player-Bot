# SSL Configuration for Server Environment
# Add this to the top of bot.py for server deployment

import os
import ssl
import urllib3
import certifi

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set environment variables for SSL bypass
os.environ['PYTHONHTTPSVERIFY'] = '0'
os.environ['SSL_VERIFY'] = 'False'
os.environ['CURL_CA_BUNDLE'] = ''

# Create unverified SSL context
ssl._create_default_https_context = ssl._create_unverified_context

# Try to set certifi bundle if available
try:
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
except:
    pass

# Additional SSL bypass for requests
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Create session with SSL bypass
session = requests.Session()
session.verify = False

# Monkey patch requests to disable SSL verification globally
requests.packages.urllib3.disable_warnings()
requests.adapters.DEFAULT_RETRIES = 3
