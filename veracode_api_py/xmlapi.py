# xmlapi.py - API class for legacy XML API calls

from .apihelper import APIHelper
from .constants import Constants


class XMLAPI():
    baseurl = "https://analysiscenter.veracode.com/api"

    # Upload XML APIs
    def get_app_list(self):
        """Returns all application profiles."""
        return APIHelper()._xml_request(self.baseurl + "/4.0/getapplist.do", "GET")

    def get_app_info(self, app_id: int):
        """Returns application profile info for a given app ID."""
        return APIHelper()._xml_request(self.baseurl + "/5.0/getappinfo.do", "GET", params={"app_id": app_id})

    def get_sandbox_list(self, app_id: int):
        """Returns a list of sandboxes for a given app ID"""
        return APIHelper()._xml_request(self.baseurl + "/5.0/getsandboxlist.do", "GET", params={"app_id": app_id})

    def get_build_list(self, app_id: int, sandbox_id: int = None):
        """Returns all builds for a given app ID."""
        if sandbox_id is None:
            params = {"app_id": app_id}
        else:
            params = {"app_id": app_id, "sandbox_id": sandbox_id}
        return APIHelper()._xml_request(self.baseurl + "/4.0/getbuildlist.do", "GET", params=params)

    def get_build_info(self, app_id: int, build_id: int = None, sandbox_id: int = None):
        """Returns build info for a given build ID."""
        params = {"app_id": app_id}
        if sandbox_id != None:
            params["sandbox_id"] = sandbox_id
        if build_id != None:
            params["build_id"] = build_id
        return APIHelper()._xml_request(self.baseurl + "/5.0/getbuildinfo.do", "GET", params=params)


    def delete_build(self, app_id: int, sandbox_id: int = None):
        """Deletes the last build in an application profile or sandbox."""
        if sandbox_id is None:
            params = {"app_id": app_id}
        else:
            params = {"app_id": app_id, "sandbox_id": sandbox_id}
        return APIHelper()._xml_request(self.baseurl + "/5.0/deletebuild.do", "GET", params=params)


    def upload_file(self, app_id: int, file: str, sandbox_id=None, save_as=None):
        """Uploads a file to an existing build or creates a build."""
        params = {'app_id': app_id}
        if sandbox_id:
            params['sandbox_id'] = sandbox_id
        if save_as:
            params['save_as'] = save_as
        files = {'file': open(file, 'rb')}
        return APIHelper()._xml_request(self.baseurl + "/5.0/uploadfile.do", "POST", params=params, files=files)

    def begin_prescan(self, app_id: int, sandbox_id=None, auto_scan=None,scan_all_nonfatal_top_level_modules=None):
        """Runs a static prescan for an application."""
        params = {'app_id': app_id}
        if sandbox_id:
            params['sandbox_id'] = sandbox_id
        if auto_scan:
            params['auto_scan'] = auto_scan
        if scan_all_nonfatal_top_level_modules:
            params['scan_all_nonfatal_top_level_modules'] = scan_all_nonfatal_top_level_modules
        return APIHelper()._xml_request(self.baseurl + "/5.0/beginprescan.do", "POST", params=params)

    def get_prescan_results(self,app_id: int, build_id=None, sandbox_id=None):
        """Gets the prescan results for an application."""
        params = {'app_id': app_id}
        if build_id:
            params['build_id'] = build_id
        if sandbox_id:
            params['sandbox_id'] = sandbox_id
        return APIHelper()._xml_request(self.baseurl + "/5.0/getprescanresults.do", "GET", params=params)

    def get_file_list(self,app_id: int, build_id=None, sandbox_id=None):
        """Gets the list of uploaded files for an application."""
        params = {'app_id': app_id}
        if build_id:
            params['build_id'] = build_id
        if sandbox_id:
            params['sandbox_id'] = sandbox_id
        return APIHelper()._xml_request(self.baseurl + "/5.0/getfilelist.do", "GET", params=params)

    def remove_file(self,app_id: int, file_id: int, sandbox_id=None):
        """Deletes a file from an existing application scan."""
        params = {'app_id': app_id, 'file_id': file_id}
        if sandbox_id:
            params['sandbox_id'] = sandbox_id
        return APIHelper()._xml_request(self.baseurl + "/5.0/removefile.do", "GET", params=params)

    def begin_scan(self, app_id: int, modules=None, scan_all_top_level_modules=None,scan_selected_modules=None,scan_previously_selected_modules=None,sandbox_id=None):
        """Runs a static scan for an application. Must specify one of: modules, scan_all_top_level_modules, scan_selected_modules, scan_previously_selected_modules"""
        params = {'app_id': app_id}
        if sandbox_id:
            params['sandbox_id'] = sandbox_id
        if modules:
            params['modules'] = modules
        if scan_all_top_level_modules:
            params['scan_all_top_level_modules'] = scan_all_top_level_modules
        if scan_selected_modules:
            params['scan_selected_modules'] = scan_selected_modules
        if scan_previously_selected_modules:
            params['scan_previously_selected_modules'] = scan_previously_selected_modules
        return APIHelper()._xml_request(self.baseurl + "/5.0/beginscan.do", "POST", params=params)


  # Results XML APIs
    def get_detailed_report(self, build_id: int):
        """Returns a detailed report for a given build ID."""
        return APIHelper()._xml_request(self.baseurl + "/5.0/detailedreport.do", "GET", params={"build_id": build_id})

    def generate_archer(self, payload):
        return APIHelper()._xml_request(self.baseurl + "/3.0/generatearcherreport.do", "GET", params=payload)

    def download_archer(self, token=None):
        if token is None:
            payload = None
        else:
            payload = {'token': token}

        return APIHelper()._xml_request(self.baseurl + "/3.0/downloadarcherreport.do", "GET", params=payload)

   # Mitigation and Comments XML APIs
    def set_mitigation_info(self, build_id: int, flaw_id_list, action, comment: str):
        """Adds a new mitigation proposal, acceptance, rejection, or comment for a set of flaws for an application.
        Mitigation action types: ['appdesign','comment','fp','osenv','netenv','library','accepted','rejected','acceptrisk']
        """
        actiontype = Constants.ANNOT_TYPE.get(action, action)
        payload = {'build_id': build_id, 'flaw_id_list': flaw_id_list, 'action': actiontype, 'comment': comment}
        return APIHelper()._xml_request(self.baseurl + "/updatemitigationinfo.do", "POST", params=payload)
