import json
import requests
from urllib.parse import quote_plus

class HubSpotContactsAPI():

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.hubapi.com/contacts/v1/'

    def get_contact_by_email(self, email):
        """
            Returns contact data for given email
            :email: str, contact email
        """
        encoded_email = quote_plus(email)
        url = f'{self.base_url}/contact/email/{encoded_email}/profile'
        params = {
            'hapikey': self.api_key
        }
        resp = requests.get(url, params=params)
        
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 404:
            return None
        else:
            raise Exception(f'this response status code is not considered before - status code: {resp.status_code}')
    
    def update_contact_by_email(self, email, properties):
        """
            Updates contact for given email properties with given properties
            :email: contact email
            :properties: list, 
            return True if updated successfully
        """
        encoded_email = quote_plus(email)
        data = json.dumps({
            'properties': properties
        })
        params = {
            'hapikey': self.api_key
        }
        url = f'{self.base_url}/contact/email/{encoded_email}/profile'
        headers = {
            'Content-Type': 'application/json'
        }
        resp = requests.post(data=data, url=url, params=params, headers=headers)
        
        if resp.status_code == 204:
            return True
        elif resp.status_code == 400:
            raise Exception(f'{resp.text}')
        elif resp.status_code == 401:
            raise Exception(f'{resp.text}')
        elif resp.status_code == 404:
            raise Exception(f'{resp.text}')
        elif resp.status_code == 500:
            raise Exception(f'{resp.text}')
        else:
            raise Exception(f'this response status code is not considered before - status code: {resp.status_code}')
        
    def create_contact(self, properties=[]):
        """
            Creates contact with given properties (email must be included)
            :properties: list
            return Response.json()
        """
        email_prop_exists = False
        for prop in properties:
            if prop['property'] == 'email' and prop['value']:
                email_prop_exists = True
        if not email_prop_exists:
            raise Exception('Email must be included')
        url = f'{self.base_url}/contact'
        params = {
            'hapikey': self.api_key
        }
        data = json.dumps({
            'properties': properties
        })
        headers = {
            'Content-Type': 'application/json'
        }
        resp = requests.post(data=data, url=url, params=params, headers=headers)

        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 400:
            raise Exception(f'{resp.text}')
        elif resp.status_code == 409:
            raise Exception(f'{resp.text}')
        else:
            raise Exception(f'this response status code is not considered before - status code: {resp.status_code}')

    def delete_contact_by_email(self, email: str):
        """
            Deletes contact for given email
            :email: contact email
            return response.json()
        """
        contact = self.get_contact_by_email(email)
        
        if contact:
            contact_id = contact['vid']
            url = f'{self.base_url}/contact/vid/{contact_id}'
            params = {
                'hapikey': self.api_key
            }
            resp = requests.delete(url, params=params)
            
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 401:
                raise Exception(f'{resp.text}')
            elif resp.status_code == 404:
                raise Exception(f'{resp.text}')
            elif resp.status_code == 500:
                raise Exception(f'{resp.text}')
            else:
                raise Exception(f'this response status code is not considered before - status code: {resp.status_code}')
