from datetime import datetime


class Parser:
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
            completed_date = datetime.strptime(condo_data['building_info']['Date Completed'], '%B %Y').isoformat()
            condo_data['building_info']['Date Completed'] = completed_date
        else:
            pass

        return condo_data

    def parse_locations(self, description):
        city = description['addresses'][0]['city']
        country = description['addresses'][0]['country']
        state = description['addresses'][0]['region']
        location_data = {'city': city,
                         'country': country,
                         'state': state}

parser = Parser()
