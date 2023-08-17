# XML APIs

The following methods call Veracode XML APIs and return XML output. For a more detailed reference on the underlying API calls, see the [Veracode docs](https://docs.veracode.com/r/c_api_main).

_Note_: You can also access these methods from the `XMLAPI` class.

- `get_app_list()` : get a list of Veracode applications (XML format)
- `get_app_info(app_id)` : get application info for the `app_id` (integer) passed.
- `get_sandbox_list(app_id)` : get list of sandboxes for the `app_id` (integer) passed.
- `get_build_list(app_id, sandbox_id(opt))`: get list of builds for the `app_id` (integer) passed. If `sandbox_id` (integer) passed, returns a list of builds in the sandbox.
- `get_build_info(app_id, build_id, sandbox_id(opt))`: get build info for the `build_id` (integer) and `app_id` (integer) passed. If `sandbox_id` (integer) passed, returns information for the `build_id` in the sandbox.
- `get_detailed_report(build_id)`: get detailed report XML for the `build_id` (integer) passed.
- `set_mitigation_info(build_id,flaw_id_list,action,comment)`: create a mitigation of type `action` with comment `comment` for the flaws in `flaw_id_list` (comma separated list of integers) of build `build_id` (integer). Supported values for `action`: 'Mitigate by Design', 'Mitigate by Network Environment',  'Mitigate by OS Environment', 'Approve Mitigation', 'Reject Mitigation', 'Potential False Positive',  'Reported to Library Maintainer'. Any other value passed to `action` is interpreted as a comment.
- `generate_archer(payload)`: generate an Archer report based on the comma separated list of parameters provided. Possible parameters include `period` (`yesterday`, `last_week`, `last_month`; all time if omitted), `from_date` (mm-dd-yyyy format), `to_date` (mm-dd-yyyy format), `scan_type` (one of `static`, `dynamic`, `manual`). Returns a payload that contains a token to download an Archer report.
- `download_archer(token(opt))`: get Archer report corresponding to the token passed. If no token passed, retrieves the latest Archer report generated.
- `upload_file(app_id, file, sandbox_id(opt), save_as(opt))`: Uploads a file to an existing build or creates a build.
- `begin_prescan(app_id, sandbox_id(opt), auto_scan(opt), scan_all_nonfatal_top_level_modules(opt)`: begin a static prescan on the application and/or sandbox specified.
- `begin_scan(app_id, modules(opt), scan_all_top_level_modules(opt),scan_selected_modules(opt),scan_previously_selected_modules(opt),sandbox_id(opt))`: begin a static scan on the application and/or sandbox specified.
- `get_prescan_results(app_id, build_id(opt), sandbox_id(opt))`: get the prescan results for the application, sandbox and/or scan specified.
- `get_file_list(app_id, build_id(opt), sandbox_id(opt))`: get the list of files uploaded for the application, sandbox, and/or scan specified.
- `remove_file(app_id, file_id, sandbox_id(opt))`: delete a file previously uploaded for the application and/or sandbox specified.
- `delete_build(app_id, sandbox_id(opt))`: delete the last build uploaded for the application and/or sandbox specified.
[All docs](docs.md)
