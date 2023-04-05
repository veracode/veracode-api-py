# Collections

The following methods call Veracode REST APIs and return JSON.

**Notes**:

1. The Collections feature is available only to Veracode customers in the Collections Early Adopter program. As the Collections feature is not generally available yet, the functionality of the feature will change over time.
2. You can also access this method from the `Collections` class.

- `get_collections()`: get all collections for the organization.
- `get_collections_by_name(collection_name)`: get all collections with a name that partially matches `collection_name`.
- `get_collections_by_business_unit(business_unit_name)`: get all collections associated with `business_unit_name` (exact match).
- `get_collections_statistics()`: get summary counts of collections by policy status.
- `get_collection(guid)`: get detailed information for the collection identified by `guid`.
- `get_collection_assets(guid)`: get a list of assets and detailed policy information for the collection identified by `guid`.
- `create_collection(name, description(opt), tags(opt), business_unit_guid(opt),custom_fields(opt list),assets(opt list of application guids))`: create a collection with the provided settings.
- `update_collection(guid, name, description(opt), tags(opt), business_unit_guid(opt),custom_fields(opt list),assets(opt list of application guids))`: update the collection identified by `guid` with the provided settings.
- `delete_collection(guid)`: delete the collection identified by `guid`.

[All docs](docs.md)
