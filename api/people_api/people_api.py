from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from datetime import datetime

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

    def parse_description(self, description):
        head, condo_description, body, bottom = description.split('\n\n')
        params = []
        building_info = {}
        for head in head.split('\n'):
            if ":" not in head:
                params.append(head)
            else:
                key, value = head.split(':')
                building_info[key] = value.strip()
        amenities = body.split('\n')[1:]
        str1 = ""
        for ele in amenities:
            str1 += ',' + ele
        amenities = str1[1:]
        condo_data = {'params': params,
                      'building_info': building_info,
                      'description': condo_description,
                      'amenities': amenities}

        # Change string date to datetime
        data = condo_data.get('building_info')
        completed_date = data.get('Date Completed')
        if completed_date:
            completed_date = datetime.strptime(condo_data['building_info']['Date Completed'], '%B %Y')
            condo_data['building_info']['Date Completed'] = completed_date
        else:
            pass

        return condo_data

    def prepare_contacts_data(self, raw_data):
        data = []
        for condo_data in raw_data:
            condo_description = condo_data['biographies'][0]['value']
            parse_condo_description = self.parse_description(condo_description)

            name = condo_data['names'][0]['displayName']
            picture = condo_data['photos'][0]['url']
            street_name = condo_data['addresses'][0]['streetAddress']
            street_address = condo_data['addresses'][0]['formattedValue'].replace('\n', ' ')
            district = condo_data['addresses'][0]['region']
            province = condo_data['addresses'][0]['city']
            zip_code = condo_data['addresses'][0]['postalCode']
            note = parse_condo_description['description']
            description = condo_data['biographies'][0]['value']
            condo_corp = parse_condo_description['building_info']['Condo Corp']
            amenities = parse_condo_description['amenities']
            floors = parse_condo_description['building_info']['Floors']
            units = parse_condo_description['building_info']['Units']
            data_completed = parse_condo_description['building_info']['Date Completed']
            data.append({'displayName': name,
                         'picture': picture,
                         'street_name': street_name,
                         'street_address': street_address,
                         'district': district,
                         'province': province,
                         'zip_code': zip_code,
                         'note': note,
                         'description': description,
                         'amenities': amenities,
                         'condo_corp': int(condo_corp),
                         'floors': int(floors),
                         'units': int(units),
                         'date_completed': data_completed,
                         'view_floor_plans': "{'selected_pdf': ' ', 'all_pdf': []}"
                         })
        return data

    def run(self):
        service = self.get_credentials()
        data = self.get_contacts(service)
        return data

people_api = People_API()
