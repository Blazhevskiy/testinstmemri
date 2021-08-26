from __future__ import print_function

import time
import logging
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from .parser import parser

logger = logging.getLogger(__name__)


class People_API:
    SCOPES = ["https://www.googleapis.com/auth/contacts.readonly"]

    def get_credentials(self):
        creds = None

        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", self.SCOPES)
                creds = flow.run_local_server(port=0)

            with open("token.json", "w") as token:
                token.write(creds.to_json())

        service = build("people", "v1", credentials=creds)
        return service

    def get_contacts(self, service):
        next_page_token = None
        while True:
            results = (
                service.people()
                .connections()
                .list(
                    resourceName="people/me",
                    personFields=(
                        "addresses,biographies,clientData,coverPhotos,emailAddresses,locales,locations,memberships,metadata,"
                        "miscKeywords,names,nicknames,occupations,organizations,phoneNumbers,photos,relations,sipAddresses,"
                        "urls,userDefined"
                    ),
                    pageToken=next_page_token,
                )
                .execute()
            )
            condos_data = self.prepare_contacts_data(results.get("connections", []))
            next_page_token = results.get('nextPageToken', None)

            if not next_page_token:
                break
        return condos_data

    def prepare_contacts_data(self, raw_data):
        data = []
        for _data in raw_data:
            try:
                condo_description = _data["biographies"][0]["value"]
                parse_condo_description = parser.parse_description(condo_description)

                condo_data = {
                    "condo": {
                        "condo_name": _data["names"][0]["displayName"],
                        "picture": _data["photos"][0].get("url") if _data.get("photos") else None,
                        "description": parse_condo_description["description"],
                        "condo_corp": parse_condo_description["building_info"].get("Condo Corp"),
                        "floors": parse_condo_description["building_info"].get("Floors"),
                        "units": parse_condo_description["building_info"].get("Units"),
                        "date_completed": parse_condo_description["date_completed"],
                        "modified_date": _data["metadata"]["sources"][0].get("updateTime"),
                        "view_floor_plans": "{'selected_pdf': ' ', 'all_pdf': []}",
                    }
                }
                if _data.get("addresses"):
                    condo_data["addresses"] = parser.parse_address(_data["addresses"])

                if _data.get("phoneNumbers"):
                    condo_data["phones"] = parser.parse_phone(_data["phoneNumbers"])

                if _data.get("emailAddresses"):
                    condo_data["emails"] = parser.parse_email(_data["emailAddresses"])

                if _data.get("organizations"):
                    condo_data["organizations"] = parser.parse_organization(_data["organizations"])

                if parse_condo_description["amenities"]:
                    condo_data["amenities"] = parse_condo_description["amenities"]

                if _data.get("memberships"):
                    condo_data["groups"] = parser.parse_groups(_data["memberships"])

                data.append(condo_data)

            except Exception as e:
                logger.error(f"Cannot parse condo. Error: {e}")
        return data

    def run(self):
        service = self.get_credentials()
        data = self.get_contacts(service)
        return data


people_api = People_API()
