# Collections

The following methods call Veracode REST APIs and return JSON.

*Accessing*: The Collections feature is available only to Veracode customers in the Collections Early Adopter program. As the Collections feature is not generally available yet, the functionality of the feature will change over time.

- `Collections().get_all()`: get all collections for the organization.
- `Collections().get_by_name(collection_name)`: get all collections with a name that partially matches `collection_name`.
- `Collections().get_by_business_unit(business_unit_name)`: get all collections associated with `business_unit_name` (exact match).
- `Collections().get_statistics()`: get summary counts of collections by policy status.
- `Collections().get(guid)`: get detailed information for the collection identified by `guid`.
- `Collections().get_assets(guid)`: get a list of assets and detailed policy information for the collection identified by `guid`.
- `Collections().create(name, description(opt), tags(opt), business_unit_guid(opt),custom_fields(opt list),assets(opt list of application guids))`: create a collection with the provided settings.
- `Collections().update(guid, name, description(opt), tags(opt), business_unit_guid(opt),custom_fields(opt list),assets(opt list of application guids))`: update the collection identified by `guid` with the provided settings.
- `Collections().delete(guid)`: delete the collection identified by `guid`.

[All docs](docs.md)
