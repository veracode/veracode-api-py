#findings.py - API class for Findings API and related calls

import json
from uuid import UUID

from .apihelper import APIHelper

LINE_NUMBER_SLOP = 3 #adjust to allow for line number movement  

class Findings():
    
    def get_findings(self,app: UUID,scantype='STATIC',annot='TRUE',request_params=None,sandbox: UUID=None):
        #Gets a list of  findings for app using the Veracode Findings API
        if request_params == None:
            request_params = {}
        
        scantypes = ""
        scantype = scantype.split(',')
        for st in scantype:
            if st in ['STATIC', 'DYNAMIC', 'MANUAL','SCA']:
                if len(scantypes) > 0:
                    scantypes += ","
                scantypes += st
        if len(scantypes) > 0:
            request_params['scan_type'] = scantypes
        #note that scantype='ALL' will result in no scan_type parameter as in API
            
        request_params['include_annot'] = annot

        if sandbox != None:
            request_params['context'] = sandbox
        
        uri = "appsec/v2/applications/{}/findings".format(app)
        return APIHelper()._rest_paged_request(uri,"GET","findings",request_params)

    def get_static_flaw_info(self,app: UUID,issueid: int,sandbox: UUID=None):
        if sandbox != None:
            uri = "appsec/v2/applications/{}/findings/{}/static_flaw_info?context={}".format(app,issueid,sandbox)
        else:
            uri = "appsec/v2/applications/{}/findings/{}/static_flaw_info".format(app,issueid)

        return APIHelper()._rest_request(uri,"GET")

    def get_dynamic_flaw_info(self,app: UUID,issueid: int):
        uri = "appsec/v2/applications/{}/findings/{}/dynamic_flaw_info".format(app,issueid)
        return APIHelper()._rest_request(uri,"GET")

    def add_annotation(self,app: UUID,issue_list,comment: str,action,sandbox: UUID=None):
        #pass issue_list as a list of issue ids
        uri = "appsec/v2/applications/{}/annotations".format(app)

        if sandbox != None:
            params = {'context': sandbox}
        else:
            params = None

        annotation_def = {'comment': comment, 'action': action}

        converted_list = [str(element) for element in issue_list]
        issue_list_string = ','.join(converted_list)
        annotation_def['issue_list'] = issue_list_string 
        
        payload = json.dumps(annotation_def)
        return APIHelper()._rest_request(uri,"POST",body=payload,params=params)

    def match(self,origin_finding,potential_matches,approved_matches_only=True,allow_fuzzy_match=False):
        # match a finding against an array of potential matches
        match = None

        if approved_matches_only:
            potential_matches = self._filter_approved(potential_matches)

        #flatten findings arrays to make processing easier
        scan_type = origin_finding['scan_type']
        of = self._create_match_format_policy(policy_findings=[origin_finding],finding_type=scan_type)
        pm = self._create_match_format_policy(policy_findings=potential_matches,finding_type=scan_type)

        if scan_type == 'STATIC':
            match = self._match_static (of[0], pm, allow_fuzzy_match)
        elif scan_type == 'DYNAMIC':
            match = self._match_dynamic (of[0], pm)
        return match

    def format_file_path(self,file_path):
        # special case - omit prefix for teamcity work directories, which look like this:
        # teamcity/buildagent/work/d2a72efd0db7f7d7

        if file_path is None:
            return ''
            
        suffix_length = len(file_path)

        buildagent_loc = file_path.find('teamcity/buildagent/work/')

        if buildagent_loc > 0:
            #strip everything starting with this prefix plus the 17 characters after
            # (25 characters for find string, 16 character random hash value, plus / )
            formatted_file_path = file_path[(buildagent_loc + 42):suffix_length]
        else:
            formatted_file_path = file_path

        return formatted_file_path

    def _match_static(self,origin_finding,potential_matches,allow_fuzzy_match=False):
        match = None
        if origin_finding['source_file'] not in ('', None):
            #attempt precise match first
            match = next((pf for pf in potential_matches if ((origin_finding['cwe'] == int(pf['cwe'])) & 
                (origin_finding['source_file'].find(pf['source_file']) > -1 ) & 
                (origin_finding['line'] == pf['line'] ))), None)

            if match is None and allow_fuzzy_match:
                #then fall to fuzzy match
                match = next((pf for pf in potential_matches if ((origin_finding['cwe'] == int(pf['cwe'])) & 
                    (origin_finding['source_file'].find(pf['source_file']) > -1 ) & 
                    ((origin_finding['line'] - LINE_NUMBER_SLOP) <= pf['line'] <= (origin_finding['line'] + LINE_NUMBER_SLOP)))), None)

            if match is None:
                #then fall to nondebug as a last resort
                match = self._get_matched_static_finding_nondebug(origin_finding,potential_matches)
        else:
            # if we don't have source file info try matching on procedure and relative location
            match = self._get_matched_static_finding_nondebug(origin_finding,potential_matches)

        return match

    def _get_matched_static_finding_nondebug(self,origin_finding, potential_findings):
        match = None

        match = next((pf for pf in potential_findings if ((origin_finding['cwe'] == int(pf['cwe'])) & 
                    (origin_finding['procedure'].find(pf['procedure']) > -1 ) & 
                    (origin_finding['relative_location'] == pf['relative_location'] ))), None)
        return match

    def _match_dynamic (self, origin_finding, potential_matches):
        match = None

        match = next((pf for pf in potential_matches if ((origin_finding['cwe'] == int(pf['cwe'])) & 
            (origin_finding['path'] == pf['path']) &
            (origin_finding['vulnerable_parameter'] == pf['vulnerable_parameter']))), None)

        return match

    def _filter_approved(self,findings):
        return [f for f in findings if (f['finding_status']['resolution_status'] == 'APPROVED')]

    def _create_match_format_policy(self, policy_findings, finding_type):
        findings = []

        if finding_type == 'STATIC':
            thesefindings = [{'id': pf['issue_id'],
                    'resolution': pf['finding_status']['resolution'],
                    'cwe': pf['finding_details']['cwe']['id'],
                    'procedure': pf['finding_details'].get('procedure'),
                    'relative_location': pf['finding_details'].get('relative_location'),
                    'source_file': self.format_file_path(pf['finding_details'].get('file_path')),
                    'line': pf['finding_details'].get('file_line_number'),
                    'finding': pf} for pf in policy_findings]
            findings.extend(thesefindings)
        elif finding_type == 'DYNAMIC':
            thesefindings = [{'id': pf['issue_id'],
                    'resolution': pf['finding_status']['resolution'],
                    'cwe': pf['finding_details']['cwe']['id'],
                    'path': pf['finding_details']['path'],
                    'vulnerable_parameter': pf['finding_details'].get('vulnerable_parameter',''), # vulnerable_parameter may not be populated for some info leak findings
                    'finding': pf} for pf in policy_findings]
            findings.extend(thesefindings)
        return findings

