import time
import sys
import datetime
from veracode_api_py import CustomPDF
import requests

wait_seconds = 5
app = 967128

print('Generating report...')
theguid = CustomPDF().create_report(app_id=app)

print('Checking status for report {}...'.format(theguid))
thestatus,theUrl=CustomPDF().get(theguid)

while thestatus != 'COMPLETE':
    print('Waiting {} seconds before we try again...'.format(wait_seconds))
    time.sleep(wait_seconds)
    print('Checking status for report {}...'.format(theguid))
    thestatus,theUrl=CustomPDF().get(theguid)

print('Report is at {}'.format(theUrl))

if len(theUrl) > 0:
    now = datetime.datetime.now().astimezone()
    filename = 'report-app-{}-{}'.format(app,now)

    headers = {"User-Agent": "api.py"}

    request = requests.Request("GET",theUrl,headers=headers)
    prepared_request = request.prepare()
    r = requests.Session().send(prepared_request)
    if r.status_code != requests.codes.ok:
        print("API call returned non-200 HTTP status code: {}".format(r.status_code))

    thepdf = r.content

    print(len(thepdf))

    with open('{}.pdf'.format(filename), 'wb') as outfile:
        outfile.write(thepdf)
        outfile.close()

        print('Wrote to {}.pdf'.format(filename))
