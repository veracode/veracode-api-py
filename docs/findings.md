# Findings, Annotations, and Summary Reports

The following methods call Veracode REST APIs and return JSON.

## Findings and Annotations

- `Findings().get_findings(app,scantype(opt),annot(opt),request_params(opt),sandbox(opt))`: get the findings for `app` (guid).
  - `scantype`: Defaults to STATIC findings, but can be STATIC, DYNAMIC, MANUAL, SCA, or ALL (static, dynamic, manual).
  - `annot`: Defaults to TRUE but can be FALSE
  - `sandbox`: The guid of the sandbox in `app` for which you want findings. (Use the Sandboxes APIs to get the sandbox guid.)
  - `request_params`: Dictionary of additional query parameters. See the full [Findings API specification](https://help.veracode.com/r/c_findings_v2_intro) for some of the other options available.
- `Findings().get_static_flaw_info(app,issueid,sandbox(opt))`: get the static flaw information, including data paths, for the finding identified by `issueid` in `app` (guid) or its `sandbox` (guid).
- `Findings().get_dynamic_flaw_info(app,issueid)`: get the dynamic flaw information, including request/response data, for the finding identified by `issueid` in `app` (guid).
- `Findings().add_annotation(app,issue_list,comment,action,sandbox(opt))`: add an annotation (comment, mitigation proposal/acceptance/rejection) to the findings in `issue_list` for `app` (guid) (or optionally `sandbox` (guid)). Note that you must have the Mitigation Approver role (regular user) to use the ACCEPTED or REJECTED action, or the Mitigation and Comments API role for an API service account to use this call.
  - `issue_list`: must be passed as a Python list of `issue_id`s
  - `action`: must be one of COMMENT, POTENTIAL_FALSE_POSITIVE, APP_BY_DESIGN, OS_ENV, NET_ENV, LIBRARY, ACCEPT_RISK, ACCEPTED, REJECTED
- `Findings().match_findings(origin_finding,potential_matches,approved_findings_only(opt),allow_fuzzy_match(opt))`: return a matching finding from `potential_matches` for the `origin_finding`, based on the finding type.
  - `approved_findings_only`: limits matches to findings with approved mitigations.
  - `allow_fuzzy_match`: look for matches within a range of source lines around the origin finding. This allows for code movement but can result in flaws being mismatched; use sparingly.

## Summary Report

- `SummaryReport().get_summary_report(app,sandbox(opt))`: get the summary report for `app` (guid) or its `sandbox` (guid).

## Manual Testing

- `ManualScans().get_for_app(appid)`: get the manual scans for `appid` (guid).
- `ManualScans().get(scanid)`: get the manual scan information for `scanid` (int), returned by `get_for_app()`.
- `ManualScans().get_findings(scanid,include_artifacts(opt))`: get the manual findings detail for `scanid` (int). 
  - `include_artifacts`: if `True`, includes screenshots and code samples associated with the findings. 

[All docs](docs.md)
