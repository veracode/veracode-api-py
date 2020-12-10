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

#### Applications

- `get_apps()` : get a list of Veracode applications (JSON format).
- `get_app(guid(opt),legacy_id(opt))`: get information for a single Veracode application using either the `guid` or the `legacy_id` (integer).
- `get_app_by_name(name)`: get list of applications whose names contain the search string `name`.
- `create_app(app_name, business_criticality, business_unit(opt), teams(opt))`: create an application profile.
  - `business_criticality`: one of "VERY HIGH", "HIGH", "MEDIUM", "LOW", "VERY LOW"
  - `business_unit`: the GUID of the business unit to which the application should be assigned
  - `teams`: a list of the GUIDs of the teams to which the application should be assigned
- `delete_app(guid)`: delete the application identified by `guid`. This is not a reversible action.

#### Sandboxes

- `get_app_sandboxes(guid)`: get the sandboxes associated with the application identified by `guid`.
- `create_sandbox(app,name,auto_recreate(opt),custom_fields(opt))`: create a sandbox in the application identified by `app`. Custom fields must be specified as a list of dictionaries of `name`/`value` pairs, e.g. [{'name': 'Custom 1','value': 'foo'}].
- `update_sandbox(app,sandbox,name,auto_recreate(opt),custom_fields(opt))`: update the `sandbox` (guid) in `app` (guid) with the provided values. Note that partial updates are NOT supported, so you need to provide all values including those you don't wish to change.
- `delete_sandbox(app,sandbox)`: delete `sandbox` (guid) in `app` (guid).

#### Policy

- `get_policy(guid)`: get information for the policy corresponding to `guid`.

#### Findings

- `get_findings(app,scantype(opt),annot(opt))`: get the findings for `app` (guid).
  - `scantype`: Defaults to STATIC findings, but can be STATIC, DYNAMIC, MANUAL, SCA, or ALL (static, dynamic, manual).
  - `annot`: Defaults to TRUE but can be FALSE
- `get_summary_report(app,sandbox(opt))`: get the summary report for `app` (guid) or its `sandbox` (guid).
- `get_static_flaw_info(app,issueid,sandbox(opt))`: get the static flaw information, including data paths, for the finding identified by `issueid` in `app` (guid) or its `sandbox` (guid).
- `get_dynamic_flaw_info(app,issueid)`: get the dynamic flaw information, including request/response data, for the finding identified by `issueid` in `app` (guid).
- `add_annotation(app,issue_list,comment,action)`: add an annotation (comment, mitigation proposal/acceptance/rejection) to the findings in `issue_list` for `app` (guid). Note that you must have the Mitigation Approver role (regular user) to use the ACCEPTED or REJECTED action, or the Mitigation and Comments API role for an API service account to use this call.
  - `issue_list`: must be passed as a Python list of `issue_id`s
  - `action`: must be one of COMMENT, POTENTIAL_FALSE_POSITIVE, APP_BY_DESIGN, OS_ENV, NET_ENV, LIBRARY, ACCEPT_RISK, ACCEPTED, REJECTED

#### Users

- `get_users()`: get a list of users for the organization.
- `get_user_self()`: get user information for the current user.
- `get_user(user_guid)`: get information for an individual user based on `user_guid`.
- `get_user_by_name(username)`: look up info for an individual user based on their user_name.
- `get_creds()`: get credentials information (API ID and expiration date) for the current user.
- `create_user(email,firstname,lastname,type(opt),username(opt),roles(opt))`: create a user based on the provided information.
  - `type`: `"HUMAN"` or `"API"`. Defaults to `"HUMAN"`. If `"API"` specified, must also provide `username`.
  - `roles`: list of role names (specified in the Veracode Help Center, for both [human](https://help.veracode.com/go/c_identity_create_human) and [API service account](https://help.veracode.com/go/c_identity_create_api) users).
- `update_user(user_guid, roles)`: update the user identified by `user_guid` with the list of roles passed in `roles`. Because the Identity API does not support adding a single role, the list should be the entire list of existing roles for the user plus whatever new roles. See [veracode-user-bulk-role-assign](https://github.com/tjarrettveracode/veracode-user-bulk-role-assign) for an example.
- `disable_user(user_guid)`: set the `Active` flag the user identified by `user_guid` to `False`.
- `delete_user(user_guid)`: delete the user identified by `user_guid`. This is not a reversible action.

#### Teams

- `get_teams(all_for_org)`: get the list of teams for the user, or (if `all_for_org` is `True`) all teams in the organization.
- `create_team(team_name,business_unit,members)`: create a team named `team_name`. Optionally pass the business unit guid and/or a list of user names to add to the team.
- `update_team(team_guid,team_name(opt),business_unit(opt),members(opt))`: update the team identified by `team_guid` with the provided information.
- `delete_team(team_guid)`: delete the team identified by `team_guid`.

#### Business Units

- `get_business_units()`: get the list of business units in the organization.

#### SCA Agent

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
