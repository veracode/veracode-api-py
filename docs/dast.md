# DAST

The following methods call Veracode REST APIs and return JSON.

## Targets

Manage information and settings related to scan targets.

- `DASTTargets().get_all()`: get a list of DAST targets to which you have access.
- `DASTTargets().get(target_id)`: get the DAST target identified by `target_id`.
- `DASTTargets().get_by_name(target_name)`: get a list of DAST targets whose name contains `target_name`.
- `DASTTargets().search(target_name(opt), url(opt), search_term(opt), target_type)`: get a list of DAST targets to which you have access based on the search terms provided:
  - `target_name`: finds targets whose name contains `target_name`
  - `url`: finds targets whose url contains `url`
  - `search_term`: finds targets whose name or URL contains `search_term`
  - `target_type`: use to restrict the search to a `WEB_APP` or an `API`
- `DASTTargets().create(name, description, protocol, url, api_specification_file_url, target_type, scan_type,is_sec_lead_only,teams(opt))`: create a DAST target. Note that this will also create an analysis profile for the target. Arguments include:
  - `name`: the name of the target.
  - `description`: the long description of the target.
  - `protocol`: the protocol of the main URL for the target (`HTTP`, `HTTPS`).
  - `url`: the main URL for the target. Must be specified for `target_type` = `WEB_APP`.
  - `api_specification_file_url`: the API specification URL for the target. Must be specified for `target_type` = `API`. 
  - `target_type`: use to specify that the target is a `WEB_APP` or an `API`.
  - `scan_type`: use to specify the type of scan (`QUICK` or `FULL`).
  - `is_sec_lead_only`: set to `False` if the target should be accessed only by one or more `teams`.
  - `teams` (opt): an array of team GUIDs for whom access to the target should be restricted.
- `DASTTargets().update(target_id, name, description, protocol, url, api_specification_file_url, target_type, scan_type,is_sec_lead_only,teams(opt))`: update the DAST target identified by `target_id`.
- `DASTTargets().delete(target_id)`: delete the DAST target identified by `target_id`.


## Analysis Profiles

Configure analysis options for a scan.

- `DASTAnalysisProfiles().get_all(target_id(opt),type(opt))`: Retrieve the analysis profiles for the account, optionally filtered by `target_id` or `type`.
  - `target_id`: Retrieve the analysis profiles associated with the target identified by `target_id`. Note that this returns an array, though currently DAST Essentials only supports a single analysis profile per target.
  - `type`: One of `TARGET` or `SYSTEM`.
- `DASTAnalysisProfiles().get(analysis_profile_id)`: Retrieve the details for the analysis profile identified by `analysis_profile_id`.
- `DASTAnalysisProfiles().update(self, analysis_profile_id, allowed_urls(opt),denied_urls(opt), seed_urls(opt), grouped_urls(opt), crawler_mode(opt), rate_limit(opt), max_duration(opt), max_crawl_duration(opt))`: Update the analysis profile identified by `analysis_profile_id` with one or more settings:
  - `allowed_urls`: an array of the URLs the scanner is allowed to scan.
  - `denied_urls`: an array of the URLs the scanner is not allowed to scan.
  - `seed_urls`: an array of [seed URLs](https://docs.veracode.com/r/advanced-scan-configuration#seed-urls) that the scanner can use as starting points to crawl the target. Use this to include URLs that are not linked from the application but should be scanned.
  - `grouped_urls`: an array of [grouped URLs](https://docs.veracode.com/r/advanced-scan-configuration#grouped-urls). Define this parameter to improve scanning speed on sites that have a large number of similar pages.
  - `crawler_mode`: one of `SMART`, `EXHAUSTIVE`.
  - `rate_limit`: an integer that limits the number of attacks the crawler makes in an interval.
  - `max_duration`: an integer that specifies the maximum duration for the scan.
  - `max_crawl_duration`: an integer that specifies the maximum duration for crawling the target.
- `DASTAnalysisProfiles().update_parent(analysis_profile_id, parent_analysis_profile_id)`: identifies a new parent analysis profile for the analysis profile identified by `analysis_profile_id`. This allows inheriting analysis profile settings from the parent.
- `DASTAnalysisProfiles().get_authentications(analysis_profile_id)`: Retrieve the authentication options for the analysis profile identified by `analysis_profile_id`.
- `DASTAnalysisProfiles().update_system_auth(analysis_profile_id, username, password)`: Set the username and password used for basic (HTTP) authentication for the analysis profile identified by `analysis_profile_id`.
- `DASTAnalysisProfiles().update_app_auth(analysis_profile_id, username, password, login_url)`: Set the username and password used for application authentication on the login page at `login_url`, for the analysis profile identified by `analysis_profile_id`.
- `DASTAnalysisProfiles().update_parameter_auth(analysis_profile_id, id, title, type, key, value)`: Set the options for paraemeter authentication for the analysis profile identified by `analysis_profile_id`.
- `DASTAnalysisProfiles().get_scanners(analysis_profile_id)`: get the scanners associated with the analysis profile identified by `analysis_profile_id`.
- `DASTAnalysisProfiles().update_scanners(analysis_profile_id, scanner_id, scanner_value)`: For the analysis profile identified by `analysis_profile_id`, enable or disable the scanner identified by `scanner_id`. Allowed values include: [ 'fingerprinting', 'ssl', 'http_header', 'portscan', 'fuzzer', 'sql_injection', 'xss', 'file_inclusion', 'deserialization', 'xxe', 'command_injection', 'csrf', 'ldap_injection']
- `DASTAnalysisProfiles().get_schedules(analysis_profile_id)`: Get the schedules associated with the application profile identified by `analysis_profile_id`.  
- `DASTAnalysisProfiles().get_schedule(analysis_profile_id, schedule_id)`: Get the schedule identified by `schedule_id` and associated with the application profile identified by `analysis_profile_id`.
- `DASTAnalysisProfiles().create_schedule(analysis_profile_id, frequency, day=1, weekday=1, timezone='America/New York',time="00:00"))`: Create a schedule for the application profile identified by `analysis_profile_id`. Options include:
  - `frequency`: one of [`daily`, `weekly`, `monthly`]
  - `day`: integer identifying the day of the month to perform a scan with monthly frequency
  - `weekday`: integer identifying the day of the week to perform a scan with weekly frequency
  - `timezone`: time zone identifier for scheduling the scan
  - `time`: timestamp at which to start the scan
- `DASTAnalysisProfiles().update_schedule(analysis_profile_id, schedule_id, frequency, day=1, weekday=1, timezone='America/New York',time="00:00"))`: Update the schedule identified by `schedule_id` for the application profile identified by `analysis_profile_id`.
- `DASTAnalysisProfiles().delete_schedule(analysis_profile_id, schedule_id))`: Delete the schedule identified by `schedule_id` for the application profile identified by `analysis_profile_id`. 

## Analysis Runs

Begin or check the status of an analysis run.

- `DASTAnalysisRuns().start(target_id)`: start an analysis run for the target identified by `target_id`.
- `DASTAnalysisRuns().get(target_id)`: get the PDF report for the target identified by `target_id`. Returns a 400 if the scanning report is not ready. Save the response to a file to use.

[All docs](docs.md)
