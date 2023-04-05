# Business Units

The following methods call Veracode REST APIs and return JSON.

_Note_: You can also access this method from the `BusinessUnits` class.

- `get_business_units()`: get the list of business units in the organization.
- `get_business_unit(guid)`: get the business unit identified by `guid`.
- `create_business_unit(name,teams)`: create a business unit. `teams` is a list of `team_id` GUIDs.
- `update_business_unit(guid,name,teams)`: update the business unit identified by `guid`.
- `delete_business_unit(guid)`: delete the business unit identified by `guid`.

[All docs](docs.md)
