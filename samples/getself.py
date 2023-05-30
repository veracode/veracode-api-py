# a simple sample to get attributes from the user's login information
from veracode_api_py import Users

me = Users().get_self()

print("You are {}".format(me['user_name']))