# Roles and Permissions

The following methods call Veracode REST APIs and return JSON.

- `Roles().get_all()`: get the list of roles for the organization.
- `Roles().get(role_guid)`: get the role definition for a given role.
- `Roles().create(role_name,role_description,is_api (opt),jit_assignable(opt),jit_assignable_default (opt),permissions (opt),child_roles (opt))`: create a role named `role_name`. You must specify either `permissions` or `child_roles`, or both. Arguments include:
    - `role_description`: The human readable description of the role.
    - `is_api`: Set to `True` to create a role for an API user. Defaults to `False`.
    - `jit_assignable`: Set to `True` to allow the role to be assigned by a SAML assertion using just-in-time provisioning. Defaults to `True`.
    - `jit_assignable_default`: Set to `True` to allow the role to be assigned by default during just-in-time provisioning. Defaults to `True`.
    - `permissions`: An array of permission names. Use `Permissions().get_all()` to see the list of assignable permissions. 
    - `child_roles`: An array of role names. Adding a child role to a custom role gives the user all the permissions contained in the child role, in addition to any permissions defined in `permissinos`. You can add more than one child role.
- `Roled().update(role_name,role_description,role_guid,is_api (opt),jit_assignable(opt),jit_assignable_default (opt),permissions (opt),child_roles (opt))`: update the role identified by `role_guid` with the provided information.
- `Roles().delete(role_guid)`: delete the role identified by `role_guid`. Note: You can only delete custom roles.
- `Permissions().get_all()`: get the list of permissions that can be part of custom roles.
- `Permissions().get(permission_guid)`: get the permission definition for a given permission.


[All docs](docs.md)
