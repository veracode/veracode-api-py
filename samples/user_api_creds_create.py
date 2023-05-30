from veracode_api_py import Users, APICredentials

# This script creates an API user and then initializes their API credentials

the_teams = ['46cc22ff-xxxx-xxxx-xxxx-xxxxxxxxxxx'] # fill in with the appropriate team GUIDs from Teams().get_all()
the_username = 'sample_username' # fill in with the appropriate username
the_email = 'veracode123@example.com' # fill in with the appropriate email
the_roles = ["resultsapi"] # fill in with appropriate roles. Roles list is provided by Roles().get_all()

print('Creating API service account with username {}...'.format(the_username))
theuser = Users().create(email=the_email,lastname='demo',firstname='demo',username=the_username,
                         type='API',roles=the_roles,teams=the_teams)

theguid = theuser['user_id']

thecreds = APICredentials().create(user_guid=theguid)

print('')
print('[{}]'.format(the_username))
print('veracode_api_key_id={}'.format(thecreds['api_id']))
print('veracode_api_key_secret={}'.format(thecreds['api_secret']))
print('')
print('Please clear your terminal and scrollback buffer once you have copied the credentials!')
