from pprint import pprint
import pickle
import os.path
import socket
import json
import sys

from googleapiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


socket.setdefaulttimeout(120)

SCOPES = ['https://www.googleapis.com/auth/forms',
          'https://www.googleapis.com/auth/script.send_mail',
          'https://www.googleapis.com/auth/script.projects']

MANIFEST = '''
{
    "timeZone": "America/New_York",
    "exceptionLogging": "STACKDRIVER",
    "executionApi": {
        "access": "ANYONE"
    }
}
'''.strip()


def login():
    try:
        creds = None
        cred_path = 'credentials/'
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    cred_path + 'google_credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('script', 'v1', credentials=creds)
        pprint('Login successful')
        return service

    except Exception as e:
        pprint(f'Login failure: {e}')
        return None


def update_project(service, script_id, form_url):
    # Read from file code we want to deploy
    with open('export-google-form.gs', 'r') as f:
        sample_code = f.read()

    sample_code = sample_code.replace('<YOUR_FORM_URL>', form_url)

    # Upload two files to the project
    request = {
        'files': [{
            'name': 'hello',
            'type': 'SERVER_JS',
            'source': sample_code
        }, {
            'name': 'appsscript',
            'type': 'JSON',
            'source': MANIFEST
        }
        ]
    }

    # Update files in the project
    service.projects().updateContent(
        body=request,
        scriptId=script_id
    ).execute()

    pprint('Project was successfully updated')


# Get JSON, which is returned by script
def get_json(service, script_id, file_name):
    body = {
        "function": "main",
        "devMode": True
    }
    # Get JSON from script
    resp = service.scripts().run(scriptId=script_id, body=body).execute()

    # Write out JSON to file
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(resp['response']['result'], f, ensure_ascii=False, indent=4)

    pprint('Form was successfully exported')


def main():

    try:

        args = sys.argv
        if len(args) != 4:
            raise TypeError('Not enough arguments. Three arguments required: <json_file_name>, <script_id> and '
                            '<google_form_url>')
        file_name = args[1]
        script_id = args[2]
        form_url = args[3]

        service = login()

        update_project(service, script_id, form_url)

        get_json(service, script_id, file_name)

    except (errors.HttpError, ) as error:
        # The API encountered a problem.
        pprint(error.content.decode('utf-8'))


if __name__ == '__main__':
    main()

