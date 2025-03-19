#applications.py - API class for Applications API calls

import json
from urllib import parse
from uuid import UUID

from .apihelper import APIHelper
from .constants import Constants

class Applications():    
    def get_all(self,policy_check_after=None):
        if policy_check_after == None:
            params={}
        else:
            params={"policy_compliance_checked_after": policy_check_after}

        return APIHelper()._rest_paged_request('appsec/v1/applications',"GET", params=params, 
                                                element="applications")

    def get (self,guid: UUID=None,legacy_id: int=None):
        """Gets a single applications in the current customer account using the Veracode Application API."""
        if legacy_id == None:
            apps_base_uri = "appsec/v1/applications" + "/{}"
            uri = apps_base_uri.format(guid)
        else:
            apps_base_uri = "appsec/v1/applications?legacy_id={}"
            uri = apps_base_uri.format(legacy_id)

        return APIHelper()._rest_request(uri,"GET")

    def get_by_name (self,appname: str):
        """Gets a list of applications having a name that matches appname, using the Veracode Applications API."""
        params = {"name": parse.quote(appname)}
        return APIHelper()._rest_paged_request(uri="appsec/v1/applications",method="GET",element="applications",params=params)

    def get_by_repo (self,git_repo_url: str):
        """Gets a list of applications having a name that matches appname, using the Veracode Applications API."""
        params = {"git_repo_url": parse.quote(git_repo_url)}
        return APIHelper()._rest_paged_request(uri="appsec/v1/applications",method="GET",element="applications",params=params)
    
    def create(self,app_name:str ,business_criticality, description: str=None, business_unit: UUID=None, teams=[], policy_guid:UUID=None,
                custom_fields=[], bus_owner_name=None, bus_owner_email=None, git_repo_url=None, custom_kms_alias: str=None, tags=None):
        return self._create_or_update("CREATE",app_name=app_name,business_criticality=business_criticality,
                                      description=description,business_unit=business_unit,teams=teams, policy_guid=policy_guid, 
                                      custom_fields=custom_fields, tags=tags, bus_owner_name=bus_owner_name, 
                                      bus_owner_email=bus_owner_email, git_repo_url=git_repo_url, custom_kms_alias=custom_kms_alias)

    def update(self,guid: UUID,app_name:str, business_criticality, description: str=None, business_unit: UUID=None, 
               teams=[], policy_guid:UUID=None, custom_fields=[],
               bus_owner_name=None,bus_owner_email=None, git_repo_url=None, custom_kms_alias: str=None, tags=None):
        return self._create_or_update("UPDATE",app_name=app_name,business_criticality=business_criticality,
                                      description=description,business_unit=business_unit,teams=teams,guid=guid, 
                                      policy_guid=policy_guid, custom_fields=custom_fields, tags=tags, 
                                      bus_owner_name=bus_owner_name,bus_owner_email=bus_owner_email,
                                      git_repo_url=git_repo_url, custom_kms_alias=custom_kms_alias)

    def delete(self,guid: UUID):
        uri = 'appsec/v1/applications/{}'.format(guid)
        return APIHelper()._rest_request(uri,'DELETE')

    def _create_or_update(self,method,app_name: str, business_criticality, description: str=None, business_unit: UUID=None, 
                          teams=[],guid=None,policy_guid:UUID=None, custom_fields=[],
                          bus_owner_name=None,bus_owner_email=None,git_repo_url=None,custom_kms_alias:str=None, tags=None):
        if method == 'CREATE':
            uri = 'appsec/v1/applications'
            httpmethod = 'POST'
        elif method == 'UPDATE':
            uri = 'appsec/v1/applications/{}'.format(guid)
            httpmethod = 'PUT'
        else:   
            return
        
        if business_criticality not in Constants().BUSINESS_CRITICALITY:
            raise ValueError("{} is not in the list of valid business criticalities ({})".format(business_criticality,Constants().BUSINESS_CRITICALITY))
        business_criticality = business_criticality.replace(" ", "_")

        app_def = {'name':app_name, 'business_criticality':business_criticality}

        if (description != None):
            desc = { 'description': description}
            app_def.update(desc)

        if (tags != None):
            app_def.update({ 'tags': tags })

        if policy_guid:
            app_def.update({"policies": [{'guid': policy_guid}]})

        if len(teams) > 0:
            # optionally pass a list of teams to add to the application profile
            team_list = []
            for team in teams:
                team_list.append({'guid': team})
            app_def.update({'teams': team_list})

        if business_unit != None:
            bu = {'business_unit': {'guid': business_unit}}
            app_def.update(bu)

        if (custom_fields != None):
            app_def.update({"custom_fields": custom_fields})

        if (bus_owner_email != None) & (bus_owner_name != None):
            bus_owner = {'business_owners':[ {'email': bus_owner_email, 'name': bus_owner_name } ] }
            app_def.update(bus_owner)

        if (git_repo_url != None):
            gru = { 'git_repo_url': git_repo_url}
            app_def.update(gru)

        if (custom_kms_alias != None):
            app_def.update({"custom_kms_alias": custom_kms_alias})

        payload = json.dumps({"profile": app_def})
        return APIHelper()._rest_request(uri,httpmethod,body=payload)

class Sandboxes ():
    def get_all(self,guid: UUID):
        request_params = {}
        uri = 'appsec/v1/applications/{}/sandboxes'.format(guid)
        return APIHelper()._rest_paged_request(uri,'GET','sandboxes',request_params)

    def create(self, app: UUID, name: str, auto_recreate=False, custom_fields=[]):
        uri = 'appsec/v1/applications/{}/sandboxes'.format(app)
        sandbox_def = {'name': name, 'auto_recreate': auto_recreate}

        if len(custom_fields) > 0:
            sandbox_def.update({"custom_fields": custom_fields})

        payload = json.dumps(sandbox_def)
        return APIHelper()._rest_request(uri,'POST',body=payload)

    def update(self, app: UUID, sandbox: UUID, name: str, auto_recreate=False, custom_fields=[]):
        uri = 'appsec/v1/applications/{}/sandboxes/{}'.format(app,sandbox)
        sandbox_def = {'name': name, 'auto_recreate': auto_recreate}

        if len(custom_fields) > 0:
            sandbox_def.update({"custom_fields": custom_fields})

        payload = json.dumps(sandbox_def)
        return APIHelper()._rest_request(uri,'PUT',body=payload)

    def delete(self, app: UUID, sandbox: UUID):
        uri = 'appsec/v1/applications/{}/sandboxes/{}'.format(app,sandbox)
        return APIHelper()._rest_request(uri,'DELETE')

class CustomFields():
    def get_all (self):
        return APIHelper()._rest_request('appsec/v1/custom_fields','GET')
