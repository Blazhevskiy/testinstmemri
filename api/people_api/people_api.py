from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import re

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
            personFields='addresses,ageRanges,biographies,birthdays,calendarUrls,clientData,coverPhotos,emailAddresses,events,externalIds,genders,imClients,interests,locales,locations,memberships,metadata,miscKeywords,names,nicknames,occupations,organizations,phoneNumbers,photos,relations,sipAddresses,skills,urls,userDefined').execute()
        condos_data = self.prepare_contacts_data(results.get('connections', []))
        return condos_data

    def prepare_contacts_data(self, raw_data):
        data = []
        for condo_data in raw_data:
            name = condo_data['names'][0]['displayName']
            picture = condo_data['photos'][0]['url']
            street_name = condo_data['addresses'][0]['streetAddress']
            street_address = condo_data['addresses'][0]['formattedValue'].replace('\n', ' ')
            district = condo_data['addresses'][0]['region']
            province = condo_data['addresses'][0]['city']
            zip_code = condo_data['addresses'][0]['postalCode']
            note = condo_data['biographies'][0]['value']
            description = condo_data['biographies'][0]['value']
            #amenities
            condo_corp_match = re.search("Condo Corp: (.*)", description)[0].split(' ')
            condo_corp = condo_corp_match[2]
            data.append({'displayName': name,
                         'picture': picture,
                         'street_name': street_name,
                         'street_address': street_address,
                         'district': district,
                         'province': province,
                         'zip_code': zip_code,
                         'note': note,
                         'description': description,
                         'condo_corp': condo_corp,
                         })
        return data

    def run(self):
        service = self.get_credentials()
        data = self.get_contacts(service)
        return data

people_api = People_API()
