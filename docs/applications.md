# Applications and Sandboxes

The following methods call Veracode REST APIs and return JSON.

## Applications

_Note_: You can also access these methods from the `Applications` class.

- `get_apps(policy_check_after(opt))` : get a list of Veracode applications (JSON format). If provided, returns only applications that have a policy check date on or after `policy_check_after` (format is `yyyy-mm-dd`).
- `get_app(guid(opt),legacy_id(opt))`: get information for a single Veracode application using either the `guid` or the `legacy_id` (integer).
- `get_app_by_name(name)`: get list of applications whose names contain the search string `name`.
- `create_app(app_name, business_criticality, business_unit(opt), teams(opt), policy_guid(opt), custom_fields(opt array))`: create an application profile.
  - `business_criticality`: one of "VERY HIGH", "HIGH", "MEDIUM", "LOW", "VERY LOW"
  - `business_unit`: the GUID of the business unit to which the application should be assigned
  - `teams`: a list of the GUIDs of the teams to which the application should be assigned
  - `policy_guid`: the GUID of the policy to set for this application.
  - `custom_fields`: an array of custom field values for the application
- `update_app(guid, app_name, business_criticality, business_unit(opt), teams(opt), policy_guid(opt), custom_fields(opt array))`: update an application profile. Note that partial updates are NOT supported, so you need to provide all values including those that aren't changing.
- `delete_app(guid)`: delete the application identified by `guid`. This is not a reversible action.
- `get_custom_fields()`: get a list of app profile custom fields available for your organization.
  - `policy_guid` The GUID of the policy to set for this application.

## Sandboxes

_Note_: You can also access these methods from the `Sandboxes` class.

- `get_app_sandboxes(guid)`: get the sandboxes associated with the application identified by `guid`.
- `create_sandbox(app,name,auto_recreate(opt),custom_fields(opt))`: create a sandbox in the application identified by `app`. Custom fields must be specified as a list of dictionaries of `name`/`value` pairs, e.g. [{'name': 'Custom 1','value': 'foo'}].
- `update_sandbox(app,sandbox,name,auto_recreate(opt),custom_fields(opt))`: update the `sandbox` (guid) in `app` (guid) with the provided values. Note that partial updates are NOT supported, so you need to provide all values including those you don't wish to change.
- `delete_sandbox(app,sandbox)`: delete `sandbox` (guid) in `app` (guid).

[All docs](docs.md)
