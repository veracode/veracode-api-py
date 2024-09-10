#collections.py - API class for Collections API calls

import json
from urllib import parse
from typing import List
from uuid import UUID

from .apihelper import APIHelper

ROOT_URL = 'was/configservice/v1'

class Analyses():
   base_url = ROOT_URL + '/analyses'

   #public methods
   def get_all(self):
      request_params = {}
      return self._get_analyses(request_params)

   def get_by_name(self,analysis_name: str):
      params = {"name": parse.quote(analysis_name)}
      return self._get_analyses(params)

   def get_by_target_url(self,target_url):
      params = {"target_url": target_url}
      return self._get_analyses(params)

   def get_by_search_term(self,search_term: str):
      params = {"search_term": parse.quote(search_term)}
      return self._get_analyses(params)

   def get(self,guid: UUID):
      uri = self.base_url + "/{}".format(guid)
      return APIHelper()._rest_request(uri,"GET")

   def get_audits(self,guid: UUID):
      uri = self.base_url + "/{}/audits".format(guid)
      return APIHelper()._rest_paged_request(uri,"GET",'analysis_audits',{'page':0})

   def create_scan(self,guid: UUID):
      uri = self.base_url + '/{}/scans'.format(guid)
      payload = {} #TODO add code for all the scan values
      return APIHelper()._rest_request(uri,"POST",json.dumps(payload))

   def get_scans(self,guid: UUID):
      uri = self.base_url + "/{}/scans".format(guid)
      return APIHelper()._rest_paged_request(uri,"GET",'scans',{'page': 0})

   def create(self,name: str,scans,start_scan=None,business_unit_guid: UUID=None,email=None,owner: str=None):
      # basic create that adds only metadata. Use Scans().setup() to create a Scans object
      return self._create_or_update(method="CREATE",name=name,scans=scans,
                  business_unit_guid=business_unit_guid,email=email,owner=owner,start_scan=start_scan)

   def update(self,guid: UUID,name: str,scans,start_scan=None,business_unit_guid: UUID=None,email=None,owner: str=None):
      return self._create_or_update(method="UPDATE",name=name,scans=scans,
                  business_unit_guid=business_unit_guid,email=email,owner=owner,guid=guid,start_scan=start_scan)

   def get_scanner_variables(self,guid: UUID):
      uri = self.base_url + "/{}/scanner_variables".format(guid)
      return APIHelper()._rest_paged_request(uri,"GET", 'scanner_variables', {'page': 0})

   def update_scanner_variable(self,analysis_guid: UUID,scanner_variable_guid: UUID,reference_key: str,value: str,description: str):
      uri = self.base_url + '/{}/scanner_variables/{}'.format(analysis_guid,scanner_variable_guid)
      body = { 'reference_key': reference_key, 'value': value, 'description': description }
      return APIHelper()._rest_request(uri,"PUT",body)

   def delete_scanner_variable(self,analysis_guid: UUID,scanner_variable_guid: UUID):
      uri = self.base_url + '/{}/scanner_variables/{}'.format(analysis_guid,scanner_variable_guid)
      return APIHelper()._rest_request(uri,'DELETE')

   def delete(self,guid: UUID):
      uri = self.base_url + "/{}".format(guid)
      return APIHelper()._rest_request(uri,"DELETE")

   #private methods

   def _get_analyses(self,params):
      return APIHelper()._rest_paged_request(self.base_url,"GET","analyses",params=params)

   def _create_or_update(self,method,name: str,scans,start_scan=None,business_unit_guid: UUID=None,email=None,owner: str=None,guid: UUID=None):
      if method == 'CREATE':
         uri = self.base_url
         httpmethod = 'POST'
      elif method == 'UPDATE':
         uri = self.base_url + '/{}'.format(guid)
         httpmethod = 'PUT'
      else:   
         return

      payload = {"name": name, "scans": scans}

      org_info = {}
      if business_unit_guid != None:
         org_info.update({'business_unit_id': business_unit_guid })
      if email != None:
         org_info.update({'email': email})
      if owner != None:
         org_info.update({'owner': owner})
      payload.update({'org_info': org_info})
      if start_scan != None:
         payload.update(start_scan)
      payload.update({"visibility": {"setup_type": "SEC_LEADS_ONLY", "team_identifiers": []}})
      return APIHelper()._rest_request(uri,httpmethod,params={},body=json.dumps(payload))

