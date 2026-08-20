#custompdf.py - API class for Custom PDF API calls

import json
from uuid import UUID

from .apihelper import APIHelper
from .utilities import Utilities

class CustomPDF():

   scan_types = ["Static", "Dynamic", "Manual", "SCA"]
   findings_severity_levels = ["all", "very_high", "high", "medium", "low", "very_low"]

   base_url = 'report/pdf'

   #public methods
   def create_report(self,app_id:int, scan_types:list = [], executive_summary=True,
                     policy_evaluation=True, findings_impacting_policy=True, findings_severity_level='all', 
                     findings_details=True, flaw_category_details=True, findings_summary=True, 
                     changes_from_last_scan=True, sca_vulnerability_details=True, static_scan_details=True, 
                     dynamic_scan_details=True, penetration_test_summary=True, 
                     proposed_mitigated_findings=True, approved_mitigated_findings=True, 
                     rejected_mitigated_findings=True, sca_standalone=True, veracode_methodology=True,
                     rawjson=False):

      valid_scan_types = self.scan_types
      valid_severities = self.findings_severity_levels
      report_def = { }

      report_def['app_id'] = app_id

      if len(scan_types) > 0: 
         for scan_type in scan_types:
            if not(Utilities().case_insensitive_list_compare(scan_type,valid_scan_types)):
               raise ValueError("{} is not in the list of valid scan types ({})".format(scan_type,valid_scan_types))
            
         report_def['scan_types'] = scan_types

      if not(Utilities().case_insensitive_list_compare([findings_severity_level],valid_severities)):
            raise ValueError("{} is not in the list of valid severities ({})".format(findings_severity_level,valid_severities))

      report_def['findings_severity_level'] = findings_severity_level

      # a long list of boolean switches
      report_def['executive_summary'] = executive_summary
      report_def['policy_evaluation'] = policy_evaluation
      report_def['findings_impacting_policy'] = findings_impacting_policy
      report_def['findings_details'] = findings_details
      report_def['flaw_category_details'] = flaw_category_details
      report_def['flaw_category_details'] = flaw_category_details
      report_def['findings_summary'] = findings_summary
      report_def['changes_from_last_scan'] = changes_from_last_scan
      report_def['sca_vulnerability_details'] = sca_vulnerability_details
      report_def['static_scan_details'] = static_scan_details
      report_def['dynamic_scan_details'] = dynamic_scan_details
      report_def['penetration_test_summary'] = penetration_test_summary
      report_def['proposed_mitigated_findings'] = proposed_mitigated_findings
      report_def['approved_mitigated_findings'] = approved_mitigated_findings
      report_def['rejected_mitigated_findings'] = rejected_mitigated_findings
      report_def['sca_standalone'] = sca_standalone
      report_def['veracode_methodology'] = veracode_methodology
      
      payload = json.dumps(report_def)
      response = APIHelper()._rest_request(url=self.base_url,method="POST",body=payload)

      if rawjson:
         return response
      else:
         return response['request_id'] #we will usually just need the guid so we can come back and fetch the report

   def get(self,guid: UUID):
      # handle multiple scan types
      uri = "{}/{}".format(self.base_url,guid)
      theresponse = APIHelper()._rest_request(uri,"GET",{})
      thestatus = theresponse.get('status','')
      theurl = theresponse.get('downloadUrl',{})
      return thestatus, theurl
