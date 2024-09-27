#collections.py - API class for Collections API calls

import json
from urllib import parse
from typing import List
from uuid import UUID
from requests import RequestException

from .apihelper import APIHelper
from .constants import Constants
from .exceptions import VeracodeAPIError, VeracodeError

ROOT_URL = 'dae/api/tcs-api/api/v1'

class DASTTargets():
   base_url = ROOT_URL + '/targets'

   def get_all(self):
      return APIHelper()._rest_paged_request(self.base_url, 'GET', element='targets',params={})
   
   def get(self, target_id: UUID):
      uri = self.base_url + '/{}'.format(target_id)
      return APIHelper()._rest_request(uri, 'GET')
   
   def get_by_name(self, target_name):
      return self.search(target_name=target_name)
   
   def search(self, target_name=None, url=None, search_term=None, target_type=None):
      # do null checks and construct the parameters
      params = {}

      if target_name != None:
         params['name'] = target_name

      if url != None:
         params['url'] = url

      if search_term != None:
         params['search_term'] = search_term

      if target_type != None:
         if target_type not in Constants().DAST_TARGET_TYPE:
            raise ValueError("{} is not in the list of valid target types ({})".format(target_type,Constants().DAST_TARGET_TYPE))
         params['target_type'] = target_type

      if params == {}:
         return {}

      return APIHelper()._rest_paged_request(self.base_url, 'GET', element='targets',params=params)
   
   def create(self, name, description, protocol, url='', api_specification_file_url='', target_type='WEB_APP',
              scan_type='QUICK',is_sec_lead_only=False,teams=[]):
      
      return self._create_or_update(method='CREATE', name=name, description=description,
                                    protocol=protocol,url=url,
                                    api_specification_file_url=api_specification_file_url,
                                    target_type=target_type,scan_type=scan_type,
                                    is_sec_lead_only=is_sec_lead_only,teams=teams)

   def update(self, target_id, name, description, protocol, url, api_specification_file_url, target_type='WEB_APP',
              scan_type='QUICK',is_sec_lead_only=False,teams=[]):
      
      return self._create_or_update(method='UPDATE', name=name, description=description,
                                    protocol=protocol,url=url,
                                    api_specification_file_url=api_specification_file_url,
                                    target_type=target_type,scan_type=scan_type,
                                    is_sec_lead_only=is_sec_lead_only,teams=teams, target_id=target_id)
   
   def delete(self, target_id: UUID):
      uri = self.base_url + '/{}'.format(target_id)
      return APIHelper()._rest_request(uri, 'DELETE')
   
   def _create_or_update(self, method, name, description, protocol, url, api_specification_file_url, target_type='WEB_APP',
              scan_type='QUICK',is_sec_lead_only=False,teams=[], target_id: UUID=None):
      
      if protocol not in Constants().DAST_PROTOCOL:
            raise ValueError("{} is not in the list of valid protocols ({})".format(protocol,Constants().DAST_PROTOCOL))

      if target_type not in Constants().DAST_TARGET_TYPE:
            raise ValueError("{} is not in the list of valid target types ({})".format(target_type,Constants().DAST_TARGET_TYPE))

      if scan_type not in Constants().DAST_SCAN_TYPE:
            raise ValueError("{} is not in the list of valid scan types ({})".format(scan_type,Constants().DAST_SCAN_TYPE))

      body = { 'name': name, 'description': description, 'protocol': protocol, 'url': url,
              'api_specification_file_url': api_specification_file_url, 'target_type': target_type,
              'scan_type': scan_type, 'is_sec_lead_only': is_sec_lead_only, 'teams': teams}

      if method == "CREATE":
         httpmethod = 'POST'
      elif method == "UPDATE":
         httpmethod = 'PUT'
         body['target_id'] = target_id
      else:
         return

      payload = json.dumps(body)

      return APIHelper()._rest_request(self.base_url,httpmethod,body=payload)

