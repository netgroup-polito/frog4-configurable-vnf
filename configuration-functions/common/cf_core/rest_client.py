from requests.exceptions import HTTPError
import requests
import logging

class RestClient():

    def get(self, url):
        headers = {'Content-type': 'application/json'}
        try:
            resp = requests.get(url, headers=headers)
            resp.raise_for_status()
            return resp.json()
        except HTTPError as err:
            raise err
        except Exception as ex:
            raise ex

    def post(self, url, data):
        headers = {'Content-type': 'application/json'}
        try:
            resp = requests.post(url, data=data, headers=headers)
            resp.raise_for_status()
            return resp.text
        except HTTPError as err:
            raise err
        except Exception as ex:
            raise ex

    def put(self, url, data):
        headers = {'Content-type': 'application/json'}
        try:
            resp = requests.put(url, data=data, headers=headers)
            resp.raise_for_status()
            return resp.text
        except HTTPError as err:
            raise err
        except Exception as ex:
            raise ex

    def delete(self, url):
        try:
            logging.debug("DELETE: " + url)
            #resp = requests.delete(self.delete_url % (nffg_id), headers=self.headers)
            #resp.raise_for_status()
            #return resp.text
        except HTTPError as err:
            raise err
        except Exception as ex:
            raise ex