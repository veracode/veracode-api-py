# Healthcheck and Status

The following methods are deprecated. To verify a successful connection to the platform, check the response to Users().get_self() instead. To get information about scheduled maintenance and incidents, use the RSS feed for the [Veracode status page](https://docs.veracode.com/r/c_about_site_status). 

- `Healthcheck().healthcheck()`: returns an empty response with HTTP 200 if authentication succeeds.
- `Healthcheck().status()`: returns detailed status of Veracode services, mirroring [status.veracode.com](https://status.veracode.com).

[All docs](docs.md)
