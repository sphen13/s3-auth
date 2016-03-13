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
Copy `s3.py` into `/usr/local/sbin/`  
Make sure its executable `sudo chomd +x /usr/local/sbin/s3.py`  
######Step 2:  
Add the executable to `AdditionalHttpHeaders`  
```!#bash
sudo defaults write /Library/Preferences/ManagedInstalls AdditionalHttpHeaders -dict Executable "/usr/local/sbin/s3.py"
```
######Step 3:  
Setup your s3-auth preferences.  
Same way you would setup munkiimport....exactly the same because I stole it from there :) Thanks Greg!  
  
```!#bash
sudo /usr/local/sbin/s3.py --configure
```
######Step 4:
Change your repo to point to your s3 bucket.  
```!#bash
sudo defaults write /Library/Preferences/ManagedInstalls SoftwareRepoURL  "https://S3_BUCKET_GOES_HERE.s3.amazonaws.com"
```
