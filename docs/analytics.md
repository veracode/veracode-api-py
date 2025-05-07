# Analytics

The following methods call Veracode REST APIs and return JSON.

**Notes**:

1. The Reporting API is available to Veracode customers by request. More information about the API is available in the [Veracode Docs](https://docs.veracode.com/r/Reporting_REST_API).

- `Analytics().create_report(report_type ('findings'),last_updated_start_date(opt), last_updated_end_date (opt), scan_type (opt), finding_status(opt), passed_policy(opt), policy_sandbox(opt), application_id(opt), rawjson(opt), deletion_start_date(opt), deletion_end_date(opt), start_date(opt), end_date(opt), audit_action(opt), target_user_id(opt), modifier_user_id(opt))`: set up a request for a report. By default this command returns the GUID of the report request; specify `rawjson=True` to get the full response. Dates should be specified as `YYYY-MM-DD HH:MM:SS` with the timestamp optional. Options include:
  - `report_type`: required, currently supports `findings`, `scans`, `deletedscans`, and `audit`.
  - `last_updated_start_date`: required for `findings` report type, beginning of date range for new or changed findings or scans
  - `last_updated_end_date`: optional, end of date range for new or changed findings or scans
  - `scan_type`: optional, one or more of 'Static Analysis', 'Dynamic Analysis', 'Manual', 'Software Composition Analysis', 'SCA'. `SCA` is only supported for the `findings` report type.
  - `finding_status`: optional, 'Open' or 'Closed'. Applies only to the `findings` report.
  - `passed_policy`: optional, boolean. Applies only to the `findings` report.
  - `policy_sandbox`: optional, 'Policy' or 'Sandbox'
  - `application_id`: optional, application ID for which to return results
  - `rawjson`: optional, defaults to False. Returns full response if True, the GUID of the request if false
  - `deletion_start_date`: required for `deletedscans` report type, beginning of date range for deleted scans.
  - `deletion_end_date`: optional, end of date range for deleted scans.
  - `sandbox_ids`: optional, array of sandbox IDs (integers) for which to return results
  - `start_date`: required for `audit` report type, beginning of date range for audit events
  - `end_date`: optional for `audit` report type, end of date range for audit events
  - `audit_action`: optional for `audit` report type. An array of audit actions to include in the report. Examples include `Login`, `Login Account`, `Auth`, `Create`, `Delete`, `Update`
  - `target_user_id`: optional for `audit` report type. The numeric user id of the user for which you want to retrieve audit events that happened to the user.
  - `modifier_user_id`: optional for `audit` report type. The numeric user id of the user for which you want to retrieve audit events that were caused by the user.

- `Analytics().create_findings_report(last_updated_start_date(opt), last_updated_end_date (opt), scan_type (opt), finding_status(opt), passed_policy(opt), policy_sandbox(opt), application_id(opt), rawjson(opt))`: set up a request for a findings report. By default this command returns the GUID of the report request; specify `rawjson=True` to get the full response. Dates should be specified as `YYYY-MM-DD HH:MM:SS` with the timestamp optional. Options include:
  - `start_date`: required, beginning of date range for findings
  - `end_date`: optional, end of date range for findings
   - `scan_type`: optional, one or more of 'Static Analysis', 'Dynamic Analysis', 'Manual', 'Software Composition Analysis', 'SCA'.
  - `finding_status`: optional, 'Open' or 'Closed'. Applies only to the `findings` report.
  - `passed_policy`: optional, boolean. Applies only to the `findings` report.
  - `policy_sandbox`: optional, 'Policy' or 'Sandbox'
  - `application_id`: optional. The numeric application id of an application whose findings you want to include in the report.
  - `rawjson`: optional, defaults to False. Returns full response if True, the GUID of the request if false

- `Analytics().create_scans_report(start_date, end_date(opt), scan_type(opt), policy_sandbox(opt), application_id(opt), rawjson(opt))`: set up a request for a scans report. By default this command returns the GUID of the report request; specify `rawjson=True` to get the full response. Dates should be specified as `YYYY-MM-DD HH:MM:SS` with the timestamp optional. Options include:
  - `start_date`: required, beginning of date range for scans
  - `end_date`: optional, end of date range for scans
  - `scan_type`: optional, one or more of 'Static Analysis', 'Dynamic Analysis', 'Manual'.
  - `policy_sandbox`: optional, 'Policy' or 'Sandbox'
  - `application_id`: optional. The numeric application id of an application whose scans you want to include in the report.
  - `rawjson`: optional, defaults to False. Returns full response if True, the GUID of the request if false

- `Analytics().create_deleted_scans_report(start_date, end_date(opt), application_id(opt),rawjson(opt))`: set up a request for a deleted scans report. By default this command returns the GUID of the report request; specify `rawjson=True` to get the full response. Dates should be specified as `YYYY-MM-DD HH:MM:SS` with the timestamp optional. Options include:
  - `start_date`: required, beginning of date range for deleted scans
  - `end_date`: optional, end of date range for deleted scans
  - `application_id`: optional. The numeric application id of an application whose deleted scans you want to include in the report.
  - `rawjson`: optional, defaults to False. Returns full response if True, the GUID of the request if false

- `Analytics().create_audit_report(start_date, end_date(opt), audit_action(opt), target_user_id(opt),                         modifier_user_id(opt),rawjson(opt))`: set up a request for an audit log report. By default this command returns the GUID of the report request; specify `rawjson=True` to get the full response. Dates should be specified as `YYYY-MM-DD HH:MM:SS` with the timestamp optional. Options include:
  - `start_date`: required, beginning of date range for audit events
  - `end_date`: optional, end of date range for audit events
  - `audit_action`: optional. An array of audit actions to include in the report. Examples include `Success`, `Logged out`, `Create`, `Delete`, `Update`
  - `target_user_id`: optional. The numeric user id of the user for which you want to retrieve audit events that happened to the user.
  - `modifier_user_id`: optional. The numeric user id of the user for which you want to retrieve audit events that were caused by the user.
  - `rawjson`: optional, defaults to False. Returns full response if True, the GUID of the request if false

- `Analytics().get(guid, report_type(findings))`: check the status of the report request and return the report contents when ready. Note that this method returns a tuple of `status` (string) and `results` (list); when `status` is `COMPLETED`, the `results` list will populate with results. Also, you need to specify the type of data expected by the GUID with `report_type`; this defaults to `findings`.

- `Analytics().get_findings(guid)`: check the status of a findings report request specified by `guid` and return the report contents when ready. Note that this method returns a tuple of `status` (string) and `results` (list); when `status` is `COMPLETED`, the `results` list will populate with results. 

- `Analytics().get_scans(guid)`: check the status of a scans report request specified by `guid` and return the report contents when ready. Note that this method returns a tuple of `status` (string) and `results` (list); when `status` is `COMPLETED`, the `results` list will populate with results. 

- `Analytics().get_deletedscans(guid)`: check the status of a deleted scans report request specified by `guid` and return the report contents when ready. Note that this method returns a tuple of `status` (string) and `results` (list); when `status` is `COMPLETED`, the `results` list will populate with results. 

[All docs](docs.md)
