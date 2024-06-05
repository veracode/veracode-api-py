# a sample to show how to use veracode-api-py to access static scanning functions
from veracode_api_py import StaticCLI

#you can get a scan id from the output of the veracode static scan CLI command
sample_scan_id = 'a5565dfa-6cad-491c-b680-e32f501c1b5a'

scan = StaticCLI().Scans().get(scan_id=sample_scan_id)

status = scan['scan_status']
segments = scan['binary_segments_expected']

print ('Scan status is {}'.format(status))

if status == 'SUCCESS':
    findings = StaticCLI().Scans().Findings().get(scan_id=sample_scan_id)
    print ('Findings: {}'.format(len(findings.get("findings"))))
