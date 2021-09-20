import requests
from .utils import HTTPMethods, AuthenticationError, SendProcessFailureError
from .statics import BASE_URL, ACCESS_URL_PATH, SMTP_URL_PATH

class SendPulse:
    """ SendPulse SMTP API """

    def __init__(self, client_id: str, client_secret: str):
        """
            :client_id:     string, SendPulse client id
            :client_secret: string, SendPulse client secret key
        """
        self._client_id = client_id
        self._client_secret = client_secret
        self._access_token = self.__get_access_token()


    def get_url(self, path: str=''):
        """
            Concanates path and url

            :path: string

            return concanated url
        """
        return BASE_URL + path


    def __get_header(self, use_access_token: bool=True):
        """
            Returns needed header

            return dict
        """
        return {'Authorization': 'Bearer ' + self._access_token} if use_access_token else {}


    def __perform_request(self, path: str, http_method: HTTPMethods, params: dict={}, body: dict={}, use_access_token: bool=True) -> dict:
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
        request = getattr(requests, http_method.name)

        return request(
            url=self.get_url(path),
            headers=self.__get_header(use_access_token=use_access_token),
            params=params,
            json=body
        )

    
    def refresh_token(self):
        """
            Gets new access token
        """
        self._access_token = self.__get_access_token()


    def __get_access_token(self) -> str:
        """
            Gets access token

            :path: string, added to end of the base url

            return str, access token
        """
        response = self.__perform_request(path=ACCESS_URL_PATH, http_method=HTTPMethods.post, use_access_token=False, body={
            'grant_type': 'client_credentials',
            'client_id': self._client_id,
            'client_secret': self._client_secret,
        })

        if response.status_code == 200:
            return response.json()['access_token']
        else:
            raise AuthenticationError


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
        try:
            return self.__perform_request(path=SMTP_URL_PATH, http_method=HTTPMethods.post, body={'email': {
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
            }}).json()
        except:
            raise SendProcessFailureError


    def send_email(self, subject: str, html: str, text: str, from_name: str, from_email: str, to_data: list):
        """
            Sends email by using templates on Sendpulse

            :subject:     string, email subject
            :html:        string, html of email encoded in Base64
            :text:        string, text of email
            :from_name:   string, email sender's name
            :from_email:  string, email sender's adress
            :to_data:     list, [{'name': <to_name>, 'email': <to_email>}]

            return response body from Sendpulse
        """
        try:
            return self.__perform_request(path=SMTP_URL_PATH, http_method=HTTPMethods.post, body={'email': {
                'subject': subject,
                'html': html,
                'text': text,
                'from': {
                    'name': from_name,
                    'email': from_email
                },
                'to': to_data
            }}).json()
        except:
            raise SendProcessFailureError
