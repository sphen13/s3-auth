t****This is a work in progress. Better documentation to follow.****


##Getting Started
What you need:  
* An AWS account
* A s3 bucket
* IAM user with limited policy (optional)
* Developement build of munki version 2.6.1.2721 or higher to use middleware. You can find that [here](https://munkibuilds.org/)


###Bucket
Create your s3 bucket and add you repo files to it. There are many ways to get your files in there.  
Cyberduck, s3cmd, aws cli. to name a few

###IAM User
Amazon Identity and Access Management (IAM) is used to authenticate access to the various services. You'll find it listed in the [AWS console](https://console.aws.amazon.com/iam/home)

###Installing

######Step 1:  
Copy `middleware_s3.py` into `/usr/local/munki/`  
```!#bash
sudo curl https://raw.githubusercontent.com/waderobson/s3-auth/master/middleware_s3.py -o /usr/local/munki/middleware_s3.py
```
######Step 3:  
Setup your s3-auth preferences.  
```!#bash
sudo defaults write /Library/Preferences/com.github.waderobson.s3-auth AccessKey 'AKIAIX2QPWZ7EXAMPLE'
sudo defaults write /Library/Preferences/com.github.waderobson.s3-auth SecretKey 'z5MFJCcEyYBmh2BxbrlZBWNJ4izEXAMPLE'
sudo defaults write /Library/Preferences/com.github.waderobson.s3-auth Region 'us-west-2'
```
######Step 4:
Change your repo to point to your s3 bucket.  
```!#bash
sudo defaults write /Library/Preferences/ManagedInstalls SoftwareRepoURL  "https://S3_BUCKET_GOES_HERE.s3.amazonaws.com"
```
