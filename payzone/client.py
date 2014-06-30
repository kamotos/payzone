import json
from requests.auth import HTTPBasicAuth

import requests
from payzone import exceptions


API_BASE = 'https://paiement.payzone.ma'
API_VERSION = '002'


class Customer(object):
    def __init__(self, shopper_id=None, shopper_email=None,
                 ship_to_first_name=None
    ):
        self.shopper_id = shopper_id
        self.shopper_email = shopper_email
        self.ship_to_first_name = ship_to_first_name


class Transaction(object):
    endpoint = "/transaction/"
    api_base = API_BASE
    api_version = API_VERSION

    def __init__(self, auth, api_base=api_base,
                 api_version=api_version):
        self.auth = auth
        self.api_base = api_base
        self.api_version = api_version

    def prepare(self, **params):
        """
        Required fields are:
            * apiVersion
            * customerIP
            * orderID
            * currency
            * amount
            * shippingType : (Physical|Virtual)
            * paymentType
            * ctrlRedirectURL
        """
        url = self.api_base + self.endpoint + "prepare"
        data = self._prepare_post_data(**params)
        response = requests.post(url, data=data, auth=self.auth)
        json_response = response.json()

        if json_response['code'] == '401':
            raise exceptions.MissingParameterError(json_response['message'])
        elif not json_response['code'] == '200':
            raise exceptions.PayzoneError(json_response['message'])

        return json_response

    def _prepare_post_data(self, **params):
        data = {
            'apiVersion': self.api_version,
            'currency': 'MAD'
        }
        data.update(params)
        return json.dumps(data)

    def status(self, merchant_token):
        url = self.api_base + self.endpoint + merchant_token + "/status"
        return requests.get(url, auth=self.auth).json()

    @classmethod
    def get_dopay_url(cls, customer_token):
        return cls.api_base + cls.endpoint + customer_token + "/dopay"


class PayZoneClient(object):
    def __init__(self, username, password, api_base=API_BASE,
                 api_version=API_VERSION):
        self.api_base = api_base
        self.api_version = api_version
        self.username = username
        self.password = password

    @property
    def transaction(self):
        return Transaction(
            self.auth(), api_base=self.api_base, api_version=self.api_version
        )

    def auth(self):
        return HTTPBasicAuth(self.username, self.password)