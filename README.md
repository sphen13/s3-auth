**** This is a work in progress. Better documentation to follow.
pull requests welcomed :)

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

```!#bash
sudo defaults write /Library/Preferences/ManagedInstalls s3AccessKey 'AKIAIX2QPWZ7EXAMPLE'
sudo defaults write /Library/Preferences/ManagedInstalls s3AccessKey 'z5MFJCcEyYBmh2BxbrlZBWNJ4izEXAMPLE'
```


###Installing
Since these headers are created for each request we need to (at this time) mess with munki to get it to work.  
I don't really like it but its the only way to get it to work.  

First  
copy s3.py into /usr/local/munki/munkilib/
Second  
Too be continued

