#healthcheck.py - API class for Healthcheck API calls

from .apihelper import APIHelper

class Healthcheck():

     def healthcheck(self):
        uri = 'healthcheck/status'
        return APIHelper()._rest_request(uri,"GET")