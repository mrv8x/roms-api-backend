
# Features
- Generates changelogs automatically from device trees in your org
- Create a changelog-page to telegraph
- Upload builds to your GDrive
- Posts automatically builds with changelogs, device name, rom banner, maintainer name and download link in your telegram channel
- Docker support
- Firebase support
- Checkout [SwaggerHUB](https://app.swaggerhub.com/apis/Billaids/ROMS-REST-API/0.1.0) for requests
---
# Show pics or it didn't happen
<p align="center">
	<img src="https://i.imgur.com/opuyhXL.png" width="450">
</p>

<p><b>Generated log <a href="https://telegra.ph/DerpFest-for-violet-04-06-54">example</a></b></p>

# How to deploy?
## Installing requirements
- Clone this repo, install requirements and generate Google Drive token:
<div class="termy">

```console
$ git clone https://github.com/roms-api-backend

$ cd roms-api-backend

$ python3 -m pip install -r requirements.txt

$ python3 starter.py

```
</div>

## Setting up config file
<details>
    <summary><b>Click here for more details</b></summary>

Fill up rest of the fields. Meaning of each fields are described below:
- **devices_org**: This is the name of your github organization.
- **github_token**: This is your github token.
- **drive_id**: This is the folder ID of the Google Drive Folder to where you upload your builds.
- **firebase_cred_file**: This is the path to your firebase credential file.
- **firebase_project_id**: This the id of your firebase project id, check url after you created a project
- **firebase_collection_user**: This is the name of the collection for user authentification.
- **firebase_collection_admin**: This is the name of the collection for admin authentification.
- **firebase_rldb**: This is the url of your firebase realtime database.
- **firebase_rldb_builds_db**: This is the collection name where save informations about builds.
- **rom_name**: This is the name of your rom.
- **author_name**: This is the author name for telegraph posts.
- **rom_pic_url**: This the rom banner url
- **telegram_token**: The telegram bot token that you get from [@Bot](https://t.me/Botr)
- **channel_name**:  This is the name of your telegram channel for example @channel123
- **support_group**: This is the support group name for example @mrv8x
- **devices_url**: This is the direct link to your devices.yaml file in your organization
</details>

## Create a firebase instance
- Visit [Firebase Console](https://console.firebase.google.com/)
- Create a project
- Type in a project name
- Create a Firestore Database and choose Productionmode
- Go to Projectsettings and go to service account, then click on Firebase Admin SDK and create your private key (add it later to roms-api-backend as firebase_credentials.json)
- Create a Realtime Database and choose lockmode
- Copy your database url (in config: firebase_rldb)

## Getting Google OAuth API credential file for Google Drive

- Visit the [Google Cloud Console](https://console.developers.google.com/apis/credentials)
- Go to the OAuth Consent tab, fill it, and save.
- Go to the Credentials tab and click Create Credentials -> OAuth Client ID
- Choose Desktop and Create.
- Use the download button to download your credentials.
- Move that file to the root of roms-api-backend, and rename it to credentials.json
- Visit [Google API page](https://console.developers.google.com/apis/library)
- Search for Drive and enable it, if it is disabled
- Finally, start roms-api-backend and generate your **token.json** file for Google Drive:
<div class="termy">

```console
$ python3 starter.py
```
</div>
    
## How to add an admin?
- Please execute only after the firebase instance has been created and the config file is complete!
- The return value will be your token, you need this token to upload builds and add other users
<div class="termy">

```console
$ python3 starter.py DEVICE USERNAME
```
</div>

## How to add an user?
<div class="termy">

```console
$ curl -X POST -d \
        '{"devices":["YOURDEVICE"],"token":"YOURADMINTOKEN","name":"NEWUSER","admin":"ADMINNAME"}' \
        http://GET.YOUROWN.DOMAIN/auth/add_user
```
</div>

<details>
    <summary><b>Click here for more details</b></summary>

Replace rest of the fields. Meaning of each fields are described below:
- **devices**: Add one or several devices with their codenames from new user
- **token**: Admin authentication token
- **name**: Name from new user
- **admin**: Name from Admin

</details>

## How get device.yaml?
- Create in your organization a repository, for example [official_devices](https://github.com/stormbreaker-project/official_devices), and add a devices.yaml file like [here](https://github.com/roms-rest-api/roms-api-backend/blob/master/devices_example.yaml) with same syntax
- You have to use the predefined fields, otherwise the program may not work.

## Deploying
### Deploy it with docker
- Clone [Traefik-Configs](https://github.com/roms-rest-api/traefik-configs) and follow the instructions in readme file

- Create your Google Drive token:

<div class="termy">

```console
$ python3 starter.py
```
</div>


- Build Docker image:
<div class="termy">

```console
$ sudo docker build . -t backend
```
</div>

- Replace your domain name in docker-compose-yml

- Run the image, if you replaced your domain name in docker-compose.yml:
<div class="termy">

```console
$ sudo docker-compose up -d
```
</div>

## Without docker:
<div class="termy">

```console
$ python3 -m uvicorn api:app --reload --host 0.0.0.0 (use gunicorn in production)

```
</div>

## How to upload builds?
This is an example for uploading builds. Replace your values with ones written in caps lock.
<div class="termy">

```console
$  curl -X 'POST' 'https://api.YOUR.DOMAIN/api/upload' \   
                    -H 'accept: application/json' \  
                    -H 'Content-Type: multipart/form-data' \
                    -F 'codename=DEVICENAME' 
                    -F 'version=YOURANDROIDVERSION' \   
                    -F 'username=YOURUSERNAME' \  
                    -F 'file=@PATH/TO/YOUR/BUILD.ZIP;type=text/plain' \
                    -F 'token=YOURTOKEN' \
```
</div>

<details>
    <summary><b>Click here for more details</b></summary>

Replace rest of the fields. Meaning of each fields are described below:
- **codename**: Codename from device, for example violet
- **version**: Android version, for example eleven-plus
- **username**: Username
- **file**: Path to your build, for example $OUT/lineage-18.1-20210413-UNOFFICIAL-billie.zip
- **token**: Authentication token

</details>
