# API Object

As an alternative to importing individual objects into your library, you can access all methods in `veracode-api-py` from the `API()` object. Unless otherwise noted, the following methods call Veracode REST APIs and return JSON.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc --maxlevel 2 api.md TO UPDATE -->
**Table of Contents**

- [Health Check](#health-check)
- [Reporting and Findings](#reporting-and-findings)
- [Applications and Policy](#applications-and-policy)
- [Dynamic Analysis](#dynamic-analysis)
- [Software Composition Analysis (SCA)](#software-composition-analysis-sca)
- [Users, Credentials, Teams, and Business Units](#users-credentials-teams-and-business-units)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Health Check

*See also*: You can also access these methods from the [Healthcheck class](healthcheck.md).

- `healthcheck()`: returns an empty response with HTTP 200 if authentication succeeds.
- `status()`: returns detailed status of Veracode services, mirroring [status.veracode.com](https://status.veracode.com).

## Reporting and Findings

### Analytics Reporting

1. *Accessing*: The Reporting API is available to Veracode customers by request. 
1. *More information*: See the [Veracode Docs](https://docs.veracode.com/r/Reporting_REST_API).
1. *See Also*: You can also access these methods from the [Analytics class](analytics.md).

- `create_analytics_report(report_type ('findings'),last_updated_start_date, last_updated_end_date (opt), scan_type (opt), finding_status(opt), passed_policy(opt), policy_sandbox(opt), application_id(opt), rawjson(opt))`: set up a request for a report. By default this command returns the GUID of the report request; specify `rawjson=True` to get the full response. Dates should be specified as `YYYY-MM-DD HH:MM:SS` with the timestamp optional. Options include:
  - `report_type`: required, currently only supports `findings`
  - `last_updated_start_date`: required, beginning of date range for new or changed findings
  - `last_updated_end_date`: optional, end of date range for new or changed findings
  - `scan_type`: optional, one or more of 'Static Analysis', 'Dynamic Analysis', 'Manual', 'Software Composition Analysis', 'SCA'
  - `finding_status`: optional, 'Open' or 'Closed'
  - `passed_policy`: optional, boolean
  - `policy_sandbox`: optional, 'Policy' or 'Sandbox'
  - `application_id`: optional, application ID for which to return results
  - `rawjson`: optional, defaults to False. Returns full response if True, the GUID of the request if false

- `get_analytics_report(guid)`: check the status of the report request and return the report contents when ready. Note that this method returns a tuple of `status` (string) and `results` (list); when `status` is `COMPLETED`, the `results` list will populate with results.

### Findings

*See also*: You can also access these methods from the [Findings class](findings.md#findings-and-annotations).

- `get_findings(app,scantype(opt),annot(opt),request_params(opt),sandbox(opt))`: get the findings for `app` (guid).
  - `scantype`: Defaults to STATIC findings, but can be STATIC, DYNAMIC, MANUAL, SCA, or ALL (static, dynamic, manual).
  - `annot`: Defaults to TRUE but can be FALSE
  - `sandbox`: The guid of the sandbox in `app` for which you want findings. (Use the Sandboxes APIs to get the sandbox guid.)
  - `request_params`: Dictionary of additional query parameters. See the full [Findings API specification](https://help.veracode.com/r/c_findings_v2_intro) for some of the other options available.
- `get_static_flaw_info(app,issueid,sandbox(opt))`: get the static flaw information, including data paths, for the finding identified by `issueid` in `app` (guid) or its `sandbox` (guid).
- `get_dynamic_flaw_info(app,issueid)`: get the dynamic flaw information, including request/response data, for the finding identified by `issueid` in `app` (guid).
- `add_annotation(app,issue_list,comment,action,sandbox(opt))`: add an annotation (comment, mitigation proposal/acceptance/rejection) to the findings in `issue_list` for `app` (guid) (or optionally `sandbox` (guid)). Note that you must have the Mitigation Approver role (regular user) to use the ACCEPTED or REJECTED action, or the Mitigation and Comments API role for an API service account to use this call.
  - `issue_list`: must be passed as a Python list of `issue_id`s
  - `action`: must be one of COMMENT, POTENTIAL_FALSE_POSITIVE, APP_BY_DESIGN, OS_ENV, NET_ENV, LIBRARY, ACCEPT_RISK, ACCEPTED, REJECTED
- `match_findings(origin_finding,potential_matches,approved_findings_only(opt),allow_fuzzy_match(opt))`: return a matching finding from `potential_matches` for the `origin_finding`, based on the finding type.
  - `approved_findings_only`: limits matches to findings with approved mitigations.
  - `allow_fuzzy_match`: look for matches within a range of source lines around the origin finding. This allows for code movement but can result in flaws being mismatched; use sparingly.

### MPT Scans and Findings

*See also*: You can also access these methods from the [ManualScans class](findings.md#manual-testing).

- `get_manual_scans_for_app(appid)`: get the manual scans for `appid` (guid).
- `get_manual_scan(scanid)`: get the manual scan information for `scanid` (int), returned by `get_manual_scans_for_app()`.
- `get_manual_findings(scanid,include_artifacts(opt))`: get the manual findings detail for `scanid` (int). 
  - `include_artifacts`: if `True`, includes screenshots and code samples associated with the findings. 

### Summary Report

*See also*: You can also access this method from the [SummaryReport class](findings.md#summary-report).

- `get_summary_report(app,sandbox(opt))`: get the summary report for `app` (guid) or its `sandbox` (guid).

## Applications and Policy

### Applications

*See also*: You can also access these methods from the [Applications class](applications.md).

- `get_apps(policy_check_after(opt))` : get a list of Veracode applications (JSON format). If provided, returns only applications that have a policy check date on or after `policy_check_after` (format is `yyyy-mm-dd`).
- `get_app(guid(opt),legacy_id(opt))`: get information for a single Veracode application using either the `guid` or the `legacy_id` (integer).
- `get_app_by_name(name)`: get list of applications whose names contain the search string `name`.
- `create_app(app_name, business_criticality, business_unit(opt), teams(opt), policy_guid(opt), custom_fields(opt array), bus_owner_name(opt), bus_owner_email(opt),git_repo_url(opt))`: create an application profile.
  - `business_criticality`: one of "VERY HIGH", "HIGH", "MEDIUM", "LOW", "VERY LOW"
  - `business_unit`: the GUID of the business unit to which the application should be assigned
  - `teams`: a list of the GUIDs of the teams to which the application should be assigned
  - `policy_guid`: the GUID of the policy to set for this application.
  - `custom_fields`: an array of custom field values for the application
  - `bus_owner_name`: the name of the business owner of the application
  - `bus_owner_email`: the email address of the business owner of the application
  - `git_repo_url`: the URL to the git repository containing the code for the application
- `update_app(guid, app_name, business_criticality, business_unit(opt), teams(opt), policy_guid(opt), custom_fields(opt array), bus_owner_name(opt), bus_owner_email(opt),git_repo_url(opt))`: update an application profile. Note that partial updates are NOT supported, so you need to provide all values including those that aren't changing.
- `delete_app(guid)`: delete the application identified by `guid`. This is not a reversible action.
- `get_custom_fields()`: get a list of app profile custom fields available for your organization.

### Sandboxes

*See also*: You can also access these methods from the [Sandboxes class](applications.md#sandboxes).

- `get_app_sandboxes(guid)`: get the sandboxes associated with the application identified by `guid`.
- `create_sandbox(app,name,auto_recreate(opt),custom_fields(opt))`: create a sandbox in the application identified by `app`. Custom fields must be specified as a list of dictionaries of `name`/`value` pairs, e.g. [{'name': 'Custom 1','value': 'foo'}].
- `update_sandbox(app,sandbox,name,auto_recreate(opt),custom_fields(opt))`: update the `sandbox` (guid) in `app` (guid) with the provided values. Note that partial updates are NOT supported, so you need to provide all values including those you don't wish to change.
- `delete_sandbox(app,sandbox)`: delete `sandbox` (guid) in `app` (guid).

### Collections

1. *Accessing*: The Collections feature is available only to Veracode customers in the Collections Early Adopter program. As the Collections feature is not generally available yet, the functionality of the feature will change over time.
2. *See also*: You can also access this method from the [Collections class](collections.md).

- `get_collections()`: get all collections for the organization.
- `get_collections_by_name(collection_name)`: get all collections with a name that partially matches `collection_name`.
- `get_collections_by_business_unit(business_unit_name)`: get all collections associated with `business_unit_name` (exact match).
- `get_collections_statistics()`: get summary counts of collections by policy status.
- `get_collection(guid)`: get detailed information for the collection identified by `guid`.
- `get_collection_assets(guid)`: get a list of assets and detailed policy information for the collection identified by `guid`.
- `create_collection(name, description(opt), tags(opt), business_unit_guid(opt),custom_fields(opt list),assets(opt list of application guids))`: create a collection with the provided settings.
- `update_collection(guid, name, description(opt), tags(opt), business_unit_guid(opt),custom_fields(opt list),assets(opt list of application guids))`: update the collection identified by `guid` with the provided settings.
- `delete_collection(guid)`: delete the collection identified by `guid`.

### Policy

_See also_: You can also access these methods from the [Policies class](policy.md).

- `get_policies`: Get a list of available policies.
- `get_policy(guid)`: get information for the policy corresponding to `guid`.
- `create_policy(name,description,vendor_policy(opt),finding_rules(opt),scan_frequency_rules(opt),grace_period_rules(opt))`: create a policy
- `update_policy(guid,name,description,vendor_policy(opt),finding_rules(opt),scan_frequency_rules(opt),grace_period_rules(opt))`: update a policy
- `delete_policy(guid)`: delete a policy

## Dynamic Analysis

### Analyses

*See also*: You can also access these methods from the [Analyses class](dynamic.md#analyses).

- `get_analyses()`: get a list of dynamic analyses to which you have access.
- `get_analyses_by_name(name)`: get a list of dynamic analyses matching `name`.
- `get_analyses_by_target_url(url)`: get a list of dynamic analyses containing `url`.
- `get_analyses_by_search_term(search_term)`: get a list of dynamic analyses matching `search_term`.
- `get_analysis(analysis_id)`: get the analysis identified by `analysis_id` (guid).
- `get_analysis_audits(analysis_id)`: get the audits for the analysis identified by `analysis_id` (guid).
- `get_analysis_scans(analysis_id)`: get the scans for the analysis identified by `analysis_id` (guid).
- `get_analysis_scanner_variables(analysis_id)`: get the scanner variables for the analysis identified by `analysis_id` (guid).
- `create_analysis(name,scans,schedule_frequency='ONCE',start_scan (opt),business_unit_guid (opt),email (opt),owner (opt))`: create an analysis with the provided settings. Use `setup_scan` and related functions to construct the list of scans.
- `update_analysis(guid,name,scans,schedule_frequency='ONCE',start_scan (opt),business_unit_guid (opt),email (opt),owner (opt))`: update the analysis identified by `guid` with the provided settings.
- `update_analysis_scanner_variable(analysis_guid,scanner_variable_guid,reference_key,value,description)`: update the scanner variable identified by the `scanner_variable_guid` for the analysis identified by `analysis_guid`.
- `delete_analysis_scanner_variable(analysis_guid,scanner_variable_guid)`: delete the scanner variable identified by the `scanner_variable_guid` for the analysis identified by `analysis_guid`.
- `delete_analysis(analysis_guid)`: delete the analysis identified by `analysis_guid`.

### Scans and Occurrences

#### Scans

*See also*: You can also access these methods from the [Scans class](dynamic.md#scans).

- `get_dyn_scan(scan_guid)`: get the scan identified by `scan_guid`. Get `scan_guid` from `get_analysis_scans()`.
- `get_dyn_scan_audits(scan_guid)`: get the audits for the scan identified by `scan_guid`.
- `get_dyn_scan_config(scan_guid)`: get the scan config for the scan identified by `scan_guid`.
- `update_dyn_scan(scan_guid,scan)`: update the scan identified by `scan_guid`. Prepare `scan` with `dyn_setup_scan()`.
- `delete_dyn_scan(scan_guid)`: delete the scan identified by `scan_guid`.
- `get_scan_scanner_variables(scan_id)`: get the scanner variables for the scan identified by `scan_guid`.
- `update_scan_scanner_variable(scan_guid,scanner_variable_guid,reference_key,value,description)`: update the scanner variable identified by the `scanner_variable_guid` for the scan identified by `scan_guid`.
- `delete_scan_scanner_variable(scan_guid,scanner_variable_guid)`: delete the scanner variable identified by the `scanner_variable_guid` for the scan identified by `scan_guid`.

#### Occurrences

*See also*: You can also access these methods from the [Occurrences class](dynamic.md#scans).

- `get_analysis_occurrences()`: get all dynamic analysis occurrences.
- `get_analysis_occurrence(occurrence_guid)`: get the dynamic analysis occurrence identified by `occurrence_guid`.
- `stop_analysis_occurrence(occurrence_guid,save_or_delete)`: stop the dynamic analysis occurrence identified by `occurrence_guid`. Analysis results identified so far are processed according to `save_or_delete`.

#### Scan Occurrences

*See also*: You can also access these methods from the [ScanOccurrences class](dynamic.md#scans).

- `get_scan_occurrences(occurrence_guid)`: get the scan occurrences for the dynamic analysis occurrence identified by `occurrence_guid`.
- `get_scan_occurrence(scan_occ_guid)`: get the scan occurrence identified by `scan_occ_guid`.
- `stop_scan_occurrence(scan_occ_guid,save_or_delete)`: stop the scan occurrence identified by `scan_occ_guid`. Scan results identified so far are processed according to `save_or_delete`.
- `get_scan_occurrence_configuration(scan_occ_guid)`: get the configuration of the scan occurrence identified by `scan_occ_guid`.
- `get_scan_occurrence_verification_report(scan_occ_guid)`: get the verification report of the scan occurrence identified by `scan_occ_guid`.
- `get_scan_occurrence_notes_report(scan_occ_guid)`: get the scan notes report of the scan occurrence identified by `scan_occ_guid`.
- `get_scan_occurrence_screenshots(scan_occ_guid)`: get the screenshots of the scan occurrence identified by `scan_occ_guid`.

### Global settings

_See also_: You can also access these methods from the [CodeGroups class](dynamic.md#global-settings).

- `get_codegroups()`: get the allowable code values for all code groups for Dynamic Analysis.
- `get_codegroup(name)`: get the allowable code values for the Dynamic Analysis code group identified by `name`.

_Note_: You can also access these methods from the `Configuration` class.

- `get_dynamic_configuration()`: get the default Dynamic Analysis configuration.

_Note_: You can also access these methods from the `ScanCapacitySummary` class.

- `get_dynamic_scan_capacity_summary()`: get the Dynamic Analysis scan capacity summary.

_Note_: You can also access these methods from the `ScannerVariables` class.

- `get_global_scanner_variables()`: get the list of global Dynamic Analysis scanner variables.
- `get_global_scanner_variable(guid)`: get the Dynamic Analysis global scanner variable identified by `guid`.
- `create_global_scanner_variable(reference_key,value,description)`: create a global Dynamic Analysis scanner variable.
- `update_global_scanner_variable(guid,reference_key,value,description)`: update the global Dynamic Analysis scanner variable identified by `guid`.
- `delete_global_scanner_variable(guid)`: delete the global Dynamic Analysis scanner variable identified by `guid`.

### Utilities

*See also*: You can also access these methods from the [DynUtils class](dynamic.md#utilities).

- `dyn_setup_user_agent(custom_header,type)`: set up the payload to specify the user agent for a dynamic scan.
- `dyn_setup_custom_host(host_name,ip_address)`: set up the payload to specify the custom host for a dynamic scan.
- `dyn_setup_blocklist( urls:List)`: set up the payload to specify the blocklist for a dynamic scan.
- `dyn_setup_url(url,directory_restriction_type='DIRECTORY_AND_SUBDIRECTORY',http_and_https=True)`: set up the payload to specify a URL object for a dynamic scan. This payload can be used in other setup calls that require a `url`.
- `dyn_setup_scan_setting(blocklist_configs:list,custom_hosts:List, user_agent(opt))`: set up the payload to specify a scan setting for a dynamic scan.
- `dyn_setup_scan_contact_info(email,first_and_last_name,telephone)`: set up the payload to specify contact information for a dynamic scan.
- `dyn_setup_crawl_script(script_body,script_type='SELENIUM')`: set up the payload to specify crawl script information for a dynamic scan.
- `dyn_setup_crawl_configuration(scripts:List,disabled=False)`: set up the payload to specify crawl configuration for a dynamic scan.
- `dyn_setup_login_logout_script(script_body,script_type='SELENIUM')`: set up the payload to specify login/logout script information for a dynamic scan.
- `dyn_setup_auth(authtype,username,password,domain(opt),base64_pkcs12(opt),cert_name(opt), login_script_data(opt), logout_script_data(opt))`: set up the payload to specify authentication information for a specific authtype for a dynamic scan. The following parameters are required:
  - `AUTO`: `username`, `password`
  - `BASIC`: `username`, `password`, `domain` (opt)
  - `CERT`: `base64_pkcs12`, `cert_name`, `password`
  - `FORM`: `login_script_data`, `logout_script_data`
- `dyn_setup_auth_config(authentication_node:dict)`: set up the payload to specify authentication information for a dynamic scan. Set up `authentication_node` with `dyn_setup_auth`.
- `dyn_setup_scan_config_request( url, allowed_hosts:List, auth_config(opt), crawl_config(opt), scan_setting(opt))`: set up the payload to specify the scan config request for a dynamic scan. `url` and `allowed_hosts` are set up using `dyn_setup_url()`. `crawl_config` is setup using `dyn_setup_crawl_configuration()`. `scan_setting` is setup using `dyn_setup_scan_setting()`.
- `dyn_setup_scan( scan_config_request, scan_contact_info(opt), linked_app_guid(opt))`: set up the payload to specify the scan for a Dynamic Analysis. `scan_config_request` is setup using `dyn_setup_scan_config_request()` and `scan_contact_info` is set up using `dyn_setup_scan_contact_info()`. Specify `linked_app_guid` (using `get_apps()` or `get_app()`) to link the scan results to an application profile.
- `dyn_start_scan(length,unit)`: start a dynamic analysis and set duration. 

## Software Composition Analysis (SCA)

*Accessing*: SCA APIs must be called with a human user, since the SCA Agent APIs do not currently support being called by an API Service User.

### Workspaces, Projects, Issues, and Agents

*See also*: You can also access these methods from the [Workspaces class](sca.md#workspaces-projects-issues-and-agents).

- `get_workspaces(include_metrics(opt))`: get a list of SCA Agent workspaces for the organization. The `include_metrics` parameter can add counts of issues and other attributes in the response, at some cost to performance, and defaults to `False`.
- `get_workspace_by_name(name)`: get a list of SCA Agent workspaces whose name partially matches `name`.
- `create_workspace(name)`: create an SCA Agent workspace named `name`. Returns the GUID for the workspace.
- `add_workspace_team(workspace_guid,team_id)`: add the team identified by `team_id` (int) to the workspace identified by `workspace_guid`.
- `get_workspace_teams(workspace_guid(opt))`: get a list of teams. If no `workspace_guid` is provided, return all available teams.
- `delete_workspace(workspace_guid)`: delete the workspace identified by `workspace_guid`.
- `get_projects(workspace_guid,project_name(opt))`: get a list of projects for the workspace identified by `workspace_guid`.
- `get_agents(workspace_guid)`: get a list of agents for the workspace identified by `workspace_guid`.
- `get_agent(workspace_guid,agent_guid)`: get the agent identified by `agent_guid` in the workspace identified by `workspace_guid`.
- `create_agent(workspace_guid,name,agent_type(opt))`: create an agent in the workspace identified by `workspace_guid`. Default for `agent_type` is `CLI`.
- `delete_agent(workspace_guid,agent_guid)`: delete the agent identified by `agent_guid`.
- `get_agent_tokens(workspace_guid, agent_guid)`: get token IDs for the agent identified by `agent_guid` in the workspace identified by `workspace_guid`.
- `get_agent_token(workspace_guid, agent_guid, token_id)`: get the token ID identified by `token_id`.
- `regenerate_agent_token(workspace_guid, agent_guid)`: regenerate the token for the agent identified by `agent_id`.
- `revoke_agent_token(workspace_guid, agent_guid, token_id)`: revoke the token identified by `token_id`.
- `get_issues(workspace_guid, branch(opt), direct(opt), created_after(opt), ignored(opt), vuln_method(opt), project_id (opt array))`: get the list of issues for the workspace identified by `workspace_guid`.
- `get_issue(issue_id)`: get the issue identified by `issue_id`.
- `get_scan(scan_id)`: get the scan identified by `scan_id` (returned in `get_issue`).
- `get_libraries(workspace_guid,unmatched(bool,opt))`: get the libraries associated with the workspace identified by `workspace_guid`.
- `get_library(library_id)`: get the library identified by `library_id` (e.g. "maven:commons-fileupload:commons-fileupload:1.3.2:")
- `get_vulnerability(vulnerability_id)`: get the vulnerability identified by `vulnerability_id` (an integer value, visible in the output of `get_issues`).
- `get_license(license_id)`: get the license identified by `license_id` (a string, e.g. "GPL30").
- `get_sca_events(date_gte,event_group,event_type)`: get the audit events for the arguments passed. Be careful with the arguments for this and try to limit by date as it will fetch all pages of data, which might be a lot.

### Component Activity

*See also*: You can also access these methods from the [ComponentActivity class](sca.md#component-activity).

- `get_component_activity(component_id)`: get the activity for the component identified by `component_id` (similar to `library_id` above, e.g. "maven:net.minidev:json-smart:1.3.1").

### SBOM

*See also*: You can also access these methods from the [SBOM class](sca.md#sbom).

- `get_sbom(app_guid,format(opt),linked(opt),vulnerability(opt),dependency(opt))`: generate an SBOM in either CycloneDX (default) or SPDX format for the application represented by `app_guid`. Get the `app_guid` from the Applications API. The following options are available:
  - `linked` (CycloneDX only): if `True`, returns an SBOM based on the linked SCA Agent project. Defaults to `False`.
  - `vulnerability`: if `True`, returns an SBOM containing vulnerability information. Defaults to `True`.
  - `dependency` (SPDX only): if `True`, returns an SBOM that includes dependency information. Defaults to `True`.
- `get_sbom_project(project_guid,format(opt),vulnerability(opt))`: generate an SBOM in CycloneDX (default) or SPDX format for the SCA Agent project represented by `project_guid`. Get the `project_guid` from the SCA Agent API (e.g. `get_projects(workspace_guid)`). The following options are available:
  - `vulnerability`: if `True`, returns an SBOM containing vulnerability information. Defaults to `True`.
  - `dependency` (SPDX only): if `True`, returns an SBOM that includes dependency information. Defaults to `True`.
- `scan_sbom(sbom)`: (EXPERIMENTAL) Scan an SBOM (pass the filename, including absolute path, as the `sbom` parameter) and return an updated SBOM with additional vulnerability information from the Veracode SCA Database.


### Application Info

*See also*: You can also access these methods from the [SCAApplications class](sca.md#application-info).

- `get_app_projects(app_guid)`: get the list of linked SCA projects for an application. (This API call is also available on the SCAApplications object as `SCAApplications().get_projects()`.)
- `link_project(app_guid, project_guid)`: link the application to the project. (This API call is also available on the SCAApplications object as `SCAApplications().link_project()`.)
- `unlink_project(app_guid, project_guid)`: unlink the application from the project. (This API call is also available on the SCAApplications object as `SCAApplications().unlink_project()`.)
- `get_sca_annotations(app_guid, annotation_type, annotation_reason(opt), annotation_status(opt),cve_name(opt), cwe_id(opt), severities(opt array), license_name(opt), license_risk(opt))`: get the list of annotations (mitigations and comments) for an application. (This API call is also available on the SCAApplications object as `SCAApplications().get_annotations()`.)
- `add_sca_annotation(app_guid, action, comment, annotation_type, component_id, cve_name (required for VULNERABILITY type), license_id (required for LICENSE type))`: add an annotation (mitigation or comment) to an SCA vulnerability or license finding. Note that ability to APPROVE or REJECT requires the mitigation approver role. (This API call is also available on the SCAApplications object as `SCAApplications().add_annotation()`.)

## Users, Credentials, Teams, and Business Units

*Accessing*: Calling these methods requires a user with the [Administator, Team Admin,](https://docs.veracode.com/r/c_role_permissions) or [Admin API](https://docs.veracode.com/r/c_API_roles_details) user role, except as noted.

### Users

*See also*: You can also access this method from the [Users class](users.md).

- `get_users()`: get a list of users for the organization.
- `get_user_self()`: get user information for the current user. Accessible by any user role.
- `get_user(user_guid)`: get information for an individual user based on `user_guid`.
- `get_user_by_name(username)`: look up info for an individual user based on their user_name.
- `get_user_by_search(search_term, api_id, role_id, login_status, saml_user, team_id, detailed, user_type, request_params)`: search for users based on parameters below (all optional):
  - `search_term`: string
  - `api_id`: search by customer api id
  - `role_id`: search by role_id (see `get_roles`)
  - `login_status`: search by login status (e.g. `active`)
  - `saml_user`: search by saml user ID
  - `team_id`: serach by team ID (see `get_teams`)
  - `detailed`: returns additional attributes in summary list of users
  - `user_type`: search by user type (e.g. `user` or `api`)
  - `request_params`: optionally pass a dictionary of additional query parameters. See [Identity API specification](https://app.swaggerhub.com/apis/Veracode/veracode-identity_api/1.0#/user/getUsersBySearchUsingGET)
- `create_user(email,firstname,lastname,type(opt),username(opt),roles(opt),mfa(opt))`: create a user based on the provided information.
  - `type`: `"HUMAN"` or `"API"`. Defaults to `"HUMAN"`. If `"API"` specified, must also provide `username`.
  - `roles`: list of role names (specified in the Veracode Help Center, for both [human](https://help.veracode.com/go/c_identity_create_human) and [API service account](https://help.veracode.com/go/c_identity_create_api) users). Provide the role names from `get_roles()`.
  - `mfa`: set to `TRUE` to require the user to configure multifactor authentication on first sign in.
- `update_user_roles(user_guid, roles)`: update the user identified by `user_guid` with the list of roles passed in `roles`. Because the Identity API does not support adding a single role, the list should be the entire list of existing roles for the user plus whatever new roles. See [veracode-user-bulk-role-assign](https://github.com/tjarrettveracode/veracode-user-bulk-role-assign) for an example.
- `update_user(user_guid,changes)`: update a user based upon the provided information.
  - `user_guid`: the unique identifier of the user to be updated.
  - `changes`: the attributes of the user to be changed. Must be JSON whose format follows the [Identity API specification](https://app.swaggerhub.com/apis/Veracode/veracode-identity_api/1.0#/ResourceOfUserResource) of a valid user object.
- `update_user_email_address(user_guid,email_address,ignore_verification(opt))`: updates the email address of the specified user.
  - `ignore_verification`: Boolean. Defaults to `False`. If `True`, immediately updates email address without requiring the user to verify the change via email. If the user has not yet activated the account, this must be set to `True`.
- `send_password_reset(user_legacy_id)`: sends a password reset email to the specified user. If the user has yet to activate their account, sends a new activation email instead.
  - NOTE: this function uses the `user_legacy_id` value (as opposed to the `user_guid` value), which can be obtained via a call to `get_user()`.
- `disable_user(user_guid)`: set the `Active` flag the user identified by `user_guid` to `False`.
- `delete_user(user_guid)`: delete the user identified by `user_guid`. This is not a reversible action.
- `get_roles()`: get a list of available roles to assign to users.

### API Credentials

1. *Accessing*: Calling these methods requires a user with the [Administator, Team Admin,](https://docs.veracode.com/r/c_role_permissions) or [Admin API](https://docs.veracode.com/r/c_API_roles_details) user role.
1. *See also*: You can also access these methods from the [APICredentials class](apicreds.md).

- `get_creds(api_id(opt))`: get credentials information (API ID and expiration date) for the user specified by `api_id`; if `api_id` is `None`, get credentials information for the current user requesting the API call.
- `create_creds(user_guid)`: create or renew API credentials for the API service account specified by `user_guid`.
- `renew_creds()`: renew credentials for the current user. NOTE: you must note the return from this call as the API key cannot be viewed again. Accessible by any user role.
- `revoke_creds(api_id)`: revoke immediately the API credentials identified by `api_id`.

### Business Units

*See also*: You can also access this method from the [BusinessUnits class](businessunits.md).

- `get_business_units()`: get the list of business units in the organization.
- `get_business_unit(guid)`: get the business unit identified by `guid`.
- `create_business_unit(name,teams)`: create a business unit. `teams` is a list of `team_id` GUIDs.
- `update_business_unit(guid,name,teams)`: update the business unit identified by `guid`.
- `delete_business_unit(guid)`: delete the business unit identified by `guid`.

### Teams

*See also*: You can also access this method from the [Teams class](teams.md).

- `get_teams(all_for_org)`: get the list of teams for the user, or (if `all_for_org` is `True`) all teams in the organization.
- `get_team_by_id(team_uuid)`: get the details for a given team uuid, including members
- `create_team(team_name,business_unit,members)`: create a team named `team_name`. Optionally pass the business unit guid and/or a list of user names to add to the team.
- `update_team(team_guid,team_name(opt),business_unit(opt),members(opt))`: update the team identified by `team_guid` with the provided information.
- `delete_team(team_guid)`: delete the team identified by `team_guid`.

## Static 

*See also*: You can also access these methods from the [Static class](static.md).

- `create_static_scan(binary_name, binary_size, binary_hash, app_id(opt), project_name(opt), project_uri(opt), project_ref(opt), commit_hash(opt), dev_stage(opt), scan_timeout (opt))` - Set up a scan
- `get_static_scan(scan_id)` - Get scan details for the scan represented by `scan_id`.
- `add_static_scan_segment(scan_id,segment_id,file)` - Upload a segment of the scanned file.
- `start_static_scan(scan_id)` - Start the scan represented by `scan_id`.
- `cancel_static_scan(scan_id)` - Cancel the scan represented by `scan_id`.
- `get_static_scan_findings(scan_id)` - Get the findings for the scan represented by `scan_id`.

[All docs](docs.md)
