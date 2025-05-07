#analytics.py - API class for Analytics Reporting API calls

import json
from uuid import UUID

from .apihelper import APIHelper

class Analytics():
   report_types = [ "findings", "scans", "deletedscans", "audit" ]

   findings_scan_types = ["Static Analysis", "Dynamic Analysis", "Manual", "SCA", "Software Composition Analysis" ]
   scan_scan_types = ["Static Analysis", "Dynamic Analysis", "Manual" ]

   base_url = 'appsec/v1/analytics/report'

   #public methods
   def create_report(self,report_type,last_updated_start_date=None,last_updated_end_date=None,
                     scan_type:list = [], finding_status=None,passed_policy=None,
                     policy_sandbox=None,application_id=None,rawjson=False, deletion_start_date=None,
                     deletion_end_date=None, sandbox_ids:list = [], start_date=None, end_date=None,
                     audit_action:list = [], target_user_id:int = None, modifier_user_id:int = None):

      if report_type not in self.report_types:
         raise ValueError("{} is not in the list of valid report types ({})".format(report_type,self.report_types))

      report_def = { 'report_type': report_type }

      if report_type in ['audit']:
         if start_date:
            report_def['start_date'] = start_date
         else:
            raise ValueError("{} report type requires a start date.").format(report_type)
         
         if end_date:
            report_def['end_date'] = end_date

      if report_type in ['findings','scans']:
         if last_updated_start_date:
            report_def['last_updated_start_date'] = last_updated_start_date
         else:
            raise ValueError("{} report type requires a last updated start date.").format(report_type)

         if last_updated_end_date:
            report_def['last_updated_end_date'] = last_updated_end_date

      if report_type == 'deletedscans':   
         if deletion_start_date:
            report_def['deletion_start_date'] = deletion_start_date
         else:
            raise ValueError("{} report type requires a deletion start date.").format(report_type)

         if deletion_end_date:
            report_def['deletion_end_date'] = deletion_end_date

#  clean this part up, make it object oriented, probably switch report creation by report type and create sub methods

      if len(scan_type) > 0:
         if report_type == 'findings':
            valid_scan_types = self.findings_scan_types
         elif report_type in [ 'scans', 'deletedscans' ]:
            valid_scan_types = self.scan_scan_types
         if not(self._case_insensitive_list_compare(scan_type,valid_scan_types)):
            raise ValueError("{} is not in the list of valid scan types ({})".format(scan_type,valid_scan_types))
         report_def['scan_type'] = scan_type

      if finding_status:
         report_def['finding_status'] = finding_status

      if passed_policy:
         report_def['passed_policy'] = passed_policy

      if policy_sandbox:
         report_def['policy_sandbox'] = policy_sandbox

      if application_id:
         report_def['application_id'] = application_id

      if sandbox_ids:
         report_def['sandbox_ids'] = sandbox_ids

      if len(audit_action) > 0:
         report_def['audit_action'] = audit_action

      if target_user_id:
         report_def['target_user_id'] = target_user_id

      if modifier_user_id:
         report_def['modifier_user_id'] = modifier_user_id
      
      payload = json.dumps(report_def)
      response = APIHelper()._rest_request(url=self.base_url,method="POST",body=payload)

      if rawjson:
         return response
      else:
         return response['_embedded']['id'] #we will usually just need the guid so we can come back and fetch the report

   def create_findings_report(self, start_date, end_date=None,
                     scan_type:list = [], finding_status=None, passed_policy=None,
                     policy_sandbox=None, application_id=None,rawjson=False):
      return self.create_report(report_type='findings', last_updated_start_date=start_date,
                                last_updated_end_date=end_date,scan_type=scan_type,
                                finding_status=finding_status, passed_policy=passed_policy,
                                policy_sandbox=policy_sandbox, application_id=application_id,rawjson=rawjson) 

   def create_scans_report(self, start_date, end_date=None, scan_type:list = [], 
                           policy_sandbox=None, application_id=None, rawjson=False):
      return self.create_report(report_type='scans', last_updated_start_date=start_date, 
                                last_updated_end_date=end_date, scan_type=scan_type,
                                policy_sandbox=policy_sandbox, application_id=application_id,rawjson=rawjson)

   def create_deleted_scans_report(self, start_date, end_date=None, application_id=None,
                                   rawjson=False):
      return self.create_report(report_type='deleted_scans', deletion_start_date=start_date, 
                                deletion_end_date=end_date, application_id=application_id,
                                rawjson=rawjson)
   
   def create_audit_report(self, start_date, end_date=None, audit_action:list=[], target_user_id:int=None, 
                           modifier_user_id:int=None):
      return self.create_report(report_type='audit', start_date=start_date, end_date=end_date, audit_action=audit_action,
                                target_user_id=target_user_id, modifier_user_id=modifier_user_id)
      
   def get_findings(self, guid: UUID):
      thestatus, thefindings = self.get(guid=guid,report_type='findings')
      return thestatus, thefindings

   def get_scans(self, guid: UUID):
      thestatus, thescans = self.get(guid=guid,report_type='scans')
      return thestatus, thescans

   def get_deleted_scans(self, guid: UUID):
      thestatus, thescans = self.get(guid=guid,report_type='deletedscans')
      return thestatus, thescans

   def get_audits(self, guid: UUID):
      thestatus, theaudits = self.get(guid=guid, report_type='audit_logs')  
      return thestatus, theaudits 
   
   def get(self,guid: UUID,report_type='findings'):
      # handle multiple scan types
      uri = "{}/{}".format(self.base_url,guid)
      theresponse = APIHelper()._rest_paged_request(uri,"GET",report_type,{},fullresponse=True)
      thestatus = theresponse.get('_embedded',{}).get('status','')
      thebody = theresponse.get('_embedded',{}).get(report_type,{})
      return thestatus, thebody

   #helper methods
   def _case_insensitive_list_compare(self,input_list:list, target_list:list):
      input_set = self._lowercase_set_from_list(input_list)
      target_set = self._lowercase_set_from_list(target_list)
      return target_set.issuperset(input_set)

   def _lowercase_set_from_list(self,thelist:list):
      return set([x.lower() for x in thelist])