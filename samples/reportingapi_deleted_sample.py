import time
import sys
import json
import datetime
from veracode_api_py import Analytics

wait_seconds = 15

print('Generating deleted scans report...')
theguid = Analytics().create_report(report_type="deletedscans",deletion_start_date='2024-07-01',deletion_end_date='2024-12-31')

print('Checking status for report {}...'.format(theguid))
thestatus,thescans=Analytics().get_deleted_scans(theguid)

while thestatus != 'COMPLETED':
    print('Waiting {} seconds before we try again...'.format(wait_seconds))
    time.sleep(wait_seconds)
    print('Checking status for report {}...'.format(theguid))
    thestatus,thescans=Analytics().get_deleted_scans(theguid)

recordcount = len(thescans)

print('Retrieved {} scans'.format(recordcount))

if recordcount > 0:
    now = datetime.datetime.now().astimezone()
    filename = 'report-{}'.format(now)
    with open('{}.json'.format(filename), 'w') as outfile:
        json.dump(thescans,outfile)
        outfile.close()

    print('Wrote {} findings to {}.json'.format(recordcount,filename))