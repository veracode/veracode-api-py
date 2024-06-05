from veracode_api_py import SBOM
from requests.exceptions import RequestException
import json

# provide a file name that is either in the same directory, or a fully qualified path
# to generate a small sample, try:
# veracode sbom --type image --source alpine:latest --format cyclonedx-json
file = 'api-signing-sbom.json'

try:
    f = open (file)
except IOError:
    print('File is not valid: {}'.format(file))

try:
    updated_sbom = SBOM().scan(sbom=file)
    if updated_sbom is not None:
        # do something useful
        print(updated_sbom['components'][17])

except RequestException as e:
    print(type(e))
    print(e)
