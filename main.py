import re
import os
import sys
import logging
import requests
import argparse

from typing import Optional, Tuple
from ws_sdk.web import WS
from ws_sdk.ws_constants import AlertTypes
from smartbear_jira import SBJira, SBProductMapper
from smartbear_jira.constants import Priority, DEFAULT_PROJECT
from smartbear_jira.models.security import SecurityIssue

format = '%(asctime)-15s %(levelname)-8s %(filename)-25s %(message)s'
logging.basicConfig(format=format, level=logging.INFO, stream=sys.stdout)

ALPHA_ONLY = re.compile(r'[\W_-]+', re.UNICODE)
LICENSE_TITLE = 'License Risk'

from veracode_api_py.api import VeracodeAPI

# App profile being used.
#https://analysiscenter.veracode.com/auth/index.jsp#SandboxView:52168:770521:4326210

# Dry Run
# When set to True, script will perform no write actions, like creating
# or closing Jira tickets
DRY_RUN = False

#Veracode Connection
veracode = VeracodeAPI()

# Jira Cloud connection
jira_username = os.environ['JIRA_USER']
sb_jira_url = os.environ['SB_JIRA_URL']
jira_api_token = os.environ['JIRA_TOKEN']

JIRA = SBJira(sb_jira_url,jira_username, jira_api_token)



# This will need to be made into a drop down selector later on but POC will use 'appdesign' always
Verified_LIST = {
    'Mitigate by Design': 'appdesign',
    'Add Comment':'comment',
    'False Positive': 'fp',
    'OS Env':'osenv',
    'Network Env':'netenv',
    'Third Party Library':'library',
    'Accept Mitigation':'accepted',
    'Reject Mitigation':'rejected',
    'Risk Accepted': 'acceptrisk'
}

def get_jira_issues(is_open: bool = True) -> dict[str, SecurityIssue]:
    '''
    Return a map of WS alert IDs to the corresponding Jira ticket key for the given WS Org and Product

    Parameters:
    org_slug (str): The WhiteSource Organization in slug form (normalized value)
    product_id (str): The WhiteSource Product ID of related alerts
    is_license (bool), optional: Whether search for license issues or vulnerabilities. Default: False (vulnerabilities)
    is_open (bool), optional: Whether search will return active or closed issues. Default: True (open ticket)

    Returns:
    dict: Returns a map of WhiteSource Alert UUIDs to the corresponding Jira issue object
    '''
    jql_request = (
        f'project = {DEFAULT_PROJECT} AND issuetype = "{"Security Finding"}" '
        f'AND "Justification and Context[Paragraph]" is not EMPTY" '
        f'AND "Remediation Status[Short text]" ~ "Open" '
        f'AND resolution IS {"" if is_open else "NOT"} EMPTY ORDER BY issuekey'
    )

    all_issues: list[SecurityIssue] = JIRA.query(jql_request)

    # Return map of WS Alert ID to Jira issue key
    return {issue.link.split(':')[-1]: issue for issue in all_issues}

def get_jira_isuse_info(issue):
    working_issue = JIRA.get(issue)
    mitigation_comment = working_issue['customfield_17329']
    #build_id=veracode_build_id
    #flaw_id=veracode_flaw_id
    return mitigation_comment


def mitigate_the_flaw(build_id:int, flaw_id: int, comment:str):


    build_id= 17089903 # get from app profile link
    flaw_id = 2929 # get from flaw info
    mitigation_reason = 'Mitigate by Design' # get this from dropdown
    mitigation_key = Verified_LIST[mitigation_reason] # key match to dict from dropdown
    comment = 'This is a test comment' # get this from justification

    print(veracode.set_mitigation_info(build_id,flaw_id,mitigation_key,comment))


print(JIRA.get('APPSEC-27322'))
working_issue = JIRA.get('APPSEC-27322')

#print(mitigation_comment)
print(JIRA)