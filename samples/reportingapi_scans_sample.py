import time
import sys
import json
import datetime
from veracode_api_py import Analytics

wait_seconds = 15

print('Generating report...')

theguid = Analytics().create_scans_report(start_date="2025-10-01",application_id="1024496",policy_sandbox="POLICY",scan_type=["Static Analysis"])

print('Checking status for report {}...'.format(theguid))
thestatus,thescans=Analytics().get(theguid)

while thestatus != 'COMPLETED':
    print('Waiting {} seconds before we try again...'.format(wait_seconds))
    time.sleep(wait_seconds)
    print('Checking status for report {}...'.format(theguid))
    thestatus,thescans=Analytics().get(theguid)

recordcount = len(thescans)

print('Retrieved {} findings'.format(recordcount))

if recordcount > 0:
    now = datetime.datetime.now().astimezone()
    filename = 'report-{}'.format(now)
    with open('{}.json'.format(filename), 'w') as outfile:
        json.dump(thescans,outfile)
        outfile.close()

    print('Wrote {} scans to {}.json'.format(recordcount,filename))