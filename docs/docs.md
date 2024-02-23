# veracode-api-py docs

See the topics below for more information on how to use this library.

`veracode-api-py` provides two ways to access each method in the library. The library provides individual objects for key resource types (e.g. Applications, Users, Workspaces) on which indvidual methods can be called. Alternately, there is a single "API object" that lists all the methods in the library.

## Scans, Findings, Applications and Policy

* [XML APIs](xml.md) - work with Veracode legacy XML APIs to access report data for individual scans and to perform static scans.
* [Healthcheck and Status](healthcheck.md) - access information about the status of Veracode services.
* [Applications and Sandboxes](applications.md) - create, update, access, and delete application profiles and sandboxes.
* [Policy](policy.md) - create, update, access, and delete policy definitions.
* [Findings and Annotations](findings.md) - retrieve findings and propose, accept, and reject mitigations.
* [Collections](collections.md) - (EARLY ACCESS) create, update, access, and delete collections.
* [SCA Agent](sca.md) - access information about SCA workspaces, projects, issues, vulnerabilities, libraries, and licenses.
* [Dynamic Analysis](dynamic.md) - configure, schedule and start dynamic analyses.
* [Analytics](analytics.md) - request and retrieve reports across your Veracode organization.

## Administration

* [Users](users.md) - create, update, access, and delete users.
* [Teams](teams.md) - create, update, access, and delete teams.
* [Business Units](businessunits.md) - create, update, access, and delete business units.
* [API Credentials](apicreds.md) - create, access, renew, and revoke API credentials.

## API Object

You can use the library without importing individual methods by using the `API()` object.

* [API](api.md) - use this object to access all methods in the `veracode-api-py` library.