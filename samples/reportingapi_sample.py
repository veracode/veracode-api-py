import time
import sys
import json
import datetime
from veracode_api_py import Analytics

wait_seconds = 15

print('Generating report...')
theguid = Analytics().create_report(report_type="findings",last_updated_start_date="2023-07-01 00:00:00")

print('Checking status for report {}...'.format(theguid))
thestatus,thefindings=Analytics().get(theguid)

while thestatus != 'COMPLETED':
    print('Waiting {} seconds before we try again...'.format(wait_seconds))
    time.sleep(wait_seconds)
    print('Checking status for report {}...'.format(theguid))
    thestatus,thefindings=Analytics().get(theguid)

recordcount = len(thefindings)

print('Retrieved {} findings'.format(recordcount))

if recordcount > 0:
    now = datetime.datetime.now().astimezone()
    filename = 'report-{}'.format(now)
    with open('{}.json'.format(filename), 'w') as outfile:
        json.dump(thefindings,outfile)
        outfile.close()

    print('Wrote {} findings to {}.json'.format(recordcount,filename))