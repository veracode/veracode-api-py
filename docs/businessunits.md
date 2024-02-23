# Business Units

The following methods call Veracode REST APIs and return JSON.

- `BusinessUnits().get_all()`: get the list of business units in the organization.
- `BusinessUnits().get(guid)`: get the business unit identified by `guid`.
- `BusinessUnits().create(name,teams)`: create a business unit. `teams` is a list of `team_id` GUIDs.
- `BusinessUnits().update(guid,name,teams)`: update the business unit identified by `guid`.
- `BusinessUnits().delete(guid)`: delete the business unit identified by `guid`.

[All docs](docs.md)
