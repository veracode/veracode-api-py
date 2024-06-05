#static.py - API class for Static REST API calls

from .apihelper import APIHelper
from uuid import UUID
from .constants import Constants
import json

class StaticCLI():
     
   class Scans():
      baseuri = 'pipeline_scan/v1/scans'

      def create(self, binary_name: str, binary_size: int, binary_hash, app_id: int=None, 
                 project_name: str=None, project_uri: str=None, project_ref: str=None, 
                 commit_hash=None, dev_stage: str=None, scan_timeout: int=None):

         scan_def = { 'binary_name': binary_name, 'binary_size': binary_size, 'binary_hash': binary_hash }

         if app_id:
            scan_def.update({'app_id':app_id})

         if project_name:
            scan_def.update({'project_name': project_name})

         if project_uri:
            scan_def.update({'project_uri': project_uri})

         if project_ref:
            scan_def.update({'project_ref': project_ref})

         if commit_hash:
            scan_def.update({'commit_hash':commit_hash})

         if dev_stage:
            if dev_stage not in Constants().DEV_STAGE:
               raise ValueError("{} is not in the list of valid development stages: ({})".
                                format(dev_stage,Constants().DEV_STAGE)) 
            else:
               scan_def.update({'dev_stage': dev_stage})

         if scan_timeout:
            if scan_timeout > 60:
               raise ValueError("scan_timeout: {} too large (must be between 0 and 60)".format(scan_timeout))
            else:
               scan_def.update({'scan_timeout': scan_timeout})

         payload = json.dumps(scan_def)

         return APIHelper()._rest_request(self.baseuri,"POST",body=payload) 

      def get(self, scan_id: UUID):
         uri = self.baseuri + '/{}'.format(scan_id)
         return APIHelper()._rest_request(uri,"GET")
      
      def start(self, scan_id: UUID):
         return self()._start_or_cancel(scan_id = scan_id, action='STARTED')
      
      def cancel(self, scan_id: UUID):
         return self()._start_or_cancel(scan_id = scan_id, action='CANCELLED')
      
      def _start_or_cancel(self, scan_id: UUID, action: str):
         uri = self.baseuri + '/{}'.format(scan_id)
         return APIHelper()._rest_request(uri,"PUT",body={'scan_status': action})
      
      class Segments():
         baseuri = 'pipeline_scan/v1/scans/{}/segments/{}'

         def add(self, scan_id: UUID, segment_id: int, segment_file):
            uri = self.baseuri.format(scan_id, segment_id)

            try:
                  files = { 'file': open(segment_file)}
            except IOError:
                  print("Could not read file {}".format(segment_file))
                  return
            return APIHelper()._rest_request(uri,"PUT",params=None,files=files)

      class Findings():
         baseuri = 'pipeline_scan/v1/scans/{}/findings'

         def get(self, scan_id: UUID):
            uri = self.baseuri.format(scan_id)
            return APIHelper()._rest_request(uri,"GET")