# API Credentials

The following methods call Veracode REST APIs and return JSON.

_Note_: You can also access these methods from the `APICredentials` class.

- `get_creds()`: get credentials information (API ID and expiration date) for the current user.
- `get_creds(api_id)`: get credentials information (API ID and expiration date) for the user identified by `api_id`.
- `renew_creds()`: renew credentials for the current user. NOTE: you must note the return from this call as the API key cannot be viewed again.
- `revoke_creds(api_id)`: revoke immediately the API credentials identified by `api_id`.

[All docs](docs.md)
