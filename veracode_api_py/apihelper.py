#apihelper.py - API class for making network calls

from urllib import parse
import requests
import logging
import json
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from veracode_api_signing.exceptions import VeracodeAPISigningException
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC

from .exceptions import VeracodeAPIError
from .log import VeracodeLog as vlog

logger = logging.getLogger(__name__)

class APIHelper():
    def __init__(self, proxies=None, debug=False):
        self.baseurl = "https://analysiscenter.veracode.com/api"
        requests.Session().mount(self.baseurl, HTTPAdapter(max_retries=3))
        self.proxies = proxies
        self.base_rest_url = "https://api.veracode.com/"
        self.retry_seconds = 120
        self.connect_error_msg = "Connection Error"
        # vlog.setup_logging(self,debug=debug)

    # helper functions

    def _rest_request(self, url, method, params=None,body=None,fullresponse=False):
        # base request method for a REST request
        myheaders = {"User-Agent": "api.py"}
        if method in ["POST", "PUT"]:
            myheaders.update({'Content-type': 'application/json'})

        retry_strategy = Retry(total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"]
            )
        session = requests.Session()
        session.mount(self.base_rest_url, HTTPAdapter(max_retries=retry_strategy))

        try:
            if method == "GET":
                request = requests.Request(method, self.base_rest_url + url, params=params, auth=RequestsAuthPluginVeracodeHMAC(), headers=myheaders)
                prepared_request = request.prepare()
                r = session.send(prepared_request, proxies=self.proxies)
            elif method == "POST":
                r = requests.post(self.base_rest_url + url,params=params,auth=RequestsAuthPluginVeracodeHMAC(),headers=myheaders,data=body)
            elif method == "PUT":
                r = requests.put(self.base_rest_url + url,params=params,auth=RequestsAuthPluginVeracodeHMAC(), headers=myheaders,data=body)
            elif method == "DELETE":
                r = requests.delete(self.base_rest_url + url,params=params,auth=RequestsAuthPluginVeracodeHMAC(),headers=myheaders)
            else:
                raise VeracodeAPIError("Unsupported HTTP method")
        except requests.exceptions.RequestException as e:
            logger.exception(self.connect_error_msg)
            raise VeracodeAPIError(e)

        if not (r.status_code == requests.codes.ok):
            logger.debug("API call returned non-200 HTTP status code: {}".format(r.status_code))

        if not (r.ok):
            logger.debug("Error retrieving data. HTTP status code: {}".format(r.status_code))
            if r.status_code == 401:
                logger.exception("Error [{}]: {} for request {}. Check that your Veracode API account credentials are correct.".format(r.status_code,
                                r.text, r.request.url))
            else:
                logger.exception("Error [{}]: {} for request {}".
                    format(r.status_code, r.text, r.request.url))
            raise requests.exceptions.RequestException()

        if fullresponse:
            return r

        if r.text != "":
            return r.json()
        else:
            return ""

    def _rest_paged_request(self, uri, method, element, params=None):
        all_data = []
        page = 0
        more_pages = True

        while more_pages:
            params['page']=page
            page_data = self._rest_request(uri,method,params)
            total_pages = page_data.get('page', {}).get('total_pages', 0)
            data_page = page_data.get('_embedded', {}).get(element, [])
            all_data += data_page  
            
            page += 1
            more_pages = page < total_pages
        return all_data

    def _xml_request(self, url, method, params=None):
        # base request method for XML APIs, handles what little error handling there is around these APIs
        if method not in ["GET", "POST"]:
            raise VeracodeAPIError("Unsupported HTTP method")

        try:
            session = requests.Session()
            session.mount(self.baseurl, HTTPAdapter(max_retries=3))
            request = requests.Request(method, url, params=params, auth=RequestsAuthPluginVeracodeHMAC(),headers={"User-Agent": "api.py"})
            prepared_request = request.prepare()
            r = session.send(prepared_request, proxies=self.proxies)
            if 200 <= r.status_code <= 299:
                if r.status_code == 204:
                    #retry after wait
                    time.sleep(self.retry_seconds)
                    return self._request(url,method,params)
                elif r.content is None:
                    logger.debug("HTTP response body empty:\r\n{}\r\n{}\r\n{}\r\n\r\n{}\r\n{}\r\n{}\r\n"
                                  .format(r.request.url, r.request.headers, r.request.body, r.status_code, r.headers, r.content))
                    raise VeracodeAPIError("HTTP response body is empty")
                else:
                    return r.content
            else:
                logger.debug("HTTP error for request:\r\n{}\r\n{}\r\n{}\r\n\r\n{}\r\n{}\r\n{}\r\n"
                              .format(r.request.url, r.request.headers, r.request.body, r.status_code, r.headers, r.content))
                raise VeracodeAPIError("HTTP error: {}".format(r.status_code))
        except requests.exceptions.RequestException as e:
            logger.exception("Connection error")
            raise VeracodeAPIError(e)