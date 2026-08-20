# Custom PDF

The following methods call Veracode REST APIs and return JSON.

- `CustomPDF().create_report(app_id(int), scan_types (list), executive_summary (opt), policy_evaluation(opt), findings_impacting_policy(opt), findings_severity_level(opt), findings_details(opt), flaw_category_details(opt), findings_summary(opt), changes_from_last_scan(opt), sca_vulnerability_details(opt), static_scan_details(opt), dynamic_scan_details(opt), penetration_test_summary(opt), proposed_mitigated_findings(opt), approved_mitigated_findings(opt), rejected_mitigated_findings(opt), sca_standalone(opt), veracode_methodology(opt))`: set up a request for a report. By default this command returns the GUID of the report request; specify `rawjson=True` to get the full response. Options include:
  - `app_id`: int
  - `scan_types`: list. One or more of `"Static"`, `"Dynamic"`, `"SCA"`, `"Manual"`
  - `executive_summary` (bool): Include the Executive Summary report page
  - `policy_evaluation` (bool): Include the Policy Evaluation page
  - `findings_impacting_policy` (bool): Include only the findings impacting policy or include all findings
  - `findings_severity_level`: The minimum findings severity level to include. One of `all`, `very_high`, `high`, `medium`, `low`, `very_low`
  - `findings_details` (bool): Include the details for each included finding.
  - `flaw_category_details` (bool): Include the information about Veracode flaw categories in the report
  - `findings_summary` (bool): Include the summary list of findings
  - `changes_from_last_scan` (bool): Include the details of changes in scan configuration between the last scan and the scans included in the report
  - `sca_vulnerability_details` (bool): Include details for SCA findings
  - `static_scan_details` (bool): Include details of the static scan configuration
  - `dynamic_scan_details` (bool): Include details of the dynamic scan configuration
  - `penetration_test_summary` (bool): Include summary information about the manual penetration test
  - `proposed_mitigated_findings` (bool): Include table listing findings with proposed (not approved) mitigations 
  - `approved_mitigated_findings` (bool): Include table listing findings with approved mitigations
  - `rejected_mitigated_findings` (bool): Include table listing findings with rejected mitigations  
  - `sca_standalone` (bool): Generate a report containing only SCA findings
  - `veracode_methodology` (bool): Include the Veracode methodology document in the generated report

- `CustomPDF().get(guid)`: check the status of the report request and return the report contents when ready. Note that this method returns a tuple of `status` (string) and `downloadUrl` (URL); when `status` is `COMPLETE`, the `results` argument will populate with a URL that can be used to fetch the PDF contents to be written to a file.

[All docs](docs.md)
