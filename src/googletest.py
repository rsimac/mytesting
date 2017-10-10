from __future__ import print_function

import httplib2
import os
import time


from apiclient import discovery
from apiclient.http import MediaFileUpload

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import oauth2client.service_account



try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = ['https://www.googleapis.com/auth/drive'] #.metadata.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'

def get_credentials(credential_path="./creds/credentials.json"):
    
    credentials = oauth2client.service_account.ServiceAccountCredentials.from_json_keyfile_name(credential_path, SCOPES)
    
    return credentials

def get_service(credential_path="./creds/credentials.json"):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    
    return service

    
# drive apis here: https://developers.google.com/resources/api-libraries/documentation/drive/v3/python/latest/drive_v3.files.html


def get_credentials_old():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    
    '''
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')
    '''
    credential_path = "./creds/credentials.json"
    
    #store = Storage(credential_path)
    
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credential_path, SCOPES)
    
    #credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    
    upload_file(service, "c:/users/user/videos/motion/20171008_210735.H264")
    
    results = service.files().list(
        pageSize=10,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))
            
            #service account (this) sharing the file with other (me)
            #perm = service.permissions().create(fileId=item['id'], body={"type":"user", "role":"writer", "emailAddress":"robert.simac@gmail.com"})
            #perm.execute()
            
    #upload: https://developers.google.com/drive/v3/web/manage-uploads
    #create folder https://developers.google.com/drive/v3/web/folder

    
def upload_file(service, filename):
    max_retries = 5;
    
    file_metadata = {'name': filename.split('/')[-1]}
    
    media = MediaFileUpload(filename, mimetype='video/h264') #ASSumed
    
    file_id = None
    
    try:
        file_id = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        
    except Exception as e:
        print("Failed uploading the file, continuing. Exception: {}".format(e))
        
    if file_id:
        
        for i in range(max_retries):
            try:
                perm = service.permissions().create(fileId=file_id['id'], body={"type":"user", "role":"reader", "emailAddress":"robert.simac@gmail.com"}) #ASSumed
                perm.execute()
                break
            except Exception as e:
                print ("Failed changing permission, retrying {}/{}. Exception: {}".format(i,max_retries,e))
                time.sleep(1)
                
    
        for i in range(max_retries):
            try:
                perm = service.permissions().create(fileId=file_id['id'], body={"type":"user", "role":"owner", "emailAddress":"robert.simac@gmail.com"}, transferOwnership=True)
                perm.execute()
                break
            except Exception as e:
                print ("Failed changing ownership, retrying {}/{}. Exception: {}".format(i,max_retries,e))
                time.sleep(1)

            

    return file_id
    
    
    
    

if __name__ == '__main__':
    main()