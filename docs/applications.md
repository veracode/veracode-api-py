# Applications and Sandboxes

The following methods call Veracode REST APIs and return JSON.

## Applications

- `Applications().get_all(policy_check_after(opt))` : get a list of Veracode applications (JSON format). If provided, returns only applications that have a policy check date on or after `policy_check_after` (format is `yyyy-mm-dd`).
- `Applications().get(guid(opt),legacy_id(opt))`: get information for a single Veracode application using either the `guid` or the `legacy_id` (integer).
- `Applications().get_by_name(name)`: get list of applications whose names contain the search string `name`.
- `Applications().create(app_name, business_criticality, business_unit(opt), teams(opt), policy_guid(opt), custom_fields(opt array), bus_owner_name(opt), bus_owner_email(opt),git_repo_url(opt))`: create an application profile.
  - `business_criticality`: one of "VERY HIGH", "HIGH", "MEDIUM", "LOW", "VERY LOW"
  - `business_unit`: the GUID of the business unit to which the application should be assigned
  - `teams`: a list of the GUIDs of the teams to which the application should be assigned
  - `policy_guid`: the GUID of the policy to set for this application.
  - `custom_fields`: an array of custom field values for the application
  - `bus_owner_name`: the name of the business owner of the application
  - `bus_owner_email`: the email address of the business owner of the application
  - `git_repo_url`: the URL to the git repository containing the code for the application
- `Applications().update(guid, app_name, business_criticality, business_unit(opt), teams(opt), policy_guid(opt), custom_fields(opt array), bus_owner_name(opt), bus_owner_email(opt),git_repo_url(opt))`: update an application profile. Note that partial updates are NOT supported, so you need to provide all values including those that aren't changing.
- `Applications().delete(guid)`: delete the application identified by `guid`. This is not a reversible action.

## Custom Fields
- `CustomFields().get_all()`: get a list of app profile custom fields available for your organization.

## Sandboxes

- `Sandboxes().get_all(guid)`: get the sandboxes associated with the application identified by `guid`.
- `Sandboxes().create(app,name,auto_recreate(opt),custom_fields(opt))`: create a sandbox in the application identified by `app`. Custom fields must be specified as a list of dictionaries of `name`/`value` pairs, e.g. [{'name': 'Custom 1','value': 'foo'}].
- `Sandboxes().update(app,sandbox,name,auto_recreate(opt),custom_fields(opt))`: update the `sandbox` (guid) in `app` (guid) with the provided values. Note that partial updates are NOT supported, so you need to provide all values including those you don't wish to change.
- `Sandboxes().delete(app,sandbox)`: delete `sandbox` (guid) in `app` (guid).

[All docs](docs.md)
