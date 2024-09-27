# Just In Time Provisioning Default Settings

The following methods call Veracode REST APIs and return JSON. More information about the JIT settings is available in the [Veracode Docs](https://docs.veracode.com/r/Configure_SAML_Self_Registration).

- `JITDefaultSettings().get()` - retrieve the current Just In Time (JIT) default settings.
- `JITDefaultSettings().create(ip_restricted(opt),prefer_veracode_data(opt), allowed_ip_addresses(opt), use_csv_for_roles_claim(opt), use_csv_for_teams_claim(opt), use_csv_for_teams_managed_claim(opt), use_csv_for_ip_address_claim(opt),teams(opt),roles(opt))` - create new Just In Time (JIT) default settings. Settings include:
    - `ip_restricted`: set to `True` to apply IP restrictions (defined in `allowed_ip_addresses`) for a JIT user.
    - `prefer_veracode_data`: set to `True` to allow an administrator to manage roles, teams, and other settings for users in the Veracode administrative console after user creation. If set to `False`, the SAML assertion sent from the customer's Identity Provider must contain these values.
    - `allowed_ip_addresses`: an array of IP addresses. See the [Veracode Docs](https://docs.veracode.com/r/admin_ip) for more information.
    - `use_csv_for_roles_claim`: set to `True` if your IDP will send a comma separated list of roles (instead of an array).
    - `use_csv_for_teams_claim`: set to `True` if your IDP will send a comma separated list of teams (instead of an array).
    - `use_csv_for_teams_managed_claim`: set to `True` if your IDP will send a comma separated list of teams managed by a team admin (instead of an array).
    - `use_csv_for_ip_address_claim`: set to `True` if your IDP will send a comma separated list of IP address restrictions (instead of an array).
    - `teams`: an array of team IDs (UUIDs) that should be assigned to a JIT user by default.
    - `roles`: an array of role IDs (UUIDs) that should be assigned to a JIT user by default.
- `JITDefaultSettings().update(jit_default_id, ip_restricted(opt),prefer_veracode_data(opt), allowed_ip_addresses(opt), use_csv_for_roles_claim(opt), use_csv_for_teams_claim(opt), use_csv_for_teams_managed_claim(opt), use_csv_for_ip_address_claim(opt),teams(opt),roles(opt))` - update existing Just In Time (JIT) default settings identified by `jit_default_id`.
- `JITDefaultSettings().delete(jit_default_id)` - delete the Just In Time (JIT) default settings identified by `jit_default_id`.

[All docs](docs.md)
