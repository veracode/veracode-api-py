import time
from veracode_api_py import Analytics

wait_seconds = 15

print('Generating report...')
theguid = Analytics().create_report(report_type="findings",last_updated_start_date="2020-03-15 00:00:00")

print('Checking status for report {}...'.format(theguid))
thestatus,thefindings=Analytics().get(theguid)

while thestatus != 'COMPLETED':
    print('Waiting {} seconds before we try again...'.format(wait_seconds))
    time.sleep(wait_seconds)
    print('Checking status for report {}...'.format(theguid))
    thestatus,thefindings=Analytics().get(theguid)

print('Retrieved {} findings'.format(len(thefindings)))