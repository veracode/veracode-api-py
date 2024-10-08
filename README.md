# Veracode API Python

Python helper library for working with the Veracode APIs. Handles retries, pagination, and other features of the modern Veracode REST APIs.

Not an official Veracode product. Heavily based on original work by [CTCampbell](https://github.com/ctcampbell).

## Setup

Install from pypi:

    pip install veracode-api-py

### Authenticating from a developer machine

Save Veracode API credentials in `~/.veracode/credentials`

    [default]
    veracode_api_key_id = <YOUR_API_KEY_ID>
    veracode_api_key_secret = <YOUR_API_KEY_SECRET>

### Authenticating from a pipeline

Set Veracode API credentials as environment variables.

    export VERACODE_API_KEY_ID=<YOUR_API_KEY_ID>
    export VERACODE_API_KEY_SECRET=<YOUR_API_KEY_SECRET>

### Authenticating through a proxy

To use this library (or a script based on it) with a proxy server, set environment variables with the address of the proxy:

    export HTTP_PROXY='http://10.10.10.10:8000'
    export HTTPS_PROXY='http://10.10.10.10:1212'

## Use in your applications

Import VeracodeAPI or one of the individual API classes into your code and call the methods. Most methods return JSON or XML depending on the underlying API.

You can find sample scripts for some APIs in the [Samples folder](https://github.com/veracode/veracode-api-py/tree/main/samples).

## Docs

For detailed documentation on the available methods, please see the [veracode-api-py docs](https://github.com/veracode/veracode-api-py/blob/main/docs/docs.md).

## Notes

1. Different API calls require different roles or permissions. Consult the [Veracode Docs](https://docs.veracode.com/r/c_role_permissions).
2. This library does not include a complete set of Veracode API methods. In particular, it only provides a handful of XML API methods.
3. Contributions are welcome. See the [Contributions guidelines](CONTRIBUTING.md).
