#policy.py - API class for Policy API calls

import json
from uuid import UUID

from .apihelper import APIHelper

class Policies():

    def get_all (self):
        return APIHelper()._rest_paged_request("appsec/v1/policies","GET","policy_versions",{"page": 0})
    
    def get (self,guid: UUID):
        uri = "appsec/v1/policies/{}".format(guid)
        return APIHelper()._rest_request(uri,"GET")

    def delete (self,guid: UUID):
        uri = "appsec/v1/policies/{}".format(guid)
        return APIHelper()._rest_request(uri,"DELETE")

    def create (self, name: str, description: str, vendor_policy=False, finding_rules=[], scan_frequency_rules=[], grace_periods=None):
        if grace_periods == None:
            grace_periods = {}
        return self._create_or_update("CREATE",name,description,vendor_policy,finding_rules,scan_frequency_rules,grace_periods)

    def update(self,guid: UUID, name: str, description: str, vendor_policy=False, finding_rules=[], scan_frequency_rules=[], grace_periods=None):
        if grace_periods == None:
            grace_periods = {}
        return self._create_or_update("UPDATE",name,description,vendor_policy,finding_rules,scan_frequency_rules,grace_periods,guid)

    def format_finding_rule(self,rule_type,scan_types=[],rule_value=''):
        finding_rule = {}
        finding_rule['type'] = rule_type
        finding_rule['scan_types'] = scan_types
        finding_rule['value'] = rule_value
        return finding_rule

    def format_scan_frequency_rule(self,scan_type,frequency):
        scan_frequency_rule = {}
        scan_frequency_rule['scan_type'] = scan_type
        scan_frequency_rule['frequency'] = frequency
        return scan_frequency_rule

    def format_grace_periods(self, sev5: int, sev4: int, sev3: int, sev2: int, sev1: int, sev0: int, score: int, sca_blocklist: int):
        grace_periods = {}
        grace_periods["sev5_grace_period"] = sev5
        grace_periods["sev4_grace_period"] = sev4
        grace_periods["sev3_grace_period"] = sev3
        grace_periods["sev2_grace_period"] = sev2
        grace_periods["sev1_grace_period"] = sev1
        grace_periods["sev0_grace_period"] = sev0
        grace_periods["score_grace_period"] = score
        grace_periods["sca_blacklist_grace_period"] = sca_blocklist
        return grace_periods

    def _create_or_update(self, method, name: str, description: str, vendor_policy=False, finding_rules=[], scan_frequency_rules=[], grace_periods=None, guid: UUID=None):
        if grace_periods == None:
            grace_periods = {}
        if method == 'CREATE':
            uri = 'appsec/v1/policies'
            httpmethod = 'POST'
        elif method == 'UPDATE':
            uri = 'appsec/v1/policies/{}'.format(guid)
            httpmethod = 'PUT'
        else:   
            return
        
        policy_def = {"name": name, "description": description, "vendor_policy": vendor_policy}
        policy_def["finding_rules"] = finding_rules
        policy_def["scan_frequency_rules"] = scan_frequency_rules
        policy_def.update(grace_periods)

        return APIHelper()._rest_request(uri,httpmethod,body=json.dumps(policy_def))
