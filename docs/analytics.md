# Analytics

The following methods call Veracode REST APIs and return JSON.

**Notes**:

1. The Reporting API is available only to Veracode customers in the Reporting API Early Adopter program. As the Reporting API is not generally available yet, the functionality of the feature will change over time.
1. You can also access these methods from the `Analytics` class.

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

[All docs](docs.md)
