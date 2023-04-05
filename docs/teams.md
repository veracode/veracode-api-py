# Teams

The following methods call Veracode REST APIs and return JSON.

_Note_: You can also access this method from the `Teams` class.

- `get_teams(all_for_org)`: get the list of teams for the user, or (if `all_for_org` is `True`) all teams in the organization.
- `get_team_by_id(team_uuid)`: get the details for a given team uuid, including members
- `create_team(team_name,business_unit,members)`: create a team named `team_name`. Optionally pass the business unit guid and/or a list of user names to add to the team.
- `update_team(team_guid,team_name(opt),business_unit(opt),members(opt))`: update the team identified by `team_guid` with the provided information.
- `delete_team(team_guid)`: delete the team identified by `team_guid`.

[All docs](docs.md)
