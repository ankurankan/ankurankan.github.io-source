Title: Importing data in Google Colaboratory
date: 2018-02-20
comments: True
slug: importing-data-in-google-colab
tags: Data,Google-Colaboratory

[Google Colaboratory](https://colab.research.google.com/) is a Jupyter Notebook enviornment that doesn't require any setup and completely runs in the cloud.
The notebooks are stored on Google Drive, so it can be easily shared. Over all of this, one of the major selling points is that they are giving 
free computation on GPUs for upto 12 hours in a single session. And because of all these reason, I have been writing all my python code on Google Colab for 
the last couple of weeks. But one of the major issues I faced was importing data to the notebook. Since the intances are created on the fly, the data 
gets deleted once the notebook is closed, so we need to keep on transferring it again and again and there isn't a simple way to transfer data unless you 
have your data hosted somewhere where you can use something like `wget`.

So, I compiled a list of ways to import data to Google Colab:

Using wget
----------
The Google Colab machines are built on Debian based linux, therefore the simplest way for downloading data is `wget` or your faviorite tool for 
downloading data.

```
wget url_to_data
```

Using google.colab python module
--------------------------------
Google Colaboratory provided a python module `google.colab` with some utility tools, one of which is transfering files from/to your local system.
```
from google.colab import files
files.upload()
```
This creates a button using which you can select the files you want to upload. But in my experience till now, this is the worst way since the 
upload was super slow (Took me more than 2 minutes to upload 30 MBs) and no it wasn't my internet. And I couldn't exactly figure out any 
possible reasons for the upload to be so slow.

Mount google drive using google-drive-ocamlfuse
-----------------------------------------------
Another possible option is to use google drive to store your data and mount your google drive on the machine using `google-drive-ocamlfuse`.

Installing `google-drive-ocamlfuse`:
```
!apt-get install -y -qq software-properties-common python-software-properties module-init-tools
!add-apt-repository -y ppa:alessandro-strada/ppa 2>&1 > /dev/null
!apt-get update -qq 2>&1 > /dev/null
!apt-get -y install -qq google-drive-ocamlfuse fuse
```
Authenticate and get credentials:
```
from google.colab import auth
auth.authenticate_user()
from oauth2client.client import GoogleCredentials
creds = GoogleCredentials.get_application_default()
```
Setting up `google-drive-ocamlfuse`:
```
import getpass
!google-drive-ocamlfuse -headless -id={creds.client_id} -secret={creds.client_secret} < /dev/null 2>&1 | grep URL
vcode = getpass.getpass()
!echo {vcode} | google-drive-ocamlfuse -headless -id={creds.client_id} -secret={creds.client_secret}
```
And then you can finally mount your google drive:
```
!mkdir gdrive
!google-drive-ocamlfuse gdrive
!ls gdrive
```

Getting data from google cloud storage using gsutil
---------------------------------------------------
Alternatively you can download data from google cloud storage. 
Start by authenticating the user:
```
from google.colab import auth
auth.authenticate_user()
```
And set the project and download data:
```
project_id = 'Your_project_ID_here'

# Download the file.
!gsutil cp gs://{bucket_name}/{filename} {download_dir}
```

Another possible option is to mount the bucket using [Cloud Storage Fuse](https://cloud.google.com/storage/docs/gcs-fuse) but good luck setting the right permissions to access data :P.