class Scans():
   base_url = ROOT_URL + '/scans'

   def get(self, guid: UUID):
      uri = self.base_url + "/{}".format(guid)
      return APIHelper()._rest_request(uri,"GET")

   def get_audits(self, guid: UUID):
      uri = self.base_url + "/{}/audits".format(guid)
      return APIHelper()._rest_paged_request(uri,"GET",'scan_audits',{'page':0})

   def get_configuration(self,guid: UUID):
      uri = self.base_url + "/{}/configuration".format(guid)
      return APIHelper()._rest_request(uri,"GET")

   def delete(self,guid: UUID):
      uri = self.base_url + '/{}'.format(guid)
      return APIHelper()._rest_request(uri, 'DELETE')

   def update(self,guid: UUID,scan):
      # use DynUtils().setup_scan() to create the scans parameter
      uri = self.base_url + '/{}'.format(guid)
      return APIHelper()._rest_request(uri,'PUT',body=json.dumps(scan))

   def get_scanner_variables(self,guid: UUID):
      uri = self.base_url + "/{}/scanner_variables".format(guid)
      return APIHelper()._rest_paged_request(uri,"GET",'scanner_variables',{'page': 0})

   def update_scanner_variable(self,scan_guid: UUID,scanner_variable_guid: UUID,reference_key: str,value: str,description: str):
      uri = self.base_url + '/{}/scanner_variables/{}'.format(scan_guid,scanner_variable_guid)
      body = { 'reference_key': reference_key, 'value': value, 'description': description }
      return APIHelper()._rest_request(uri,"PUT",body)

   def delete_scanner_variable(self,scan_guid: UUID,scanner_variable_guid: UUID):
      uri = self.base_url + '/{}/scanner_variables/{}'.format(scan_guid,scanner_variable_guid)
      return APIHelper()._rest_request(uri,'DELETE')   

class Occurrences():
   base_url = ROOT_URL + '/analysis_occurrences'

   def get_all(self):
      return APIHelper()._rest_paged_request(self.base_url,'GET','analysis_occurrences',{'page':0})

   def get(self,guid: UUID):
      uri = self.base_url + '/{}'.format(guid)
      return APIHelper()._rest_request(uri, 'GET')

   def stop(self, guid: UUID, save_or_delete):
      actions = {'SAVE': 'STOP_SAVE', 'DELETE': 'STOP_DELETE'}
      uri = self.base_url + '/{}'.format(guid)
      params = { 'action' : actions[save_or_delete] }
      return APIHelper()._rest_request(uri, 'PUT', json.dumps(params))

   def get_scan_occurrences(self,guid: UUID):
      uri = self.base_url + '/{}/scan_occurrences'.format(guid)
      return APIHelper()._rest_paged_request(uri, 'GET', 'scan_occurrences',{'page':0})

class ScanOccurrences():
   base_url = ROOT_URL + '/scan_occurrences'

   def get(self, guid: UUID):
      uri = self.base_url + '/{}'.format(guid)
      return APIHelper()._rest_request(uri,'GET')

   def stop(self,guid: UUID,save_or_delete):
      actions = {'SAVE': 'STOP_SAVE', 'DELETE': 'STOP_DELETE'}
      uri = self.base_url + '/{}'.format(guid)
      params = { 'action': actions[save_or_delete]}
      return APIHelper()._rest_request(uri,'PUT', json.dumps(params))

   def get_configuration(self,guid: UUID):
      uri = self.base_url + '/{}/configuration'.format(guid)
      return APIHelper()._rest_request(uri,'GET')
   
   def get_verification_report(self,guid: UUID):
      uri = self.base_url + '/{}/verification_report'.format(guid)
      return APIHelper()._rest_request(uri,'GET')

   def get_scan_notes_report(self,guid: UUID):
      uri = self.base_url + '/{}/scan_notes_report'.format(guid)
      return APIHelper()._rest_request(uri,'GET')

   def get_scan_screenshots(self,guid: UUID):
      uri = self.base_url + '/{}/scan_screenshots'.format(guid)
      return APIHelper()._rest_request(uri,'GET')

class CodeGroups():
   base_url = ROOT_URL + '/code_groups'

   def get_all(self):
      return APIHelper()._rest_request(self.base_url,'GET')

   def get(self,name: str):
      uri = self.base_url + '/{}'.format(name)
      return APIHelper()._rest_request(uri,'GET')

class Configuration():
   base_url = ROOT_URL + '/configuration'

   def get(self):
      return APIHelper()._rest_request(self.base_url,'GET')

