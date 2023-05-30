# API Credentials

The following methods call Veracode REST APIs and return JSON.

**Notes**:

1. You can also access these methods from the `APICredentials` class.
1. Calling these methods requires a user with the [Administator, Team Admin,](https://docs.veracode.com/r/c_role_permissions) or [Admin API](https://docs.veracode.com/r/c_API_roles_details) user role.

- `get_creds(api_id(opt))`: get credentials information (API ID and expiration date) for the user specified by `api_id`; if `api_id` is `None`, get credentials information for the user themselves.
- `create_creds(user_guid)`: create or renew API credentials for the API service account specified by `user_guid`.
- `renew_creds()`: renew credentials for the current user. NOTE: you must note the return from this call as the API key cannot be viewed again.
- `revoke_creds(api_id)`: revoke immediately the API credentials identified by `api_id`.

[All docs](docs.md)
