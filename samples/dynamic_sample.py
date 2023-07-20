from veracode_api_py.dynamic import Analyses, Scans, ScanCapacitySummary, ScanOccurrences, ScannerVariables, DynUtils, Occurrences

url = DynUtils().setup_url('http://www.example.com','DIRECTORY_AND_SUBDIRECTORY',False)

allowed_hosts = [url]

auth = DynUtils().setup_auth('AUTO','admin','smithy')

auth_config = DynUtils().setup_auth_config(auth)

crawl_config = DynUtils().setup_crawl_configuration([],False)

scan_setting = DynUtils().setup_scan_setting(blocklist_configs=[],custom_hosts=[],user_agent=None)

scan_config_request = DynUtils().setup_scan_config_request(url, allowed_hosts,auth_config, crawl_config, scan_setting)

scan_contact_info = DynUtils().setup_scan_contact_info('tjarrett@example.com','Alan Smithee','800-555-1212')

scan = DynUtils().setup_scan(scan_config_request,scan_contact_info)

start_scan = DynUtils().start_scan(12, "HOUR")

print(scan)

analysis = Analyses().create('My API Analysis 4',scans=[scan],owner='Tim Jarrett',email='tjarrett@example.com', start_scan=start_scan)

print(analysis)