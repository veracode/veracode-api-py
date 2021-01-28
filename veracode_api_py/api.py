# Purpose:  API utilities
#
# Notes:    API credentials must be enabled on Veracode account and placed in ~/.veracode/credentials like
#
#           [default]
#           veracode_api_key_id = <YOUR_API_KEY_ID>
#           veracode_api_key_secret = <YOUR_API_KEY_SECRET>
#
#           and file permission set appropriately (chmod 600)

import requests
import logging
from requests.adapters import HTTPAdapter

from veracode_api_signing.exceptions import VeracodeAPISigningException
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC

from .constants import Constants
from .exceptions import VeracodeAPIError
from .applications import Applications, Sandboxes, CustomFields
from .findings import Findings, SummaryReport
from .policy import Policies
from .sca import Workspaces
from .collections import Collections
from .identity import Users, Teams, BusinessUnits, APICredentials, Roles
from .healthcheck import Healthcheck
from .xmlapi import XMLAPI

class VeracodeAPI:

    def __init__(self, proxies=None):
        self.baseurl = 'https://analysiscenter.veracode.com/api'
        requests.Session().mount(self.baseurl, HTTPAdapter(max_retries=3))
        self.proxies = proxies
        self.retry_seconds = 120
        self.connect_error_msg = "Connection Error"

    #xml apis

    def get_app_list(self):
        return XMLAPI().get_app_list()

    def get_app_info(self, app_id):
        return XMLAPI().get_app_info(app_id)

    def get_sandbox_list(self, app_id):
        return XMLAPI().get_sandbox_list(app_id)

    def get_build_list(self, app_id, sandbox_id=None):
        return XMLAPI().get_build_list(app_id, sandbox_id)
    
    def get_build_info(self, app_id, build_id=None, sandbox_id=None):
        return XMLAPI().get_build_info(app_id,build_id,sandbox_id)

    def get_detailed_report(self, build_id):
        return XMLAPI().get_detailed_report(build_id)

    def set_mitigation_info(self,build_id,flaw_id_list,action,comment):
        return XMLAPI().set_mitigation_info(build_id,flaw_id_list,action,comment)

    def generate_archer(self,payload):
        return XMLAPI().generate_archer(payload)

    def download_archer(self, token=None):
        return XMLAPI().download_archer(token)

    # rest apis

    ## Application and Sandbox APIs

    def healthcheck(self):
        return Healthcheck().healthcheck()

    def get_apps(self):
        return Applications().get_all()

    def get_app (self,guid=None,legacy_id=None):
        return Applications().get(guid,legacy_id)

    def get_app_by_name (self,appname):
        return Applications().get_by_name(appname)

    def create_app(self,app_name,business_criticality, business_unit=None, teams=[]):
        return Applications().create(app_name,business_criticality,business_unit,teams)

    def delete_app (self,guid):
        return Applications().delete(guid)

    def get_custom_fields (self):
        return CustomFields().get_all()

    def get_app_sandboxes (self,guid):
        return Sandboxes().get_all(guid)

    def create_sandbox (self, app, name, auto_recreate=False, custom_fields=[]):
        return Sandboxes().create(app,name,auto_recreate,custom_fields)

    def update_sandbox (self, app, sandbox, name, auto_recreate=False, custom_fields=[]):
        return Sandboxes().update(app,sandbox,name,auto_recreate,custom_fields)

    def delete_sandbox (self, app, sandbox):
        return Sandboxes().delete(app,sandbox)

    # Policy APIs

    def get_policies (self):
        return Policies().get_all()

    def get_policy (self,guid):
        return Policies().get(guid)

    def create_policy(self, name, description, vendor_policy=False, finding_rules=[], scan_frequency_rules=[], grace_periods={}):
        return Policies().create(name, description, vendor_policy, finding_rules, scan_frequency_rules, grace_periods)

    def delete_policy (self,guid):
        return Policies().delete(guid)

    def update_policy(self, guid, name, description, vendor_policy=False, finding_rules=[], scan_frequency_rules=[], grace_periods={}):
        return Policies().update(guid, name, description, vendor_policy, finding_rules, scan_frequency_rules, grace_periods)

    # Findings and Reporting APIs

    def get_findings(self,app,scantype='STATIC',annot='TRUE',request_params=None):
        return Findings().get_findings(app,scantype,annot,request_params)

    def get_static_flaw_info(self,app,issueid,sandbox=None):
        return Findings().get_static_flaw_info(app,issueid,sandbox)

    def get_dynamic_flaw_info(self,app,issueid):
        return Findings().get_dynamic_flaw_info(app,issueid)

    def get_summary_report(self,app,sandbox=None):
        return SummaryReport().get_summary_report(app,sandbox)

    def add_annotation(self,app,issue_list,comment,action):
        return Findings().add_annotation(app,issue_list,comment,action)

    ## Collections APIs

    def get_collections(self):
        return Collections().get_all()

    def get_collections_by_name(self,collection_name):
        return Collections().get_by_name(collection_name)

    def get_collections_by_business_unit(self,business_unit_name):
        return Collections().get_by_business_unit(business_unit_name)

    def get_collections_statistics(self):
        return Collections().get_statistics()

    def get_collection(self,guid):
        return Collections().get(guid)

    def get_collection_assets(self,guid):
        return Collections().get_assets(guid)

    def create_collection(self,name,description="",tags='',business_unit_guid=None,custom_fields=[],assets=[]):
        return Collections().create(name,description,tags,business_unit_guid,custom_fields,assets)

    def update_collection(self,guid,name,description="",tags="",business_unit_guid=None,custom_fields=[],assets=[]):
        return Collections().update(name,description,tags,business_unit_guid,custom_fields,assets)

    def delete_collection(self,guid):
        return Collections().delete(guid)

    ## Identity APIs

    def get_users(self):
        return Users().get_all()

    def get_user_self (self):
        return Users().get_self()

    def get_user(self,user_guid):
        return Users().get(user_guid)

    def get_user_by_name(self,username):
        return Users().get_by_name(username)

    def create_user (self,email,firstname,lastname,username=None,type="HUMAN",roles=[],teams=[]):
        return Users().create(email,firstname,lastname,username,type,roles,teams)

    def update_user (self,user_guid,roles):
        return Users().update(user_guid,roles)

    def disable_user (self,user_guid):
        return Users().disable(user_guid)

    def delete_user (self,user_guid):
        return Users().delete(user_guid)

    def get_teams (self, all_for_org=False):
        return Teams().get_all()

    def create_team (self, team_name, business_unit=None, members=[]):        
        return Teams().create(team_name,business_unit,members)

    def update_team (self, team_guid, team_name="", business_unit=None, members=[]):
        return Teams().update(team_guid,team_name,business_unit,members)

    def delete_team (self, team_guid):
        return Teams().delete(team_guid)
            
    def get_business_units (self):
        return BusinessUnits().get_all()

    def get_business_unit (self, guid):
        return BusinessUnits().get(guid)

    def create_business_unit (self, name, teams=[]):
        return BusinessUnits().create(name,teams)

    def update_business_unit (self, guid, name='', teams=[]):
        return BusinessUnits().update(guid,name,teams)

    def delete_business_unit (self, guid):
        return BusinessUnits().delete(guid)

    def get_creds (self,api_id=None):
        if api_id != None:
            return APICredentials().get(api_id)
        else:
            return APICredentials().get_self()

    def renew_creds (self):
        return APICredentials().renew()

    def revoke_creds (self, api_id):
        return APICredentials().revoke(api_id)

    def get_roles (self):
        return Roles().get_all()

