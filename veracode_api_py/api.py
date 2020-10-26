# Purpose:  API utilities
#
# Notes:    API credentials must be enabled on Veracode account and placed in ~/.veracode/credentials like
#
#           [default]
#           veracode_api_key_id = <YOUR_API_KEY_ID>
#           veracode_api_key_secret = <YOUR_API_KEY_SECRET>
#
#           and file permission set appropriately (chmod 600)

from urllib import parse
import time
import requests
import logging
import json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

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
        self.retry_seconds = 120
        self.connect_error_msg = "Connection Error"
        self.sca_base_url = "srcclr/v3/workspaces"

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
            logging.exception(self.connect_error_msg)
            raise VeracodeAPIError(e)

        if not (r.status_code == requests.codes.ok):
            logging.debug("API call returned non-200 HTTP status code: {}".format(r.status_code))

        if not (r.ok):
            logging.debug("Error retrieving data. HTTP status code: {}".format(r.status_code))
            if r.status_code == 401:
                logging.exception("Check that your Veracode API account credentials are correct.")
            else:
                logging.exception("Error [{}]: {} for request {}".
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
        request_params = {}
        return self._rest_paged_request('appsec/v1/applications',"GET", params=request_params, element="applications")

    def get_app (self,guid=None,legacy_id=None):
        """Gets a single applications in the current customer account using the Veracode Application API."""
        if legacy_id == None:
            apps_base_uri = "appsec/v1/applications" + "/{}"
            uri = apps_base_uri.format(guid)
        else:
            apps_base_uri = "appsec/v1/applications?legacy_id={}"
            uri = apps_base_uri.format(legacy_id)

        return self._rest_request(uri,"GET")

    def get_app_by_name (self,appname):
        """Gets a list of applications having a name that matches appname, using the Veracode Applications API."""
        params = {"name": appname}
        return self._rest_paged_request(uri="appsec/v1/applications",method="GET",element="applications",params=params)

    def create_app(self,app_name,business_criticality, business_unit=None, teams=[]):
        app_def = {'name':app_name, 'business_criticality':business_criticality}

        if len(teams) > 0:
            # optionally pass a list of teams to add to the application profile
            team_list = []
            for team in teams:
                team_list.append({'guid': team})
            app_def.update({'teams': team_list})

        if business_unit != None:
            bu = {'business_unit': {'guid': business_unit}}
            app_def.update(bu)

        payload = json.dumps({"profile": app_def})
        return self._rest_request('appsec/v1/applications','POST',body=payload)

    def delete_app (self,guid):
        uri = 'appsec/v1/applications/{}'.format(guid)
        return self._rest_request(uri,"DELETE")

    def get_policy (self,guid):
        policy_base_uri = "appsec/v1/policies/{}"
        uri = policy_base_uri.format(guid)
        return self._rest_request(uri,"GET")

    def get_findings(self,app,scantype='STATIC',annot='TRUE'):
        #Gets a list of  findings for app using the Veracode Findings API
        request_params = {}

        if scantype in ['STATIC', 'DYNAMIC', 'MANUAL','SCA']:
            request_params['scan_type'] = scantype
        #note that scantype='ALL' will result in no scan_type parameter as in API
            
        request_params['include_annot'] = annot
        
        uri = "appsec/v2/applications/{}/findings".format(app)
        return self._rest_paged_request(uri,"GET","findings",request_params)

    ## Identity APIs

    def get_users(self):
        #Gets a list of users using the Veracode Identity API        
        request_params = {'page': 0} #initialize the page request
        return self._rest_paged_request("api/authn/v2/users","GET","users",request_params)

    def get_user_self (self):
        #Gets the user info for the current user, using the Veracode Identity API
        return self._rest_request("api/authn/v2/users/self","GET")

    def get_user(self,user_guid):
        #Gets an individual user provided their GUID, using the Veracode Identity API
        uri = "api/authn/v2/users/{}".format(user_guid)
        return self._rest_request(uri,"GET")

    def get_user_by_name(self,username):
        #Gets all the users who match the provided email address, using the Veracode Identity API
        request_params = {'user_name': username} #initialize the page request
        return self._rest_paged_request("api/authn/v2/users","GET","users",request_params)

    def get_creds (self):
        return self._rest_request("api/authn/v2/api_credentials","GET")

    def create_user (self,email,firstname,lastname,username=None,type="HUMAN",roles=[],teams=[]):
        user_def = { "email_address": email, "first_name": firstname, "last_name": lastname }

        rolelist = []
        if len(roles) > 0:
            for role in roles:
                rolelist.append({"role_name": role})
            user_def.append({"roles":rolelist})

        if type == "API":
            user_def.update({"user_name": username})
            user_def.update({"permissions": [{"permission_name": "apiUser"}]})
            if len(roles) == 0:
               rolelist.append({"role_name": "uploadapi"})
               rolelist.append({"role_name":"apisubmitanyscan"})
        else:
            if len(roles) == 0:
               rolelist.append({"role_name":"submitter"}) 

        teamlist = []
        if len(teams) > 0:
            for team in teams:
                teamlist.append({"team_id": team})
            user_def.update({"teams": teamlist})

        user_def.update({"roles": rolelist})

        payload = json.dumps(user_def)
        return self._rest_request('api/authn/v2/users','POST',body=payload)

    def update_user (self,user_guid,roles):
        request_params = {'partial':'TRUE',"incremental": 'TRUE'}
        uri = "api/authn/v2/users/{}".format(user_guid)
        return self._rest_request(uri,"PUT",request_params,roles)  

    def disable_user (self,user_guid):
        request_params = {'partial':'TRUE'}
        uri = 'api/authn/v2/users/{}'.format(user_guid)
        payload = json.dumps({'active': False})
        return self._rest_request(uri,"PUT",request_params,payload)

    def delete_user (self,user_guid):
        uri = 'api/authn/v2/users/{}'.format(user_guid)
        return self._rest_request(uri,"DELETE")

    def get_teams (self, all_for_org=False):
        #Gets a list of teams using the Veracode Identity API       
        if all_for_org:
            request_params = {'all_for_org': True}
        else:
            request_params = {'page': 0} #initialize the page request
        return self._rest_paged_request("api/authn/v2/teams","GET","teams",request_params)

    def create_team (self, team_name, business_unit=None, members=[]):        
        team_def = {'team_name': team_name}
        
        if len(members) > 0:
            # optionally pass a list of usernames to add as team members
            users = []
            for member in members:
                users.append({'user_name': member})
            team_def.update({'users': users})

        if business_unit != None:
            bu = {'bu_id': business_unit}
            team_def.update(bu)

        payload = json.dumps(team_def)
        return self._rest_request('api/authn/v2/teams','POST',body=payload)

    def update_team (self, team_guid, team_name="", business_unit=None, members=[]):
        requestbody = {}
        
        if team_name != "":
            requestbody.update({"team_name": team_name})

        if business_unit != None:
            requestbody.update({"business_unit": {"bu_id": business_unit}})

        if len(members) > 0:
            users = []
            for member in members:
                users.append({"user_name": member})
            requestbody.update({"users": users})

        if requestbody == {}:
            logging.error("No update specified for team {}".format(team_guid))

        payload = json.dumps(requestbody)
        params = {"partial":True, "incremental":True}
        uri = 'api/authn/v2/teams/{}'.format(team_guid)
        return self._rest_request(uri,'PUT',body=payload,params=params)

    def delete_team (self, team_guid):
        uri = 'api/authn/v2/teams/{}'.format(team_guid)
        return self._rest_request(uri,"DELETE")
            
    def get_business_units (self):
        request_params = {'page': 0}
        return self._rest_paged_request("api/authn/v2/business_units","GET","business_units",request_params)

## SCA APIs - note must be human user to use these, not API user

    def get_workspaces(self):
        #Gets existing workspaces
        request_params = {}
        return self._rest_paged_request(self.sca_base_url,"GET",params=request_params,element="workspaces")

    def get_workspace_by_name(self,name):
        #Does a name filter on the workspaces list. Note that this is a partial match. Only returns the first match
        name = parse.quote(name) #urlencode any spaces or special characters
        request_params = {'filter[workspace]': name}
        return self._rest_paged_request(self.sca_base_url,"GET",params=request_params,element="workspaces")

    def create_workspace(self,name):
        #pass payload with name, return guid to workspace
        payload = json.dumps({"name": name})
        r = self._rest_request(self.sca_base_url,"POST",body=payload,fullresponse=True)
        loc = r.headers.get('location','')
        return loc.split("/")[-1]

    def add_workspace_team(self,workspace_guid,team_id):
        return self._rest_request(self.sca_base_url + "/{}/teams/{}".format(workspace_guid,team_id),"PUT")

    def delete_workspace(self,workspace_guid):
        return self._rest_request(self.sca_base_url + "/{}".format(workspace_guid),"DELETE") 