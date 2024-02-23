# Healthcheck and Status

The following methods call Veracode REST APIs and return JSON.

- `Healthcheck().healthcheck()`: returns an empty response with HTTP 200 if authentication succeeds.
- `Healthcheck().status()`: returns detailed status of Veracode services, mirroring [status.veracode.com](https://status.veracode.com).

[All docs](docs.md)