## SCA APIs - note must be human user to use these, not API user

    def get_workspaces(self):
        return Workspaces().get_all()

    def get_workspace_by_name(self,name):
        return Workspaces().get_by_name(name)

    def create_workspace(self,name):
        return Workspaces().create(name)

    def add_workspace_team(self,workspace_guid,team_id):
        return Workspaces().add_team(workspace_guid,team_id)

    def delete_workspace(self,workspace_guid):
        return Workspaces().delete(workspace_guid)

    def get_projects(self,workspace_guid):
        return Workspaces().get_projects(workspace_guid)

    def get_project(self,workspace_guid,project_guid):
        return Workspaces().get_project(workspace_guid,project_guid)

    def get_agents(self,workspace_guid):
        return Workspaces().get_agents(workspace_guid)

    def get_agent(self,workspace_guid,agent_guid):
        return Workspaces().get_agent(workspace_guid,agent_guid)

    def create_agent(self,workspace_guid,name,agent_type='CLI'):
        return Workspaces().create_agent(workspace_guid,name,agent_type)

    def get_agent_tokens(self,workspace_guid,agent_guid):
        return Workspaces().get_agent_tokens(workspace_guid,agent_guid)

    def get_agent_token(self,workspace_guid,agent_guid,token_id):
        return Workspaces().get_agent_token(workspace_guid,agent_guid,token_id)
        
    def regenerate_agent_token(self,workspace_guid,agent_guid):
        return Workspaces().regenerate_agent_token(workspace_guid,agent_guid)

    def revoke_agent_token(self,workspace_guid,agent_guid,token_id):
        return Workspaces().revoke_agent_token(workspace_guid,agent_guid,token_id)

    def get_issues(self,workspace_guid):
        return Workspaces().get_issues(workspace_guid)

    def get_issue(self,issue_id):
        return Workspaces().get_issues(issue_id)

    def get_libraries(self,workspace_guid,unmatched=False):
        return Workspaces().get_libraries(workspace_guid, unmatched)

    def get_library(self,library_id):
        return Workspaces().get_library(library_id)

    def get_vulnerability(self,vulnerability_id):
        return Workspaces().get_vulnerability(vulnerability_id)

    def get_license(self,license_id):
        return Workspaces().get_license(license_id)

    def get_sca_events(self,date_gte=None,event_group=None,event_type=None):
        return Workspaces().get_events(date_gte,event_group,event_type)

    def get_sca_scan(self,scan_id):
        return Workspaces().get_scan(scan_id)
    