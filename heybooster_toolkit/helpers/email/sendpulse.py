import requests
from utils import HTTPMethods, AuthenticationError, CredentialsError, InvalidResponseError, RetryLimitExceededError

class SendPulse:
    """ SendPulse SMTP API """

    def __init__(self, client_id: str, client_secret: str):
        """
            :client_id:     string, SendPulse client id
            :client_secret: string, SendPulse client secret key
        """
        self._base_url = 'https://api.sendpulse.com/'
        self._client_id = client_id
        self._client_secret = client_secret
        self._access_token = self.__get_access_token()
        
    
    def __perform_request(self, path: str, http_method: int, params: dict={}, json: dict={}, use_access_token: bool=True, retry: bool=True) -> dict:
        """
            Sends request and refreshes access_token if necessary 

            :path:             string, added to end of the base url
            :http_method:      int, enum from HTTPMethods
            :params:           dict, request parameters
            :json:             dict, request body
            :use_access_token: bool, whether header must include access_token
            :retry:            bool, if true retry on authentication failure 

            return response body from Sendpulse
        """
        url = self._base_url + path
        headers = {'Authorization': 'Bearer ' + self._access_token} if use_access_token else {}

        if http_method == HTTPMethods.GET:
            response = requests.get(url, headers=headers, params=params)
        elif http_method == HTTPMethods.POST:
            response = requests.post(url, headers=headers, params=params, json=json)
        elif http_method == HTTPMethods.PUT:
            response = requests.put(url, headers=headers, params=params, json=json)
        else:
            response = requests.put(url, headers=headers, params=params, json=json)

        try:
            response = response.json()
        except:
            raise InvalidResponseError('Unknown responseL {}'.format(response))

        if response.get('error_code'):
            if response['error_code'] == 5:
                if retry:
                    self._access_token = self.__get_token()
                    return self.__perform_request(path, http_method, params, json, use_access_token, False)
                else:
                    raise AuthenticationError('SendPulse authentication failed.')
            elif not retry:
                raise RetryLimitExceededError
        
        return response


    def __get_access_token(self, path: str='oauth/access_token') -> str:
        """
            Gets access token

            :path: string, added to end of the base url

            return str, access token
        """
        data = {
            'grant_type': 'client_credentials',
            'client_id': self._client_id,
            'client_secret': self._client_secret,
        }
        
        try:
            return requests.post(self._base_url+path, json=data).json()['access_token']
        except KeyError:
            raise KeyError
        except:
            raise CredentialsError('Check your credentials.')


    def send_email_with_template(self, subject: str, template_id: str, variables: dict, from_name: str, from_email: str, to_data: list):
        """
            Sends email by using templates on Sendpulse

            :subject:     string, email subject
            :template_id: string, template_id on SenpPulse
            :variables:   dict, {<variable_name>: <value>}
            :from_name:   string, email sender's name
            :from_email:  string, email sender's adress
            :to_data:     list, [{'name': <to_name>, 'email': <to_email>}]

            return response body from Sendpulse
        """
        
        email = {
            'subject': subject,
            'template': {
                'id': template_id,
                'variables': variables
            },
            'from': {
                'name': from_name,
                'email': from_email
            },
            'to': to_data
        }

        return self.__perform_request('smtp/emails', HTTPMethods.POST, json={'email': email})