class ScannerVariables():
   base_url = ROOT_URL + '/scanner_variables'

   def get_all(self):
      return APIHelper()._rest_paged_request(self.base_url,"GET",'scanner_variables',{'page': 0})

   def create(self,reference_key: str,value: str,description: str):
      payload = {'reference_key':reference_key, 'value': value, 'description': description}
      return APIHelper()._rest_request(self.base_url,'POST',body=json.dumps(payload))

   def get(self,guid: UUID):
      uri = self.base_url + '/{}'.format(guid)
      return APIHelper()._rest_request(uri,"GET")

   def update(self,guid: UUID,reference_key: str,value: str,description: str):
      uri = self.base_url + '/{}'.format(guid) + "?method=PATCH"
      body = { 'reference_key': reference_key, 'value': value, 'description': description }
      return APIHelper()._rest_request(uri,"PUT",body=json.dumps(body))

   def delete(self,guid: UUID):
      uri = self.base_url + '/{}'.format(guid)
      return APIHelper()._rest_request(uri,'DELETE')   

class ScanCapacitySummary():

   def get(self):
      return APIHelper()._rest_request(ROOT_URL + '/scan_capacity_summary', 'GET')

class DynUtils():

   def setup_user_agent(self,custom_header: str,type):
      return { "custom_header": custom_header, "type": type}

   def setup_custom_host(self,host_name,ip_address):
      return { 'host_name': host_name, 'ip_address': ip_address}

   def setup_blocklist(self, urls:List):
      return { 'black_list': urls}

   def setup_url(self,url,directory_restriction_type='DIRECTORY_AND_SUBDIRECTORY',http_and_https=True):
      # use to format any URL being made
      return { 'url': url, 'directory_restriction_type': directory_restriction_type, 'http_and_https': http_and_https}

   def setup_scan_setting(self,blocklist_configs:list,custom_hosts:List, user_agent: str=None):
      payload = {}
      
      if len(blocklist_configs) > 0:
         payload.update({'blacklist_configuration': blocklist_configs})

      if len(custom_hosts) > 0:
         payload.update({'custom_hosts': custom_hosts})

      if user_agent != None:
         payload.update({'user_agent':user_agent})

      return { 'scan_setting': payload }

   def setup_scan_contact_info(self,email,first_and_last_name: str,telephone):
      return {'scan_contact_info': {'email': email, 'first_and_last_name': first_and_last_name, 'telephone': telephone}}

   def setup_crawl_script(self,script_body: str,script_type='SELENIUM'):
      return { 'crawl_script_data': { 'script_body': script_body, 'script_type': script_type}}

   def setup_crawl_configuration(self,scripts:List,disabled=False):
      return { 'crawl_configuration': { 'disabled': disabled, 'scripts': scripts}}

   def setup_login_logout_script(self,script_body: str,script_type='SELENIUM'):
      return { 'script_body': script_body, 'script_type': script_type}

   def setup_auth(self,authtype,username: str,password: str,domain=None,base64_pkcs12=None,cert_name: str=None, login_script_data: str=None, logout_script_data: str=None):
      payload = {}
      if authtype == 'AUTO':
         payload.update({'AUTO': {'authtype': authtype, 'username': username, 'password': password}})
      elif authtype == 'BASIC':
         payload.update({'BASIC': {'authtype': authtype, 'username': username, 'password': password, 'domain': domain}})
      elif authtype == 'CERT':
         payload.update({'CERT': {'authtype': authtype, 'password': password, 'base64_pkcs12': base64_pkcs12, 'cert_name': cert_name}})
      elif authtype == 'FORM':
         payload.update({'FORM': {'authtype': authtype, 'login_script_data': login_script_data, 'logout_script_data': logout_script_data}})
      return payload

   def setup_auth_config(self,authentication_node:dict):
      return { 'auth_configuration': { 'authentications': authentication_node}}

   def setup_scan_config_request(self, url, allowed_hosts:List, auth_config=None, crawl_config=None, scan_setting=None):
      payload = {'target_url': url }

      if len(allowed_hosts) > 0:
         payload.update({'allowed_hosts': allowed_hosts})
      if scan_setting != None:
         payload.update(scan_setting)
      if auth_config != None:
         payload.update(auth_config)
      if crawl_config != None:
         payload.update(crawl_config)
      return { 'scan_config_request': payload }

   def setup_scan(self, scan_config_request, scan_contact_info=None, linked_app_guid: UUID=None):
      payload = {}
      payload.update( scan_config_request )
      if scan_contact_info is None:
         scan_contact_info = self.setup_scan_contact_info("", "", "")
         payload.update(scan_contact_info)
      if linked_app_guid != None:
         payload.update({'linked_platform_app_uuid': linked_app_guid})
      return payload
   def start_scan(self, length, unit):
      return { 'schedule': {'now': True, 'duration':{'length': length,'unit': unit }} }
