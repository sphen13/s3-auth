**** This is a work in progress. Better documentation to follow.


##Getting Started
What you need:  
* An AWS account
* A s3 bucket
* IAM user with limited policy (optional)
* [munki](https://github.com/munki/munki)


###Bucket
Create your s3 bucket and add you repo files to it. There are many ways to get your files in there.  
Cyberduck, s3cmd, aws cli. to name a few

###IAM User
Amazon Identity and Access Management (IAM) is used to authenticate access to the various services. You'll find it listed in the [AWS console](https://console.aws.amazon.com/console/home)

###Installing
Since these headers are created for each request we need to (at this time) mess with munki to get it to work.  
I don't really like it but its the only way to get it to work.  

######Step 1:  
copy `s3.py` into `/usr/local/munki/munkilib/`  
######Step 2:  
open `/usr/local/munki/munkilib/updatecheck.py` in your favourite text editor  

```#!python
def getResourceIfChangedAtomically(
        url, destinationpath, message=None, resume=False, expected_hash=None,
        verify=False):

    '''Gets a given URL from the Munki server.
    Adds any additional headers to the request if present'''

    # Add any additional headers specified in ManagedInstalls.plist.
    # AdditionalHttpHeaders must be an array of strings with valid HTTP
    # header format. For example:
    # <key>AdditionalHttpHeaders</key>
    # <array>
    #   <string>Key-With-Optional-Dashes: Foo Value</string>
    #   <string>another-custom-header: bar value</string>
    # </array>
    custom_headers = munkicommon.pref(
        munkicommon.ADDITIONAL_HTTP_HEADERS_KEY)

    if 's3.amazonaws.com' in url:                 #  Add these
        from s3 import s3_auth_headers			  #  Three
        custom_headers = s3_auth_headers(url)     #  Lines

```
######Step 3:  
Add your IAM access creds to the managed installs preference file.  
As well as the region for your bucket.  
```!#bash
sudo defaults write /Library/Preferences/ManagedInstalls s3AccessKey 'AKIAIX2QPWZ7EXAMPLE'
sudo defaults write /Library/Preferences/ManagedInstalls s3SecretKey 'z5MFJCcEyYBmh2BxbrlZBWNJ4izEXAMPLE'
sudo defaults write /Library/Preferences/ManagedInstalls s3Region 'us-west-2'
```
######Step 4:
Change your repo to point to your s3 bucket.  
```!#bash
sudo defaults write /Library/Preferences/ManagedInstallsSoftwareRepoURL  "https://S3_BUCKET_GOES_HERE.s3.amazonaws.com"
```
