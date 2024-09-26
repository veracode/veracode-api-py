# apihelper.py - API class for making network calls

import requests
import logging
import json
import time
from requests.adapters import HTTPAdapter

from veracode_api_signing.exceptions import VeracodeAPISigningException
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC
from veracode_api_signing.credentials import get_credentials
from veracode_api_signing.regions import get_region_for_api_credential

from .exceptions import VeracodeAPIError
from .log import VeracodeLog as vlog
from .constants import Constants

logger = logging.getLogger(__name__)


class APIHelper():
    api_key_id = None
    api_key_secret = None
    region = None

    def __init__(self, debug=False):
        self.baseurl = self._get_baseurl()
        self.base_rest_url = self._get_baseresturl()
        self.retry_seconds = 120
        self.connect_error_msg = "Connection Error"
        # vlog.setup_logging(self,debug=debug)

    # helper functions

    def _get_baseurl(self):
        return self._get_region_url('xml')

    def _get_baseresturl(self):
        return self._get_region_url('rest')

    def _get_region_url(self, type):
        if self.api_key_id is None or self.api_key_secret is None:
            self.api_key_id, self.api_key_secret = get_credentials()
        if self.region is None:
            self.region = get_region_for_api_credential(self.api_key_id)

        if type == 'xml':
            return Constants().REGIONS[self.region]['base_xml_url']
        elif type == 'rest':
            return Constants().REGIONS[self.region]['base_rest_url']

    def _check_for_errors(self,theresponse, *args, **kwargs):
        if theresponse.status_code in (429, 502, 503, 504):
            # retry by populating new prepared request from the request in the response object
            # and recalculating auth
            logger.debug("Retrying request, error code {} received".format(theresponse.status_code))
            session = requests.Session()
            oldreq = theresponse.request
            oldheaders = oldreq.headers
            del oldheaders['authorization']
            newreq = requests.Request(oldreq.method,oldreq.url,auth=RequestsAuthPluginVeracodeHMAC(),
                                      headers=oldheaders)
            return session.send(newreq.prepare())
        
    def _prepare_headers(self,method,apifamily,files=False):
        headers = {"User-Agent": "api.py"}
        if method in ["POST", "PUT"] and apifamily=='json' and not(files):
            headers.update({'Content-type': 'application/json'})
        return headers
                
    def _rest_request(self, url, method, params=None, body=None, fullresponse=False, use_base_url=True, files=None):
        # base request method for a REST request
        if files is None:
            myheaders = self._prepare_headers(method,'json')
        else:
            myheaders = self._prepare_headers(method,'json',files=True)

        session = requests.Session()

        if use_base_url:
            url = self.base_rest_url + url

        try:
            if method == "GET":
                request = requests.Request(method, url, params=params, auth=RequestsAuthPluginVeracodeHMAC(),
                                           headers=myheaders,
                                           hooks={'response': self._check_for_errors})
                prepared_request = request.prepare()
                r = session.send(prepared_request)
            elif method == "POST":
                if files is None:
                    r = requests.post(url, params=params, auth=RequestsAuthPluginVeracodeHMAC(), headers=myheaders,
                                  data=body)
                else:
                    r = requests.post(url, params=params, auth=RequestsAuthPluginVeracodeHMAC(), headers=myheaders,
                                  data=body, files=files)
            elif method == "PUT":
                r = requests.put(url, params=params, auth=RequestsAuthPluginVeracodeHMAC(), headers=myheaders,
                                 data=body)
            elif method == "DELETE":
                r = requests.delete(url, params=params, auth=RequestsAuthPluginVeracodeHMAC(), headers=myheaders)
            else:
                raise VeracodeAPIError("Unsupported HTTP method")
        except requests.exceptions.RequestException as e:
            logger.exception("Error: {}".format(self.connect_error_msg))
            raise VeracodeAPIError(e.text) from e

        if r.status_code != requests.codes.ok:
            logger.debug("API call returned non-200 HTTP status code: {}".format(r.status_code))

        if not (r.ok):
            conv_id = r.headers['x-conversation-id']
            logger.debug("Error retrieving data. HTTP status code: {}, conversation id {}".format(r.status_code,conv_id))
            if r.status_code == 401:
                logger.exception(
                    "Error [{}]: {} for request {}. Check that your Veracode API account credentials are correct.".format(
                        r.status_code,
                        r.text, r.request.url))
            else:
                logger.exception("Error [{}]: {} for request {}".
                                 format(r.status_code, r.text, r.request.url))
                re = requests.exceptions.RequestException()
                re.response = r
                re.errno = r.status_code
                re.request = r.request
            raise re

        if fullresponse:
            return r
        elif r.text != "":
            return r.json()
        else:
            return ""

    def _rest_paged_request(self, uri, method, element, params=None,fullresponse=False):
        all_data = []
        page = 0
        more_pages = True

        while more_pages:
            params['page'] = page
            page_data = self._rest_request(uri, method, params)
            total_pages = page_data.get('page', {}).get('total_pages', 0)
            data_page = page_data.get('_embedded', {}).get(element, [])
            all_data += data_page

            page += 1
            more_pages = page < total_pages
        if page==1 and fullresponse:
            return page_data    
        else:
            return all_data

    def _xml_request(self, url, method, params=None, files=None):
        # base request method for XML APIs, handles what little error handling there is around these APIs
        if method not in ["GET", "POST"]:
            raise VeracodeAPIError("Unsupported HTTP method")

        try:
            session = requests.Session()
            session.mount(self.baseurl, HTTPAdapter(max_retries=3))
            request = requests.Request(method, url, params=params, files=files,
                                       auth=RequestsAuthPluginVeracodeHMAC(), headers=self._prepare_headers(method,'xml'))
            prepared_request = request.prepare()
            r = session.send(prepared_request)
            if 200 <= r.status_code <= 299:
                if r.status_code == 204:
                    # retry after wait
                    time.sleep(self.retry_seconds)
                    return self._xml_request(url,method,params)
                elif r.content is None:
                    logger.debug("HTTP response body empty:\r\n{}\r\n{}\r\n{}\r\n\r\n{}\r\n{}\r\n{}\r\n"
                                 .format(r.request.url, r.request.headers, r.request.body, r.status_code, r.headers,
                                         r.content))
                    raise VeracodeAPIError("HTTP response body is empty")
                else:
                    return r.content
            else:
                logger.debug("HTTP error for request:\r\n{}\r\n{}\r\n{}\r\n\r\n{}\r\n{}\r\n{}\r\n"
                             .format(r.request.url, r.request.headers, r.request.body, r.status_code, r.headers,
                                     r.content))
                raise VeracodeAPIError("HTTP error: {}".format(r.status_code))
        except requests.exceptions.RequestException as e:
            logger.exception("Connection error")
            raise VeracodeAPIError(e)
