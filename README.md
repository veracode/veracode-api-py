# Veracode API Python

Python helper library for working with the Veracode APIs. Handles retries, pagination, and other features of the modern Veracode REST APIs.

Not an official Veracode product.

## Setup

Install from pypi:

    pypi veracode-api-py

(Optional) Save Veracode API credentials in `~/.veracode/credentials`

    [default]
    veracode_api_key_id = <YOUR_API_KEY_ID>
    veracode_api_key_secret = <YOUR_API_KEY_SECRET>

## Use in your applications

Include the library in your code and call the methods. Most methods return JSON or XML depending on the underlying API.

## Notes

1. Different API calls require different roles. Consult the [Veracode Help Center](https://help.veracode.com/go/c_role_permissions).
2. This library does not include a complete set of Veracode API methods.
3. Contributions are welcome.
