#xmlapi.py - API class for legacy XML API calls

from .apihelper import APIHelper
from .constants import Constants

class XMLAPI():

    baseurl = "https://analysiscenter.veracode.com/api"

    def get_app_list(self):
        """Returns all application profiles."""
        return APIHelper()._xml_request(self.baseurl + "/4.0/getapplist.do", "GET")

    def get_app_info(self, app_id):
        """Returns application profile info for a given app ID."""
        return APIHelper()._xml_request(self.baseurl + "/5.0/getappinfo.do", "GET", params={"app_id": app_id})

    def get_sandbox_list(self, app_id):
        """Returns a list of sandboxes for a given app ID"""
        return APIHelper()._xml_request(self.baseurl + "/5.0/getsandboxlist.do", "GET", params={"app_id": app_id})

    def get_build_list(self, app_id, sandbox_id=None):
        """Returns all builds for a given app ID."""
        if sandbox_id is None:
            params = {"app_id": app_id}
        else:
            params = {"app_id": app_id, "sandbox_id": sandbox_id}
        return APIHelper()._xml_request(self.baseurl + "/4.0/getbuildlist.do", "GET", params=params)
    
    def get_build_info(self, app_id, build_id=None, sandbox_id=None):
        """Returns build info for a given build ID."""
        params = {"app_id": app_id}
        if sandbox_id != None:
            params["sandbox_id"] = sandbox_id
        if build_id != None:
            params["build_id"] = build_id
        return APIHelper()._xml_request(self.baseurl + "/5.0/getbuildinfo.do", "GET", params=params)

    def get_detailed_report(self, build_id):
        """Returns a detailed report for a given build ID."""
        return APIHelper()._xml_request(self.baseurl + "/5.0/detailedreport.do", "GET", params={"build_id": build_id})

    def set_mitigation_info(self,build_id,flaw_id_list,action,comment):
        """Adds a new mitigation proposal, acceptance, rejection, or comment for a set of flaws for an application."""
        actiontype = Constants.ANNOT_TYPE.get(action, 'comment')        
        payload = {'build_id': build_id, 'flaw_id_list': flaw_id_list, 'action': actiontype, 'comment': comment}
        return APIHelper()._xml_request(self.baseurl + "/updatemitigationinfo.do", "POST", params=payload)

    def generate_archer(self,payload):
        return APIHelper()._xml_request(self.baseurl + "/3.0/generatearcherreport.do", "GET",params=payload)

    def download_archer(self, token=None):
        if token==None:
            payload = None
        else:
            payload = {'token': token}

        return APIHelper()._xml_request(self.baseurl + "/3.0/downloadarcherreport.do", "GET", params=payload)