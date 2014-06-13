import json
from requests.auth import HTTPBasicAuth

import requests
from payzone import exceptions


api_base = 'https://paiement.payzone.ma'
api_version = '002'


class Customer(object):
    def __init__(self, shopper_id=None, shopper_email=None,
                 ship_to_first_name=None
    ):
        self.shopper_id = shopper_id
        self.shopper_email = shopper_email
        self.ship_to_first_name = ship_to_first_name


class Transaction(object):
    endpoint = "/transaction/"

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
            * shippingType
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

    def dopay_url(self, customer_token):
        return self.api_base + self.endpoint + customer_token + "/status"


class PayZoneClient(object):
    def __init__(self, username, password, api_base=api_base,
                 api_version=api_version ):
        self.api_base = api_base
        self.api_version = api_version
        self.username = username
        self.password = password

    def prepare_transaction(self, **params):
        return Transaction(
            self.auth(), api_base=api_base, api_version=self.api_version
        ).prepare(**params)

    def auth(self):
        return HTTPBasicAuth(self.username, self.password)