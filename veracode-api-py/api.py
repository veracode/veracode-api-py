# Purpose:  API utilities
#
# Notes:    API credentials must be enabled on Veracode account and placed in ~/.veracode/credentials like
#
#           [default]
#           veracode_api_key_id = <YOUR_API_KEY_ID>
#           veracode_api_key_secret = <YOUR_API_KEY_SECRET>
#
#           and file permission set appropriately (chmod 600)

from urllib.parse import urlparse
import time
import requests
import logging
from requests.adapters import HTTPAdapter

from veracode_api_signing.exceptions import VeracodeAPISigningException
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC

from .constants import Constants
from .exceptions import VeracodeAPIError

class VeracodeAPI:

    def __init__(self, proxies=None):
        self.baseurl = "https://analysiscenter.veracode.com/api"
        requests.Session().mount(self.baseurl, HTTPAdapter(max_retries=3))
        self.proxies = proxies
        self.base_rest_url = "https://api.veracode.com/"
        self.base_uri = base_uri = "https://api.veracode.com/appsec/v1/applications"
        self.find_uri = "https://api.veracode.com/appsec/v2/applications"
        self.retry_seconds = 120

    # helper functions

    def _request(self, url, method, params=None):
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
                    logging.debug("HTTP response body empty:\r\n{}\r\n{}\r\n{}\r\n\r\n{}\r\n{}\r\n{}\r\n"
                                  .format(r.request.url, r.request.headers, r.request.body, r.status_code, r.headers, r.content))
                    raise VeracodeAPIError("HTTP response body is empty")
                else:
                    return r.content
            else:
                logging.debug("HTTP error for request:\r\n{}\r\n{}\r\n{}\r\n\r\n{}\r\n{}\r\n{}\r\n"
                              .format(r.request.url, r.request.headers, r.request.body, r.status_code, r.headers, r.content))
                raise VeracodeAPIError("HTTP error: {}".format(r.status_code))
        except requests.exceptions.RequestException as e:
            logging.exception("Connection error")
            raise VeracodeAPIError(e)

    def _rest_request(self, url, method, params=None,body=None):
        # base request method for a REST request
        if method in ["GET","POST"]:
            try: 
                session = requests.Session()
                session.mount(self.base_rest_url, HTTPAdapter(max_retries=3))
                request = requests.Request(method, self.base_rest_url + url, params=params, auth=RequestsAuthPluginVeracodeHMAC(), headers={"User-Agent": "api.py"})
                prepared_request = request.prepare()
                r = session.send(prepared_request, proxies=self.proxies)
                if r.status_code == 500 or r.status_code == 504:
                    time.sleep(1)
                    r = requests.Request(method, url, params=params, auth=RequestsAuthPluginVeracodeHMAC(),headers={"User-Agent": "api.py"},json=body)
            except requests.exceptions.RequestException as e:
                logging.exception("Connection error")
                raise VeracodeAPIError(e)
        elif method == "PUT":
            try:
                r = requests.put(self.base_rest_url + url,params=params,auth=RequestsAuthPluginVeracodeHMAC(), headers={"User-Agent": "api.py", 'Content-type': 'application/json'},data=body)
            except requests.exceptions.RequestException as e:
                logging.exception("Connection error")
                raise VeracodeAPIError(e)
        else:
            raise VeracodeAPIError("Unsupported HTTP method")

        if not (r.status_code == requests.codes.ok):
            logging.debug("Error retrieving data. HTTP status code: {}".format(r.status_code))
            if r.status_code == 401:
                logging.exception("Check that your Veracode API account credentials are correct.")
            else:
                logging.exception("Error:" + r.text + " for request " + r.request.url)
            raise requests.exceptions.RequestException()
        else:
            return r.json()

    def _rest_paged_request(self, url, method, element, params=None):
        all_data = []
        page = 0
        more_pages = True

        while more_pages:
            params['page']=page
            page_data = self._rest_request(url,method,params)
            total_pages = page_data.get('page', {}).get('total_pages', 0)
            data_page = page_data.get('_embedded', {}).get(element, [])
            all_data += data_page  
            
            page += 1
            more_pages = page < total_pages
        return all_data

    #xml apis

    def get_app_list(self):
        """Returns all application profiles."""
        return self._request(self.baseurl + "/4.0/getapplist.do", "GET")

    def get_app_info(self, app_id):
        """Returns application profile info for a given app ID."""
        return self._request(self.baseurl + "/5.0/getappinfo.do", "GET", params={"app_id": app_id})

    def get_sandbox_list(self, app_id):
        """Returns a list of sandboxes for a given app ID"""
        return self._request(self.baseurl + "/5.0/getsandboxlist.do", "GET", params={"app_id": app_id})

    def get_build_list(self, app_id, sandbox_id=None):
        """Returns all builds for a given app ID."""
        if sandbox_id is None:
            params = {"app_id": app_id}
        else:
            params = {"app_id": app_id, "sandbox_id": sandbox_id}
        return self._request(self.baseurl + "/4.0/getbuildlist.do", "GET", params=params)
    
    def get_build_info(self, app_id, build_id, sandbox_id=None):
        """Returns build info for a given build ID."""
        if sandbox_id is None:
            params = {"app_id": app_id, "build_id": build_id}
        else:
            params = {"app_id": app_id, "build_id": build_id, "sandbox_id": sandbox_id}
        return self._request(self.baseurl + "/5.0/getbuildinfo.do", "GET", params=params)

    def get_detailed_report(self, build_id):
        """Returns a detailed report for a given build ID."""
        return self._request(self.baseurl + "/5.0/detailedreport.do", "GET", params={"build_id": build_id})

    def set_mitigation_info(self,build_id,flaw_id_list,action,comment):
        """Adds a new mitigation proposal, acceptance, rejection, or comment for a set of flaws for an application."""
        actiontype = Constants.ANNOT_TYPE.get(action, 'comment')        
        payload = {'build_id': build_id, 'flaw_id_list': flaw_id_list, 'action': actiontype, 'comment': comment}
        return self._request(self.baseurl + "/updatemitigationinfo.do", "POST", params=payload)

    def generate_archer(self,payload):
        return self._request(self.baseurl + "/3.0/generatearcherreport.do", "GET",params=payload)

    def download_archer(self, token=None):
        if token==None:
            payload = None
        else:
            payload = {'token': token}

        return self._request(self.baseurl + "/3.0/downloadarcherreport.do", "GET", params=payload)

    # rest apis

    ## Appsec APIs

    def get_apps(self):
        return self._rest_paged_request('appsec/v1/applications',"GET","applications")

    def get_app (self,guid=None,legacy_id=None):
        """Gets a single applications in the current customer account using the Veracode Application API."""
        if legacy_id == None:
            apps_base_uri = "appsec/v1/applications" + "/{}"
            uri = apps_base_uri.format(guid)
        else:
            apps_base_uri = "appsec/v1/applications?legacy_id={}"
            uri = apps_base_uri.format(legacy_id)

        return self._rest_request(uri,"GET")

    def get_policy (self,guid):
        policy_base_uri = "appsec/v1/policies/{}"
        uri = policy_base_uri.format(guid)
        return self._rest_request(uri,"GET")

    def get_findings(self,app):
        #Gets a list of static findings for app using the Veracode Findings API
        request_params = {'include_annot': 'TRUE', 'scan_type': 'STATIC'}
        uri = "appsec/v2/applications/{}/findings".format(app)
        return self._rest_paged_request(uri,"GET","findings",request_params)

    ## Identity APIs

    def get_users(self):
        #Gets a list of users using the Veracode Identity API        
        request_params = {'page': 0} #initialize the page request
        return self._rest_paged_request("api/authn/v2/users","GET","users",request_params)

    def get_user(self,user_guid):
        #Gets an individual user provided their GUID, using the Veracode Identity API
        uri = "api/authn/v2/users/{}".format(user_guid)
        return self._rest_request(uri,"GET")

    def get_creds (self):
        return self._rest_request("api/authn/v2/api_credentials","GET")

    def update_user (self,user_guid,roles):
        request_params = {'partial':'TRUE',"incremental": 'TRUE'}
        uri = "api/authn/v2/users/{}".format(user_guid)
        return self._rest_request(uri,"PUT",request_params,roles)       