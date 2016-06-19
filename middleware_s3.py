#!/usr/bin/python
"""
Generate AWS4 authentication headers for your protected files

This module is meant to plug into munki.
https://github.com/munki/munki/wiki

This is just a modified version of this
http://docs.aws.amazon.com/general/latest/gr/sigv4-signed-request-examples.html#sig-v4-examples-get-auth-header

"""

##############################################################################
# Copyright 2016 Wade Robson
# 
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not
#  use this file except in compliance with the License. You may obtain a copy
#  of the License at
# 
#       http://www.apache.org/licenses/LICENSE-2.0
# 
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
##############################################################################

__version__ = '0.15'

import datetime
import hashlib
import hmac
import urllib2
import xml.etree.ElementTree as ET
from urlparse import urlparse

# pylint: disable=E0611
from Foundation import CFPreferencesCopyAppValue
# pylint: enable=E0611

S3_PREF = 'com.github.waderobson.s3-auth'
MUNKI_PREF = 'ManagedInstalls'

METHOD = 'GET'
SERVICE = 's3'

def pref(pref_name, bundle_id):
    """Return a preference. See munkicommon.py for details
    """
    pref_value = CFPreferencesCopyAppValue(pref_name, bundle_id)
    return pref_value


ACCESS_KEY = pref('AccessKey', S3_PREF)
SECRET_KEY = pref('SecretKey', S3_PREF)
REGION = pref('Region', S3_PREF)
SOFTWARE_REPO = pref('SoftwareRepoURL', MUNKI_PREF)


def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()


def get_signature_key(key, datestamp, region, service):
    kdate = sign(('AWS4' + key).encode('utf-8'), datestamp)
    kregion = sign(kdate, region)
    kservice = sign(kregion, service)
    ksigning = sign(kservice, 'aws4_request')
    return ksigning


def uri_from_url(url):
    parse = urlparse(url)
    return parse.path

def bucket_from_url(url):
    parse = urlparse(url)
    return parse.hostname.split('.')[0]

def host_from_url(url):
    parse = urlparse(url)
    return parse.hostname


def s3_auth_headers(url, REGION, get_location=False):
    """
    Returns a dict that contains all the required header information.
    Each header is unique to the url requested.
    """
    # Create a date for headers and the credential string
    time_now = datetime.datetime.utcnow()
    amzdate = time_now.strftime('%Y%m%dT%H%M%SZ')
    datestamp = time_now.strftime('%Y%m%d') # Date w/o time, used in credential scope
    uri = uri_from_url(url)
    if get_location:
        host = 's3.amazonaws.com'
        canonical_querystring = u'location='
        REGION = 'us-east-1'
    else:
        host = host_from_url(url)
        canonical_querystring = ''
    canonical_uri = uri
    canonical_headers = 'host:{}\nx-amz-date:{}\n'.format(host, amzdate)
    signed_headers = 'host;x-amz-date'
    payload_hash = hashlib.sha256('').hexdigest()
    canonical_request = '{}\n{}\n{}\n{}\n{}\n{}'.format(METHOD,
                                                        canonical_uri,
                                                        canonical_querystring,
                                                        canonical_headers,
                                                        signed_headers,
                                                        payload_hash)

    algorithm = 'AWS4-HMAC-SHA256'
    credential_scope = '{}/{}/{}/aws4_request'.format(datestamp, REGION, SERVICE)
    hashed_request = hashlib.sha256(canonical_request).hexdigest()
    string_to_sign = '{}\n{}\n{}\n{}'.format(algorithm,
                                             amzdate,
                                             credential_scope,
                                             hashed_request)


    signing_key = get_signature_key(SECRET_KEY, datestamp, REGION, SERVICE)
    signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()

    authorization_header = ("{} Credential={}/{},"
                            " SignedHeaders={}, Signature={}").format(algorithm,
                                                                      ACCESS_KEY,
                                                                      credential_scope,
                                                                      signed_headers,
                                                                      signature)

    headers = {'x-amz-date': amzdate,
               'x-amz-content-sha256': payload_hash,
               'Authorization': authorization_header}

    return headers

def get_region(url):
    """Looks up the s3 bucket region.
    url must have bucket in hostname ie; 
    
     <s3bucket>.s3.amazonaws.com.
    
    credentials need allow s3:GetBucketLocation 
    on the bucket
    """
    bucket = bucket_from_url(url)
    bucket_location_url = 'https://s3.amazonaws.com/' + bucket + '?location'
    headers = s3_auth_headers(bucket_location_url, None, get_location=True)
    req = urllib2.Request(bucket_location_url, None, headers)
    resp = urllib2.urlopen(req)
    tree = ET.parse(resp)
    root = tree.getroot()
    return root.text

## if no region is set attenpt to find it
if not REGION:
    REGION = get_region(SOFTWARE_REPO)


def process_request_options(options):
    """Make changes to options dict and return it.
       This is the fuction that munki calls."""
    if 's3.amazonaws.com' in options['url']:
        headers = s3_auth_headers(options['url'], REGION)
        options['additional_headers'].update(headers)
    return options

