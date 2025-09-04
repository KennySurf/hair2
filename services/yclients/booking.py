import requests
from os import getenv
from dotenv import load_dotenv

load_dotenv()

HEADERS = {
    'Accept': 'application/vnd.yclients.v2+json',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {getenv("YCLIENTS_TOKEN")}'
}
COMPANY_ID = getenv("YCLIENTS_COMPANY_ID")
FROM_ID = getenv("YCLIENTS_FROM_ID")

#testfields
#serviceid 10928000
#masterid 4066437

def get_services():
    url = f'https://api.yclients.com/api/v1/book_services/{COMPANY_ID}'

    response = requests.get(url, headers=HEADERS)
    response_json = response.json()
    return {i['id']: i['title'] for i in response_json['data'].get('services', [])}

def get_masters(service_id):
    url = f'https://api.yclients.com/api/v1/book_staff/{COMPANY_ID}'

    body = {
        'services_ids': service_id
    }

    response = requests.get(url, headers=HEADERS, params=body)
    response_json = response.json()
    return {i['id']: i['name'] + ' ' + i['specialization'] for i in response_json.get('data', [])}

def get_time(service_id, master_id, date):
    url = f'https://api.yclients.com/api/v1/book_times/{COMPANY_ID}/{master_id}/{date}'

    body = {
        'services_ids': service_id
    }

    response = requests.get(url, headers=HEADERS, params=body)
    response_json = response.json()
    print(response_json)
    return [i.get('time') for i in response_json['data']]

def make_booking(phone, name, email, service_id, master_id, time):
    url = f'https://api.yclients.com/api/v1/book_record/{COMPANY_ID}'

    body = {
        'phone': phone,
        'fullname': name,
        'email': email,
        'appointments': [{
            'id':FROM_ID,
            'services': service_id,
            'staff_id': master_id,
            'datetime': time,
        }]
    }

# print(get_time('10928000', '3766969', '2025-09-06'))
# print(get_masters('10928000'))
# print(get_services())