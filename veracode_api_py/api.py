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
from typing import List
from uuid import UUID

from veracode_api_signing.exceptions import VeracodeAPISigningException
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC

from .constants import Constants
from .exceptions import VeracodeAPIError
from .applications import Applications, Sandboxes, CustomFields
from .findings import Findings, SummaryReport
from .policy import Policies
from .sca import ComponentActivity, Workspaces, SBOM
from .collections import Collections
from .identity import Users, Teams, BusinessUnits, APICredentials, Roles
from .healthcheck import Healthcheck
from .dynamic import Analyses, Scans, Occurrences, Configuration, CodeGroups, ScanCapacitySummary, ScanOccurrences, ScannerVariables, DynUtils
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

    ## Healthcheck APIs

    def healthcheck(self):
        return Healthcheck().healthcheck()

    def status(self):
        return Healthcheck().status()

    ## Application and Sandbox APIs

    def get_apps(self):
        return Applications().get_all()

    def get_app (self,guid: UUID=None,legacy_id=None):
        return Applications().get(guid,legacy_id)

    def get_app_by_name (self,appname):
        return Applications().get_by_name(appname)

    def create_app(self,app_name,business_criticality, business_unit: UUID=None, teams=[]):
        return Applications().create(app_name,business_criticality,business_unit,teams)

    def delete_app (self,guid: UUID):
        return Applications().delete(guid)

    def get_custom_fields (self):
        return CustomFields().get_all()

    def get_app_sandboxes (self,guid: UUID):
        return Sandboxes().get_all(guid)

    def create_sandbox (self, app: UUID, name, auto_recreate=False, custom_fields=[]):
        return Sandboxes().create(app,name,auto_recreate,custom_fields)

    def update_sandbox (self, app: UUID, sandbox: UUID, name, auto_recreate=False, custom_fields=[]):
        return Sandboxes().update(app,sandbox,name,auto_recreate,custom_fields)

    def delete_sandbox (self, app: UUID, sandbox: UUID):
        return Sandboxes().delete(app,sandbox)

    # Policy APIs

    def get_policies (self):
        return Policies().get_all()

    def get_policy (self,guid: UUID):
        return Policies().get(guid)

    def create_policy(self, name, description, vendor_policy=False, finding_rules=[], scan_frequency_rules=[], grace_periods={}):
        return Policies().create(name, description, vendor_policy, finding_rules, scan_frequency_rules, grace_periods)

    def delete_policy (self,guid: UUID):
        return Policies().delete(guid)

    def update_policy(self, guid: UUID, name, description, vendor_policy=False, finding_rules=[], scan_frequency_rules=[], grace_periods={}):
        return Policies().update(guid, name, description, vendor_policy, finding_rules, scan_frequency_rules, grace_periods)

    # Findings and Reporting APIs

    def get_findings(self,app: UUID,scantype='STATIC',annot='TRUE',request_params=None,sandbox: UUID=None):
        return Findings().get_findings(app,scantype,annot,request_params,sandbox)

    def get_static_flaw_info(self,app: UUID,issueid,sandbox: UUID=None):
        return Findings().get_static_flaw_info(app,issueid,sandbox)

    def get_dynamic_flaw_info(self,app: UUID,issueid):
        return Findings().get_dynamic_flaw_info(app,issueid)

    def get_summary_report(self,app: UUID,sandbox=None):
        return SummaryReport().get_summary_report(app,sandbox)

    def add_annotation(self,app: UUID,issue_list,comment,action,sandbox: UUID=None):
        return Findings().add_annotation(app,issue_list,comment,action,sandbox)

    def match_findings(self,origin_finding,potential_matches,approved_findings_only=True):
        return Findings().match(origin_finding,potential_matches,approved_findings_only)

    ## Collections APIs

    def get_collections(self):
        return Collections().get_all()

    def get_collections_by_name(self,collection_name):
        return Collections().get_by_name(collection_name)

    def get_collections_by_business_unit(self,business_unit_name):
        return Collections().get_by_business_unit(business_unit_name)

    def get_collections_statistics(self):
        return Collections().get_statistics()

    def get_collection(self,guid: UUID):
        return Collections().get(guid)

    def get_collection_assets(self,guid: UUID):
        return Collections().get_assets(guid)

    def create_collection(self,name,description="",tags='',business_unit_guid: UUID=None,custom_fields=[],assets=[]):
        return Collections().create(name,description,tags,business_unit_guid,custom_fields,assets)

    def update_collection(self,guid,name,description="",tags="",business_unit_guid: UUID=None,custom_fields=[],assets=[]):
        return Collections().update(guid,name,description,tags,business_unit_guid,custom_fields,assets)

    def delete_collection(self,guid: UUID):
        return Collections().delete(guid)

    ## Identity APIs

    def get_users(self):
        return Users().get_all()

    def get_user_self (self):
        return Users().get_self()

    def get_user(self,user_guid: UUID):
        return Users().get(user_guid)

    def get_user_by_name(self,username):
        return Users().get_by_name(username)

    def get_user_by_search(self, search_term=None, api_id: UUID=None, role_id: UUID=None, login_status=None, saml_user=None, team_id: UUID=None, detailed=False, user_type=None, request_params=None):
        return Users().get_user_search(search_term,api_id,role_id,login_status,saml_user,team_id,detailed,user_type,request_params)

    def create_user (self,email,firstname,lastname,username=None,type="HUMAN",roles=[],teams=[],mfa=False):
        return Users().create(email,firstname,lastname,username,type,roles,teams,mfa=mfa)

    def update_user_roles (self,user_guid: UUID,roles):
        return Users().update_roles(user_guid,roles)

    def update_user (self,user_guid: UUID,changes):
        return Users().update(user_guid,changes)
    
    def update_user_email_address (self,user_guid: UUID,email_address,ignore_verification=False):
        return Users().update_email_address(user_guid,email_address,ignore_verification)
    
    def send_password_reset (self,user_legacy_id):
        return Users().reset_password(user_legacy_id)

    def disable_user (self,user_guid: UUID):
        return Users().disable(user_guid)

    def delete_user (self,user_guid: UUID):
        return Users().delete(user_guid)

    def get_teams (self, all_for_org=False):
        return Teams().get_all(all_for_org)

    def create_team (self, team_name, business_unit: UUID=None, members=[]):        
        return Teams().create(team_name,business_unit,members)

    def update_team (self, team_guid: UUID, team_name="", business_unit: UUID=None, members=[]):
        return Teams().update(team_guid,team_name,business_unit,members)

    def delete_team (self, team_guid: UUID):
        return Teams().delete(team_guid)
            
    def get_business_units (self):
        return BusinessUnits().get_all()

    def get_business_unit (self, guid: UUID):
        return BusinessUnits().get(guid)

    def create_business_unit (self, name, teams=[]):
        return BusinessUnits().create(name,teams)

    def update_business_unit (self, guid: UUID, name='', teams=[]):
        return BusinessUnits().update(guid,name,teams)

    def delete_business_unit (self, guid: UUID):
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

    def add_workspace_team(self,workspace_guid: UUID,team_id: UUID):
        return Workspaces().add_team(workspace_guid,team_id)

    def delete_workspace(self,workspace_guid: UUID):
        return Workspaces().delete(workspace_guid)

    def get_projects(self,workspace_guid: UUID):
        return Workspaces().get_projects(workspace_guid)

    def get_project(self,workspace_guid: UUID,project_guid: UUID):
        return Workspaces().get_project(workspace_guid,project_guid)

    def get_project_issues(self,workspace_guid: UUID,project_guid: UUID):
        return Workspaces().get_project_issues(workspace_guid,project_guid)

    def get_project_libraries(self,workspace_guid: UUID,project_guid: UUID):
        return Workspaces().get_project_libraries(workspace_guid,project_guid)

    def get_agents(self,workspace_guid: UUID):
        return Workspaces().get_agents(workspace_guid)

    def get_agent(self,workspace_guid: UUID,agent_guid: UUID):
        return Workspaces().get_agent(workspace_guid,agent_guid)

    def create_agent(self,workspace_guid: UUID,name,agent_type='CLI'):
        return Workspaces().create_agent(workspace_guid,name,agent_type)

    def get_agent_tokens(self,workspace_guid: UUID,agent_guid: UUID):
        return Workspaces().get_agent_tokens(workspace_guid,agent_guid)

    def get_agent_token(self,workspace_guid: UUID,agent_guid: UUID,token_id: UUID):
        return Workspaces().get_agent_token(workspace_guid,agent_guid,token_id)
        
    def regenerate_agent_token(self,workspace_guid: UUID,agent_guid: UUID):
        return Workspaces().regenerate_agent_token(workspace_guid,agent_guid)

    def revoke_agent_token(self,workspace_guid: UUID,agent_guid: UUID,token_id: UUID):
        return Workspaces().revoke_agent_token(workspace_guid,agent_guid,token_id)

    def get_issues(self,workspace_guid: UUID):
        return Workspaces().get_issues(workspace_guid)

    def get_issue(self,issue_id: UUID):
        return Workspaces().get_issues(issue_id)

    def get_libraries(self,workspace_guid: UUID,unmatched=False):
        return Workspaces().get_libraries(workspace_guid, unmatched)

    def get_library(self,library_id):
        return Workspaces().get_library(library_id)

    def get_vulnerability(self,vulnerability_id):
        return Workspaces().get_vulnerability(vulnerability_id)

    def get_license(self,license_id):
        return Workspaces().get_license(license_id)

    def get_sca_events(self,date_gte=None,event_group=None,event_type=None):
        return Workspaces().get_events(date_gte,event_group,event_type)

    def get_sca_scan(self,scan_id: UUID):
        return Workspaces().get_scan(scan_id)

    def get_component_activity(self,component_id):
        return ComponentActivity().get(component_id)

    def get_sbom(self,app_guid: UUID):
        return SBOM().get(app_guid)

    def get_sbom_project(self,project_guid: UUID):
        return SBOM().get_for_project(project_guid)

    #dynamic APIs

    def get_analyses(self):
        return Analyses().get_all()

    def get_analyses_by_name(self,name):
        return Analyses().get_by_name(analysis_name=name)

    def get_analyses_by_target_url(self,url):
        return Analyses().get_by_target_url(target_url=url)

    def get_analyses_by_search_term(self,search_term):
        return Analyses().get_by_search_term(search_term=search_term)

    def get_analysis(self,analysis_id: UUID):
        return Analyses().get(guid=analysis_id)
    
    def get_analysis_audits(self,analysis_id: UUID):
        return Analyses().get_audits(guid=analysis_id)

    def get_analysis_scans(self,analysis_id: UUID):
        return Analyses().get_scans(guid=analysis_id)

    def get_analysis_scanner_variables(self,analysis_id: UUID):
        return Analyses().get_scanner_variables(guid=analysis_id)

    def create_analysis(self,name,scans,business_unit_guid: UUID=None,email=None,owner=None):
        return Analyses().create(name,scans,business_unit_guid,email,owner)

    def update_analysis(self,guid: UUID,name,scans,business_unit_guid: UUID=None,email=None,owner=None):
        return Analyses().update(guid,name,scans,business_unit_guid,email,owner)
    
    def update_analysis_scanner_variable(self,analysis_guid: UUID,scanner_variable_guid: UUID,reference_key,value,description):
        return Analyses().update_scanner_variable(analysis_guid,scanner_variable_guid,reference_key,value,description)

    def delete_analysis_scanner_variable(self,analysis_guid: UUID,scanner_variable_guid: UUID):
        return Analyses().delete_scanner_variable(analysis_guid,scanner_variable_guid)

    def delete_analysis(self,analysis_guid: UUID):
        return Analyses().delete(guid=analysis_guid)
    
    def get_dyn_scan(self,scan_guid: UUID):
        return Scans().get(guid=scan_guid)

    def get_dyn_scan_audits(self,scan_guid: UUID):
        return Scans().get_audits(guid=scan_guid)

    def get_dyn_scan_config(self,scan_guid: UUID):
        return Scans().get_configuration(guid=scan_guid)

    def update_dyn_scan(self,scan_guid: UUID,scan):
        return Scans().update(guid=scan_guid,scan=scan)

    def delete_dyn_scan(self,scan_guid: UUID):
        return Scans().delete(guid=scan_guid)

    def get_scan_scanner_variables(self,scan_id: UUID):
        return Scans().get_scanner_variables(guid=scan_id)

    def update_scan_scanner_variable(self,scan_guid: UUID,scanner_variable_guid: UUID,reference_key,value,description):
        return Scans().update_scanner_variable(scan_guid,scanner_variable_guid,reference_key,value,description)

    def delete_scan_scanner_variable(self,scan_guid: UUID,scanner_variable_guid: UUID):
        return Scans().delete_scanner_variable(scan_guid,scanner_variable_guid)

    def get_analysis_occurrences(self):
        return Occurrences().get_all()

    def get_analysis_occurrence(self,occurrence_guid: UUID):
        return Occurrences().get(guid=occurrence_guid)

    def stop_analysis_occurrence(self,occurrence_guid: UUID,save_or_delete):
        return Occurrences().stop(guid=occurrence_guid,save_or_delete=save_or_delete)

    def get_scan_occurrences(self,occurrence_guid: UUID):
        return Occurrences().get_scan_occurrences(guid=occurrence_guid)

    def get_scan_occurrence(self,scan_occ_guid: UUID):
        return ScanOccurrences().get(guid=scan_occ_guid)

    def stop_scan_occurrence(self,scan_occ_guid: UUID,save_or_delete):
        return ScanOccurrences().stop(guid=scan_occ_guid, save_or_delete=save_or_delete)

    def get_scan_occurrence_configuration(self,scan_occ_guid: UUID):
        return ScanOccurrences().get_configuration(guid=scan_occ_guid)

    def get_scan_occurrence_verification_report(self,scan_occ_guid: UUID):
        return ScanOccurrences().get_verification_report(guid=scan_occ_guid)

    def get_scan_occurrence_notes_report(self,scan_occ_guid: UUID):
        return ScanOccurrences().get_scan_notes_report(guid=scan_occ_guid)

    def get_scan_occurrence_screenshots(self,scan_occ_guid: UUID):
        return ScanOccurrences().get_screenshots(guid=scan_occ_guid)

    def get_codegroups(self):
        return CodeGroups().get_all()

    def get_codegroup(self,name):
        return CodeGroups().get(name=name)

    def get_dynamic_configuration(self):
        return Configuration().get()

    def get_dynamic_scan_capacity_summary(self):
        return ScanCapacitySummary().get()

    def get_global_scanner_variables(self):
        return ScannerVariables().get_all()

    def get_global_scanner_variable(self,guid: UUID):
        return ScannerVariables().get(guid)
    
    def create_global_scanner_variable(self,reference_key,value,description):
        return ScannerVariables().create(reference_key,value,description)

    def update_global_scanner_variable(self,guid: UUID,reference_key,value,description):
        return ScannerVariables().update(guid,reference_key,value,description)

    def delete_global_scanner_variable(self,guid: UUID):
        return ScannerVariables().delete(guid)

    def dyn_setup_user_agent(self,custom_header,type):
        return DynUtils().setup_user_agent(custom_header,type)

    def dyn_setup_custom_host(self,host_name,ip_address):
        return DynUtils().setup_custom_host(host_name,ip_address)

    def dyn_setup_blocklist(self, urls:List):
        return DynUtils().setup_blocklist(urls)

    def dyn_setup_url(self,url,directory_restriction_type='DIRECTORY_AND_SUBDIRECTORY',http_and_https=True):
        return DynUtils().setup_url(url,directory_restriction_type,http_and_https)

    def dyn_setup_scan_setting(self,blocklist_configs:list,custom_hosts:List, user_agent:None):
        return DynUtils().setup_scan_setting(blocklist_configs,custom_hosts,user_agent)

    def dyn_setup_scan_contact_info(self,email,first_and_last_name,telephone):
        return DynUtils().setup_scan_contact_info(email,first_and_last_name,telephone)

    def dyn_setup_crawl_script(self,script_body,script_type='SELENIUM'):
        return DynUtils().setup_crawl_script(script_body,script_type)

    def dyn_setup_crawl_configuration(self,scripts:List,disabled=False):
        return DynUtils().setup_crawl_configuration(scripts,disabled)

    def dyn_setup_login_logout_script(self,script_body,script_type='SELENIUM'):
        return DynUtils().setup_login_logout_script(script_body,script_type)

    def dyn_setup_auth(self,authtype,username,password,domain=None,base64_pkcs12=None,cert_name=None, login_script_data=None, logout_script_data=None):
        return DynUtils().setup_auth(authtype,username,password,domain,base64_pkcs12,cert_name,login_script_data,logout_script_data)

    def dyn_setup_auth_config(self,authentication_node:dict):
        return DynUtils().setup_auth_config(authentication_node)

    def dyn_setup_scan_config_request(self, url, allowed_hosts:List, auth_config=None, crawl_config=None, scan_setting=None):
        return DynUtils().setup_scan_config_request(url,allowed_hosts,auth_config,crawl_config,scan_setting)

    def dyn_setup_scan(self, scan_config_request, scan_contact_info=None, linked_app_guid: UUID=None):
        return DynUtils().setup_scan(scan_config_request,scan_contact_info, linked_app_guid)