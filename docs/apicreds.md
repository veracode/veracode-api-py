# API Credentials

The following methods call Veracode REST APIs and return JSON.

**Notes**:

1. You can also access these methods from the `APICredentials` class.
1. Calling these methods requires a user with the [Administator, Team Admin,](https://docs.veracode.com/r/c_role_permissions) or [Admin API](https://docs.veracode.com/r/c_API_roles_details) user role.

- `APICredentials().get(api_id)`: get credentials information (API ID and expiration date) for the user specified by `api_id`.
- `APICredentials().get_self()`: get credentials information for the user calling the API.
- `APICredentials().create(user_guid)`: create or renew API credentials for the API service account specified by `user_guid`.
- `APICredentials().renew()`: renew credentials for the current user. NOTE: you must note the return from this call as the API key cannot be viewed again.
- `APICredentials().revoke (api_id)`: revoke immediately the API credentials identified by `api_id`.

[All docs](docs.md)
