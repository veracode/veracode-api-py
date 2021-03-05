#applications.py - API class for Applications API calls

import json
from urllib import parse

from .apihelper import APIHelper

class Applications():    
    def get_all(self):
        return APIHelper()._rest_paged_request('appsec/v1/applications',"GET", params={}, element="applications")

    def get (self,guid=None,legacy_id=None):
        """Gets a single applications in the current customer account using the Veracode Application API."""
        if legacy_id == None:
            apps_base_uri = "appsec/v1/applications" + "/{}"
            uri = apps_base_uri.format(guid)
        else:
            apps_base_uri = "appsec/v1/applications?legacy_id={}"
            uri = apps_base_uri.format(legacy_id)

        return APIHelper()._rest_request(uri,"GET")

    def get_by_name (self,appname):
        """Gets a list of applications having a name that matches appname, using the Veracode Applications API."""
        params = {"name": parse.quote(appname)}
        return APIHelper()._rest_paged_request(uri="appsec/v1/applications",method="GET",element="applications",params=params)

    def create(self,app_name,business_criticality, business_unit=None, teams=[]):
        return self._create_or_update("CREATE",app_name,business_criticality,business_unit,teams)

    def update(self,guid,app_name,business_criticality, business_unit=None, teams=[]):
        return self._create_or_update("UPDATE",app_name,business_criticality,business_unit,teams,guid)

    def delete(self,guid):
        uri = 'appsec/v1/applications/{}'.format(guid)
        return APIHelper()._rest_request(uri,'DELETE')

    def _create_or_update(self,method,app_name,business_criticality, business_unit=None, teams=[],guid=None):
        if method == 'CREATE':
            uri = 'appsec/v1/applications'
            httpmethod = 'POST'
        elif method == 'UPDATE':
            uri = 'appsec/v1/applications/{}'.format(guid)
            httpmethod = 'PUT'
        else:   
            return

        app_def = {'name':app_name, 'business_criticality':business_criticality}

        if len(teams) > 0:
            # optionally pass a list of teams to add to the application profile
            team_list = []
            for team in teams:
                team_list.append({'guid': team})
            app_def.update({'teams': team_list})

        if business_unit != None:
            bu = {'business_unit': {'guid': business_unit}}
            app_def.update(bu)

        payload = json.dumps({"profile": app_def})
        return APIHelper()._rest_request(uri,httpmethod,body=payload)

class Sandboxes ():
    def get_all(self,guid):
        request_params = {}
        uri = 'appsec/v1/applications/{}/sandboxes'.format(guid)
        return APIHelper()._rest_paged_request(uri,'GET','sandboxes',request_params)

    def create(self, app, name, auto_recreate=False, custom_fields=[]):
        uri = 'appsec/v1/applications/{}/sandboxes'.format(app)
        sandbox_def = {'name': name, 'auto_recreate': auto_recreate}

        if len(custom_fields) > 0:
            sandbox_def.update({"custom_fields": custom_fields})

        payload = json.dumps(sandbox_def)
        return APIHelper()._rest_request(uri,'POST',body=payload)

    def update(self, app, sandbox, name, auto_recreate=False, custom_fields=[]):
        uri = 'appsec/v1/applications/{}/sandboxes/{}'.format(app,sandbox)
        sandbox_def = {'name': name, 'auto_recreate': auto_recreate}

        if len(custom_fields) > 0:
            sandbox_def.update({"custom_fields": custom_fields})

        payload = json.dumps(sandbox_def)
        return APIHelper()._rest_request(uri,'PUT',body=payload)

    def delete(self, app, sandbox):
        uri = 'appsec/v1/applications/{}/sandboxes/{}'.format(app,sandbox)
        return APIHelper()._rest_request(uri,'DELETE')

class CustomFields():
    def get_all (self):
        return APIHelper()._rest_request('appsec/v1/custom_fields','GET')
