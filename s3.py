"""
Generate s3 authentication headers for your protected files

This module is meant to plug into munki.
https://github.com/munki/munki/wiki

This is just a modified version of this
http://docs.aws.amazon.com/general/latest/gr/sigv4-signed-request-examples.html#sig-v4-examples-get-auth-header

"""
import sys, os, datetime, hashlib, hmac 
from urlparse import urlparse

from munkicommon import pref

method = 'GET'
service = 's3'
#region = 'us-west-2'

def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def getSignatureKey(key, dateStamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning

# Read AWS access key from env. variables or configuration file. Best practice is NOT
# to embed credentials in code.
# secret_key = os.getenv('S3_SECRET_KEY')
# access_key = os.getenv('S3_ACCESS_KEY')
access_key = pref('s3AccessKey')
secret_key = pref('s3SecretKey')
region = pref('s3Region')

if access_key is None or secret_key is None:
    print 'No access key is available.'
    sys.exit()

# Create a date for headers and the credential string
t = datetime.datetime.utcnow()
amzdate = t.strftime('%Y%m%dT%H%M%SZ')
datestamp = t.strftime('%Y%m%d') # Date w/o time, used in credential scope

def uri_from_url(url):
    parse = urlparse(url)
    return parse.path

def host_from_url(url):
    parse = urlparse(url)
    return parse.hostname

def s3_auth_headers(url):
    """
    Returns a list that contains all the required header information.
    Each header is unique to the url requested.
    """
    uri = uri_from_url(url)
    host = host_from_url(url)
    canonical_uri = '{uri}'.format(uri=uri)
    canonical_querystring = ''
    canonical_headers = 'host:' + host + '\n' + 'x-amz-date:' + amzdate + '\n'
    signed_headers = 'host;x-amz-date'
    payload_hash = hashlib.sha256('').hexdigest()
    canonical_request_string = ("{method}\n{canonical_uri}\n{canonical_querystring}\n"
                                "{canonical_headers}\n{signed_headers}\n{payload_hash}")
    canonical_request = canonical_request_string.format(method=method,
                                                        canonical_uri=canonical_uri,
                                                        canonical_querystring=canonical_querystring,
                                                        canonical_headers=canonical_headers,
                                                        signed_headers=signed_headers,
                                                        payload_hash=payload_hash)

    algorithm = 'AWS4-HMAC-SHA256'
    credential_scope = datestamp + '/' + region + '/' + service + '/' + 'aws4_request'
    string_to_sign_string = "{algorithm}\n{amzdate}\n{credential_scope}\n{hashed_request}"
    hashed_request = hashlib.sha256(canonical_request).hexdigest()
    string_to_sign = string_to_sign_string.format(algorithm=algorithm,
                                                  amzdate=amzdate,
                                                  credential_scope=credential_scope,
                                                  hashed_request=hashed_request)


    signing_key = getSignatureKey(secret_key, datestamp, region, service)
    signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()

    authorization_header_string = ("{algorithm} Credential={access_key}/{credential_scope},"
                                   " SignedHeaders={signed_headers}, Signature={signature}")
    authorization_header = authorization_header_string.format(algorithm=algorithm,
                                                              access_key=access_key,
                                                              credential_scope=credential_scope,
                                                              signed_headers=signed_headers,
                                                              signature=signature)


    headers = ['x-amz-date:' + amzdate,
               'x-amz-content-sha256:' + payload_hash,
               'Authorization:' + authorization_header]
    return headers



