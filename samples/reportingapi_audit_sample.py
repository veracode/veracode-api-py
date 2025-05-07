import time
import sys
import json
import datetime
from veracode_api_py import Analytics

wait_seconds = 15

print('Generating audit report...')
theguid = Analytics().create_report(report_type="audit", start_date='2025-05-01',end_date='2025-05-05')

print('Checking status for report {}...'.format(theguid))
thestatus,theaudits=Analytics().get_audits(theguid)

while thestatus != 'COMPLETED':
    print('Waiting {} seconds before we try again...'.format(wait_seconds))
    time.sleep(wait_seconds)
    print('Checking status for report {}...'.format(theguid))
    thestatus,theaudits=Analytics().get_audits(theguid)

recordcount = len(theaudits)

print('Retrieved {} audit records'.format(recordcount))

if recordcount > 0:
    now = datetime.datetime.now().astimezone()
    filename = 'report-{}'.format(now)
    with open('{}.json'.format(filename), 'w') as outfile:
        json.dump(theaudits,outfile)
        outfile.close()

    print('Wrote {} audit records to {}.json'.format(recordcount,filename))