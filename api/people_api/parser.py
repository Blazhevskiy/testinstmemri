from contextlib import suppress
from datetime import datetime


class Parser:
    def parse_description(self, description):
        head, condo_description, *other = description.split("\n\n")
        params = []
        building_info = {}
        amenities = []

        for head in head.split("\n"):
            if ":" not in head:
                params.append(head)
            else:
                key, value = head.split(":")
                value = value.strip()
                if value:
                    building_info[key] = value

        if other:
            amenities = [{"name": amenity} for amenity in other[0].split("\n")[1:]]

        # Change date frormat from 'October 2017' to '2017-11-01T00:00:00'
        completed_date = None
        if building_info.get("Date Completed"):
            with suppress(ValueError):
                completed_date = datetime.strptime(building_info.get("Date Completed"), "%B %Y").isoformat()

        return {
            "params": params,
            "building_info": building_info,
            "description": condo_description,
            "amenities": amenities,
            "date_completed": completed_date,
        }

    def parse_address(self, addresses):
        result = []
        for address in addresses:
            result.append(
                {
                    "city": address.get("city"),
                    "country": address.get("country"),
                    "state": address.get("countryCode"),
                    "street_name": address.get("streetAddress"),
                    "street_address": address.get("formattedValue", "").replace("\n", " "),
                    "district": address.get("region"),
                    "zip_code": address.get("postalCode"),
                }
            )
        return result

    def parse_phone(self, phones):
        result = []
        for phone in phones:
            result.append({"phone_number": phone.get("value"), "phone_number_canonical": phone.get("canonicalForm")})
        return result

    def parse_email(self, emails):
        result = []
        for email in emails:
            result.append({"email": email.get("value")})
        return result

    def parse_organization(self, organizations):
        result = []
        for organization in organizations:
            result.append({"title": organization.get("title"), "name": organization.get("name")})
        return result


parser = Parser()
