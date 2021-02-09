#findings.py - API class for Findings API and related calls

import json

from .apihelper import APIHelper

class Findings():
    def get_findings(self,app,scantype='STATIC',annot='TRUE',request_params=None):
        #Gets a list of  findings for app using the Veracode Findings API
        if request_params == None:
            request_params = {}
        
        if scantype in ['STATIC', 'DYNAMIC', 'MANUAL','SCA']:
            request_params['scan_type'] = scantype
        #note that scantype='ALL' will result in no scan_type parameter as in API
            
        request_params['include_annot'] = annot
        
        uri = "appsec/v2/applications/{}/findings".format(app)
        return APIHelper()._rest_paged_request(uri,"GET","findings",request_params)

    def get_static_flaw_info(self,app,issueid,sandbox=None):
        if sandbox != None:
            uri = "appsec/v2/applications/{}/findings/{}/static_flaw_info?context={}".format(app,issueid,sandbox)
        else:
            uri = "appsec/v2/applications/{}/findings/{}/static_flaw_info".format(app,issueid)

        return APIHelper()._rest_request(uri,"GET")

    def get_dynamic_flaw_info(self,app,issueid):
        uri = "appsec/v2/applications/{}/findings/{}/dynamic_flaw_info".format(app,issueid)
        return APIHelper()._rest_request(uri,"GET")

    def add_annotation(self,app,issue_list,comment,action):
        #pass issue_list as a list of issue ids
        uri = "appsec/v2/applications/{}/annotations".format(app)

        annotation_def = {'comment': comment, 'action': action}

        converted_list = [str(element) for element in issue_list]
        issue_list_string = ','.join(converted_list)
        annotation_def['issue_list'] = issue_list_string 
        
        payload = json.dumps(annotation_def)
        return APIHelper()._rest_request(uri,"POST",body=payload)

class SummaryReport():
    def get_summary_report(self,app,sandbox=None):
        if sandbox != None:
            uri = "appsec/v2/applications/{}/summary_report?context={}".format(app,sandbox)
        else:
            uri = "appsec/v2/applications/{}/summary_report".format(app)

        return APIHelper()._rest_request(uri,"GET")