# Users

The following methods call Veracode REST APIs and return JSON.

- `Users().get_all()`: get a list of users for the organization.
- `Users().get_self()`: get user information for the current user.
- `Users().get(user_guid)`: get information for an individual user based on `user_guid`.
- `Users().get_by_name(username)`: look up info for an individual user based on their user_name.
- `Users().get_by_search(search_term, api_id, role_id, login_status, saml_user, team_id, detailed, user_type, request_params)`: search for users based on parameters below (all optional):
  - `search_term`: string
  - `api_id`: search by customer api id
  - `role_id`: search by role_id (see `get_roles`)
  - `login_status`: search by login status (e.g. `active`)
  - `saml_user`: search by saml user ID
  - `team_id`: serach by team ID (see `get_teams`)
  - `detailed`: returns additional attributes in summary list of users
  - `user_type`: search by user type (e.g. `user` or `api`)
  - `request_params`: optionally pass a dictionary of additional query parameters. See [Identity API specification](https://app.swaggerhub.com/apis/Veracode/veracode-identity_api/1.0#/user/getUsersBySearchUsingGET)
- `Users().create(email,firstname,lastname,type(opt),username(opt),roles(opt),mfa(opt))`: create a user based on the provided information.
  - `type`: `HUMAN` or `API`. Defaults to `HUMAN`. If `API` specified, must also provide `username`.
  - `roles`: list of role names (specified in the Veracode Help Center, for both [human](https://help.veracode.com/go/c_identity_create_human) and [API service account](https://help.veracode.com/go/c_identity_create_api) users). Provide the role names from `get_roles()`.
  - `mfa`: set to `TRUE` to require the user to configure multifactor authentication on first sign in.
- `Users().update_roles(user_guid, roles)`: update the user identified by `user_guid` with the list of roles passed in `roles`. Because the Identity API does not support adding a single role, the list should be the entire list of existing roles for the user plus whatever new roles. See [veracode-user-bulk-role-assign](https://github.com/tjarrettveracode/veracode-user-bulk-role-assign) for an example.
- `Users().update(user_guid,changes)`: update a user based upon the provided information.
  - `user_guid`: the unique identifier of the user to be updated.
  - `changes`: the attributes of the user to be changed. Must be JSON whose format follows the [Identity API specification](https://app.swaggerhub.com/apis/Veracode/veracode-identity_api/1.0#/ResourceOfUserResource) of a valid user object.
- `Users().update_email_address(user_guid,email_address,ignore_verification(opt))`: updates the email address of the specified user.
  - `ignore_verification`: Boolean. Defaults to `False`. If `True`, immediately updates email address without requiring the user to verify the change via email. If the user has not yet activated the account, this must be set to `True`.
- `Users().reset_password(user_legacy_id)`: sends a password reset email to the specified user. If the user has yet to activate their account, sends a new activation email instead.
  - NOTE: this function uses the `user_legacy_id` value (as opposed to the `user_guid` value), which can be obtained via a call to `get_user()`.
- `Users().disable(user_guid)`: set the `Active` flag the user identified by `user_guid` to `False`.
- `Users().delete(user_guid)`: delete the user identified by `user_guid`. This is not a reversible action.
- `Roles().get_all()`: get a list of available roles to assign to users.

[All docs](docs.md)