class DASTAnalysisProfiles():
   base_url = ROOT_URL + '/analysis_profiles'
   
   def get_all(self, target_id: UUID=None, type=None):
      params = {}

      if type != None:
         if type not in ['TARGET','SYSTEM']:
            raise ValueError("{} is not in the list of valid types ({})".format(type,['TARGET','SYSTEM']))
         params['type'] = type

      if target_id != None:
         params['target_id'] = target_id

      return APIHelper()._rest_paged_request(self.base_url,"GET",'analysis_profiles',params=params)

   def get(self,analysis_profile_id: UUID):
      uri = '{}/{}'.format(self.base_url,analysis_profile_id)
      return APIHelper()._rest_request(uri,"GET")
   
   def update(self, analysis_profile_id: UUID, allowed_urls=[],denied_urls=[],seed_urls=[],
            grouped_urls=[],crawler_mode=None,rate_limit=None,max_duration=None,
            max_crawl_duration=None):
      uri = '{}/{}'.format(self.base_url,analysis_profile_id)
      body = {}

      if len(allowed_urls) > 0:
         body['allowed_urls'] = allowed_urls

      if len(denied_urls) > 0:
         body['denied_urls'] = denied_urls

      if len(seed_urls) > 0:
         body['seed_urls'] = seed_urls

      if len(grouped_urls) > 0:
         body['grouped_urls'] = grouped_urls

      if crawler_mode != None:
         if crawler_mode not in Constants().DAST_CRAWLER_MODE:
            raise ValueError("{} is not in the list of valid crawler modes ({})".format(crawler_mode,Constants().DAST_CRAWLER_MODE))

         body['crawler_mode'] = crawler_mode

      if rate_limit != None:
         body['rate_limit'] = rate_limit

      if max_duration != None:
         body['max_duration'] = max_duration   

      if max_crawl_duration != None:
         body['max_crawl_duration'] = max_crawl_duration  

      payload = json.dumps(body)
      return APIHelper()._rest_request(uri,'PUT',body=payload)
   
   def update_parent (self, analysis_profile_id: UUID, parent_analysis_profile_id: UUID):
      uri = '{}/{}'.format(self.base_url,analysis_profile_id)
      body = { 'parent_analysis_profile_id': parent_analysis_profile_id }
      payload = json.dumps(body)

      return APIHelper()._rest_request(uri,"PUT",body=payload)

   def get_authentications ( self, analysis_profile_id: UUID):
      self.authentications = self.Authentications(analysis_profile_id=analysis_profile_id, 
                                                  base_url=self.base_url)
      return self.authentications.get()
   
   def update_system_auth ( self, analysis_profile_id: UUID, username, password):
      self.authentications = self.Authentications(analysis_profile_id=analysis_profile_id, 
                                                  base_url=self.base_url)
      return self.authentications.update_system_auth(username=username,password=password)

   def update_app_auth ( self, analysis_profile_id: UUID, username, password, login_url):
      self.authentications = self.Authentications(analysis_profile_id=analysis_profile_id, 
                                                  base_url=self.base_url)
      return self.authentications.update_app_auth(username=username,password=password,login_url=login_url)

   def update_parameter_auth ( self, analysis_profile_id: UUID, id, title, type, key, value):
      self.authentications = self.Authentications(analysis_profile_id=analysis_profile_id, 
                                                  base_url=self.base_url)
      return self.authentications.update_parameter_auth(id=id, title=title, type=type, 
                                                        key=key, value=value)

   def get_scanners(self, analysis_profile_id: UUID):
      self.scanners = self.Scanners(analysis_profile_id=analysis_profile_id, base_url=self.base_url)
      return self.scanners.get()
   
   def update_scanners(self, analysis_profile_id: UUID, scanner_id, scanner_value=True):
      self.scanners = self.Scanners(analysis_profile_id=analysis_profile_id, base_url=self.base_url)
      return self.scanners.update(scanner_id=scanner_id, scanner_value=scanner_value)
   
   def get_schedules(self, analysis_profile_id: UUID):
      self.schedules = self.Schedules(analysis_profile_id=analysis_profile_id, base_url=self.base_url)
      return self.schedules.get_all()
   
   def get_schedule(self, analysis_profile_id: UUID, schedule_id: UUID):
      self.schedules = self.Schedules(analysis_profile_id=analysis_profile_id, base_url=self.base_url)
      return self.schedules.get(schedule_id=schedule_id)
   
   def create_schedule(self,analysis_profile_id: UUID, frequency,day=1,weekday=1,timezone='America/New York',time="00:00"):
      self.schedules = self.Schedules(analysis_profile_id=analysis_profile_id, base_url=self.base_url)
      return self.schedules.create(frequency=frequency, day=day, weekday=weekday, timezone=timezone, time=time)
   
   def update_schedule(self, schedule_id: UUID, analysis_profile_id: UUID, frequency,day=1,weekday=1,timezone='America/New York',time="00:00"):
      self.schedules = self.Schedules(analysis_profile_id=analysis_profile_id, base_url=self.base_url)
      return self.schedules.update(schedule_id=schedule_id, frequency=frequency, day=day, 
                                   weekday=weekday, timezone=timezone, time=time)
   
   def delete_schedule(self, analysis_profile_id: UUID, schedule_id: UUID):
      self.schedules = self.Schedules(analysis_profile_id=analysis_profile_id, base_url=self.base_url)
      return self.schedules.delete(schedule_id=schedule_id)
   
   class Authentications():
      def __init__(self, analysis_profile_id: UUID, base_url):
         self.analysis_profile_id = analysis_profile_id
         self.base_url = '{}/{}'.format(base_url,self.analysis_profile_id)

      def get(self):
         uri = '{}/authentications'.format(self.base_url)
         return APIHelper()._rest_request(uri,"GET")
      
      def update_system_auth(self, username, password):
         uri = '{}/system_authentication'.format(self.base_url)
         body = { 'username': username, 'password': password }
         payload = json.dumps(body)

         return APIHelper()._rest_request(uri,"PUT",body=payload)
      
      def update_app_auth(self, username, password, login_url):
         uri = '{}/application_authentication'.format(self.base_url)
         body = { 'login_url': login_url, 'username': username, 'password': password }
         payload = json.dumps(body)

         return APIHelper()._rest_request(uri,"PUT",body=payload)

      def update_parameter_auth(self, id, title, type, key, value):
         uri = '{}/parameter_authentication'.format(self.base_url)
         body = { id: id, title: title, type: type, key: key, value: value }
         payload = json.dumps(body)

         return APIHelper()._rest_request(uri,"PUT",body=payload)         

   class Scanners():
      def __init__(self, analysis_profile_id: UUID, base_url):
         self.analysis_profile_id = analysis_profile_id
         self.base_url = '{}/{}/scanners'.format(base_url,self.analysis_profile_id)

      def get(self):
         return APIHelper()._rest_request(self.base_url,"GET")
      
      def update(self, scanner_id, scanner_value=True):
         if scanner_id not in Constants().DAST_SCANNERS:
            raise ValueError("{} is not in the list of valid scanners ({})".format(scanner_id,Constants().DAST_SCANNERS))

         body = { 'id': scanner_id, 'value': scanner_value}
         payload = json.dumps(body)
         return APIHelper()._rest_request(self.base_url,"PUT",body=payload)

   class Schedules():
      def __init__(self, analysis_profile_id: UUID, base_url):
         self.analysis_profile_id = analysis_profile_id
         self.base_url = '{}/{}/schedules'.format(base_url,self.analysis_profile_id)

      def get_all(self):
         return APIHelper()._rest_request(self.base_url,"GET")
      
      def get(self,schedule_id:UUID):
         uri = '{}/{}'.format(self.base_url,schedule_id)
         return APIHelper()._rest_request(uri,"GET")
      
      def create(self,frequency,day=1,weekday=1,timezone='America/New York',time="00:00"):
         return self._create_or_update("CREATE",frequency=frequency,day=day,weekday=weekday,
                                       timezone=timezone,time=time)
      
      def update(self, schedule_id: UUID, frequency,day=1,weekday=1,timezone='America/New York',time="00:00"):
         return self._create_or_update("UPDATE",frequency=frequency,day=day,weekday=weekday,
                                       timezone=timezone,time=time,schedule_id=schedule_id)
      
      def delete(self, schedule_id: UUID):
         uri = '{}/{}'.format(self.base_url,schedule_id)
         return APIHelper()._rest_request(uri, "DELETE")

      def _create_or_update(self,method,frequency,day=1,weekday=1,timezone='America/New York',
                            time="00:00",schedule_id: UUID=None):
         if method=='CREATE':
            httpmethod = "POST"
            uri = self.base_url
         elif method=='UPDATE':
            httpmethod = "PUT"
            uri = '{}/{}'.format(self.base_url,schedule_id)
         else:
            return

         body = { 'frequency': frequency, 'day': day, 'weekday': weekday, 'timezone': timezone, 'time': time }
         payload = json.dumps(body)
         return APIHelper()._rest_request(uri, httpmethod, body = payload)         

class DASTAnalysisRuns():
   base_url = ROOT_URL + '/analysis_run'

   def start(self, target_id: UUID):
      body = {'id': target_id}
      payload = json.dumps(body)
      return APIHelper()._rest_request(self.base_url,"POST",body=payload)

   def get(self, target_id: UUID):
      # this returns a PDF report when called. Save the report as a file
      uri = '{}/report/{}'.format(self.base_url,target_id)
      report = APIHelper()._rest_request(uri,"GET",fullresponse=True)
      return report
