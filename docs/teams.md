# Teams

The following methods call Veracode REST APIs and return JSON.

- `Teams().get_all(all_for_org)`: get the list of teams for the user, or (if `all_for_org` is `True`) all teams in the organization.
- `Teams().get(team_uuid)`: get the details for a given team uuid, including members
- `Teams().create(team_name,business_unit,members)`: create a team named `team_name`. Optionally pass the business unit guid and/or a list of user names to add to the team.
- `Teams().update(team_guid,team_name(opt),business_unit(opt),members(opt))`: update the team identified by `team_guid` with the provided information.
- `Teams().delete(team_guid)`: delete the team identified by `team_guid`.

[All docs](docs.md)
