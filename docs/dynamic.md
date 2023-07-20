# Dynamic Analysis

The following methods call Veracode REST APIs and return JSON.

## Analyses

_Note_: You can also access these methods from the `Analyses` class.

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

## Scans

_Note_: You can also access these methods from the `Scans` class.

- `get_dyn_scan(scan_guid)`: get the scan identified by `scan_guid`. Get `scan_guid` from `get_analysis_scans()`.
- `get_dyn_scan_audits(scan_guid)`: get the audits for the scan identified by `scan_guid`.
- `get_dyn_scan_config(scan_guid)`: get the scan config for the scan identified by `scan_guid`.
- `update_dyn_scan(scan_guid,scan)`: update the scan identified by `scan_guid`. Prepare `scan` with `dyn_setup_scan()`.
- `delete_dyn_scan(scan_guid)`: delete the scan identified by `scan_guid`.
- `get_scan_scanner_variables(scan_id)`: get the scanner variables for the scan identified by `scan_guid`.
- `update_scan_scanner_variable(scan_guid,scanner_variable_guid,reference_key,value,description)`: update the scanner variable identified by the `scanner_variable_guid` for the scan identified by `scan_guid`.
- `delete_scan_scanner_variable(scan_guid,scanner_variable_guid)`: delete the scanner variable identified by the `scanner_variable_guid` for the scan identified by `scan_guid`.

_Note_: You can also access these methods from the `Occurrences` class.

- `get_analysis_occurrences()`: get all dynamic analysis occurrences.
- `get_analysis_occurrence(occurrence_guid)`: get the dynamic analysis occurrence identified by `occurrence_guid`.
- `stop_analysis_occurrence(occurrence_guid,save_or_delete)`: stop the dynamic analysis occurrence identified by `occurrence_guid`. Analysis results identified so far are processed according to `save_or_delete`.

_Note_: You can also access these methods from the `ScanOccurrences` class.

- `get_scan_occurrences(occurrence_guid)`: get the scan occurrences for the dynamic analysis occurrence identified by `occurrence_guid`.
- `get_scan_occurrence(scan_occ_guid)`: get the scan occurrence identified by `scan_occ_guid`.
- `stop_scan_occurrence(scan_occ_guid,save_or_delete)`: stop the scan occurrence identified by `scan_occ_guid`. Scan results identified so far are processed according to `save_or_delete`.
- `get_scan_occurrence_configuration(scan_occ_guid)`: get the configuration of the scan occurrence identified by `scan_occ_guid`.
- `get_scan_occurrence_verification_report(scan_occ_guid)`: get the verification report of the scan occurrence identified by `scan_occ_guid`.
- `get_scan_occurrence_notes_report(scan_occ_guid)`: get the scan notes report of the scan occurrence identified by `scan_occ_guid`.
- `get_scan_occurrence_screenshots(scan_occ_guid)`: get the screenshots of the scan occurrence identified by `scan_occ_guid`.

## Global settings

_Note_: You can also access these methods from the `CodeGroups` class.

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

## Utilities

_Note_: You can also access these methods from the `DynUtils` class.

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

[All docs](docs.md)
