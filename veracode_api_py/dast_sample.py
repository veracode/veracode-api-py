import time
from veracode_api_py import DASTAnalysisProfiles, DASTAnalysisRuns, DASTTargets, VeracodeAPIError

# The most simple workflow to set up a DAST Essentials scan is as follows: 
# 1. Create the target
# 2. Configure the analysis profile
# 3. Run the scan
# 4. Get results
# See the Veracode Docs (https://docs.veracode.com/r/DAST_Essentials_REST_API) for more info.

#Update the values in this example for your own application
target = DASTTargets().create(name='Example', description='Example Target', protocol='HTTP',
                                url='www.example.com', target_type='WEB_APP', scan_type='QUICK', is_sec_lead_only=True)

#optionally, assign the target to a team during the create

analysisprofile = DASTAnalysisProfiles().get_all(target_id=target['target_id'])[0]

# update with actual credentials and login info using other authentication methods
DASTAnalysisProfiles().update_system_auth(analysis_profile_id=analysisprofile['analysis_profile_id'], 
                                          username='admin',password='smithy') 

DASTAnalysisProfiles().update(analysis_profile_id=analysisprofile['analysis_profile_id'], allowed_urls=[],
                              denied_urls=[], seed_urls=[], grouped_urls=[], crawler_mode='SMART')

scan = DASTAnalysisRuns().start(target_id=target['target_id'])

print('Scan id {} started on url {} at {}'.format(scan['id'], scan['url'], scan['started_at']))

# To fetch the report afterwards, use the following and save to a file.
done = False

while not done:
    try:
        report = DASTAnalysisRuns().get(target_id=target['target_id'])
        done = True
    except VeracodeAPIError:
        print('Report for target {} is not ready. Checking again in 10 seconds…'.format(target['target_id']))
        time.sleep(10)
        continue
    except Exception as e:
        print('A general exception occurred:{}'.format(str(e)))
        done=True

#print(report)