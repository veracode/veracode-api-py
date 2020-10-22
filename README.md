# Veracode API Python

Python helper library for working with the Veracode APIs. Handles retries, pagination, and other features of the modern Veracode REST APIs.

Not an official Veracode product. Heavily based on original work by [CTCampbell](https://github.com/ctcampbell).

## Setup

Install from pypi:

    pypi veracode_api_py

(Optional) Save Veracode API credentials in `~/.veracode/credentials`

    [default]
    veracode_api_key_id = <YOUR_API_KEY_ID>
    veracode_api_key_secret = <YOUR_API_KEY_SECRET>

## Use in your applications

Import VeracodeAPI into your code and call the methods. Most methods return JSON or XML depending on the underlying API.

### VeracodeAPI

The following methods call Veracode XML APIs and return XML output.

- `get_app_list()` : get a list of Veracode applications (XML format)
- `get_app_info(app_id)` : get application info for the `app_id` (integer) passed.
- `get_sandbox_list(app_id)` : get list of sandboxes for the `app_id` (integer) passed.
- `get_build_list(app_id, sandbox_id(opt))`: get list of builds for the `app_id` (integer) passed. If `sandbox_id` (integer) passed, returns a list of builds in the sandbox.
- `get_build_info(app_id, build_id, sandbox_id(opt))`: get build info for the `build_id` (integer) and `app_id` (integer) passed. If `sandbox_id` (integer) passed, returns information for the `build_id` in the sandbox.
- `get_detailed_report(build_id)`: get detailed report XML for the `build_id` (integer) passed.
- `set_mitigation_info(build_id,flaw_id_list,action,comment)`: create a mitigation of type `action` with comment `comment` for the flaws in `flaw_id_list` (comma separated list of integers) of build `build_id` (integer). Supported values for `action`: 'Mitigate by Design', 'Mitigate by Network Environment',  'Mitigate by OS Environment', 'Approve Mitigation', 'Reject Mitigation', 'Potential False Positive',  'Reported to Library Maintainer'. Any other value passed to `action` is interpreted as a comment.
- `generate_archer(payload)`: generate an Archer report based on the comma separated list of parameters provided. Possible parameters include `period` (`yesterday`, `last_week`, `last_month`; all time if omitted), `from_date` (mm-dd-yyyy format), `to_date` (mm-dd-yyyy format), `scan_type` (one of `static`, `dynamic`, `manual`). Returns a payload that contains a token to download an Archer report.
- `download_archer(token(opt))`: get Archer report corresponding to the token passed. If no token passed, retrieves the latest Archer report generated.

The following methods call Veracode REST APIs and return JSON.

- `get_apps()` : get a list of Veracode applications (JSON format).
- `get_app(guid(opt),legacy_id(opt))`: get information for a single Veracode application using either the `guid` or the `legacy_id` (integer).
- `get_policy(guid)`: get information for the policy corresponding to `guid`.
- `get_findings(app,scantype(opt),annot(opt))`: get the findings for `app` (guid).
  - `scantype`: Defaults to STATIC findings, but can be STATIC, DYNAMIC, MANUAL, SCA, or ALL (static, dynamic, manual).
  - `annot`: Defaults to TRUE but can be FALSE
- `get_users()`: get a list of users for the organization.
- `get_user_self()`: get user information for the current user.
- `get_user(user_guid)`: get information for an individual user based on `user_guid`.
- `get_user_by_name(username)`: look up info for an individual user based on their user_name.
- `get_creds()`: get credentials information (API ID and expiration date) for the current user.
- `update_user(user_guid, roles)`: update the user identified by `user_guid` with the list of roles passed in `roles`. Because the Identity API does not support adding a single role, the list should be the entire list of existing roles for the user plus whatever new roles. See [veracode-user-bulk-role-assign](https://github.com/tjarrettveracode/veracode-user-bulk-role-assign) for an example.
- `disable_user(user_guid)`: set the `Active` flag the user identified by `user_guid` to `False`.
- `get_workspaces()`: get a list of SCA Agent workspaces for the organization.
- `get_workspace_by_name(name)`: get a list of SCA Agent workspaces whose name partially matches `name`.
- `create_workspace(name)`: create an SCA Agent workspace named `name`. Returns the GUID for the workspace.
- `add_workspace_team(workspace_guid,team_id)`: add the team identified by `team_id` (int) to the workspace identified by `workspace_guid`.
- `delete_workspace(workspace_guid)`: delete the workspace identified by `workspace_guid`.

## Notes

1. Different API calls require different roles. Consult the [Veracode Help Center](https://help.veracode.com/go/c_role_permissions).
2. SCA APIs must be called with a human user.
3. This library does not include a complete set of Veracode API methods.
4. Contributions are welcome.