class SummaryReport():
    def get_summary_report(self,app: UUID,sandbox: UUID=None, build_id: int=None):
        uri = "appsec/v2/applications/{}/summary_report".format(app)
        
        params = {}
        if sandbox != None:
            params['context'] = sandbox

        if build_id != None:
            params['build_id'] = build_id            

        return APIHelper()._rest_request(uri,"GET", params=params)
    
class ManualScans():
    def get_for_app(self,appid: UUID):
        params = {}
        params['application'] = appid
        uri = 'mpt/v1/scans'
        return APIHelper()._rest_paged_request(uri,"GET","scans",params=params)
    
    def get(self,scanid: int):
        uri = "mpt/v1/scans/{}".format(scanid)
        return APIHelper()._rest_request(uri,"GET")
    
    def get_findings(self,scanid: int, include_artifacts=False):
        uri = "mpt/v1/scans/{}/findings".format(scanid)
        params = {}
        params['include_artifacts'] = include_artifacts
        return APIHelper()._rest_paged_request(uri,"GET","findings",params=params)
    
class CWEs():
    base_uri = 'appsec/v1/cwes'
    def get_all(self):
        params = {}
        return APIHelper()._rest_paged_request(self.base_uri,"GET","cwes", params=params)
    
    def get(self,cwe_id: int):
        uri = '{}/{}'.format(self.base_uri, cwe_id)
        return APIHelper()._rest_request(uri,"GET")
    
class CWECategories():
    base_uri = 'appsec/v1/categories'
    def get_all(self):
        params = {}
        return APIHelper()._rest_paged_request(self.base_uri,"GET", "categories", params=params)
    
    def get(self,category_id: int):
        uri = '{}/{}'.format(self.base_uri, category_id)
        return APIHelper()._rest_request(uri,"GET")