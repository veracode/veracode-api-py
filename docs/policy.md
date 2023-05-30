# Policy

The following methods call Veracode REST APIs and return JSON.

_Note_: You can also access these methods from the `Policies` class.

- `get_policies`: Get a list of available policies.
- `get_policy(guid)`: get information for the policy corresponding to `guid`.
- `create_policy(name,description,vendor_policy(opt),finding_rules(opt),scan_frequency_rules(opt),grace_period_rules(opt))`: create a policy
- `edit_policy(guid,name,description,vendor_policy(opt),finding_rules(opt),scan_frequency_rules(opt),grace_period_rules(opt))`: edit a policy
- `delete_policy(guid)`: delete a policy

[All docs](docs.md)
