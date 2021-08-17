from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

class People_API():
    SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']

    def get_credentials(self):
        creds = None

        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)

            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('people', 'v1', credentials=creds)
        return service

    def get_contacts(self, service):
        results = service.people().connections().list(
            resourceName='people/me',
            personFields='names,emailAddresses,biographies,organizations,photos,urls,addresses,clientData').execute()
        condos_data = self.prepare_contacts_data(results.get('connections', []))
        return condos_data

    def prepare_contacts_data(self, raw_data):
        data = []
        # TODO prepare data for serializer
        return data

    def run(self):
        service = self.get_credentials()
        data = self.get_contacts(service)
        return data

people_api = People_API()
