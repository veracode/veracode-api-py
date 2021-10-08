#sca.py - API class for SCA API calls

import json
from urllib import parse

from .apihelper import APIHelper
from .constants import Constants

class Workspaces():
     sca_base_url = "srcclr/v3/workspaces"   

     def get_all(self):
          #Gets existing workspaces
          request_params = {}
          return APIHelper()._rest_paged_request(self.sca_base_url,"GET",params=request_params,element="workspaces")

     def get_by_name(self,name):
          #Does a name filter on the workspaces list. Note that this is a partial match. Only returns the first match
          name = parse.quote(name) #urlencode any spaces or special characters
          request_params = {'filter[workspace]': name}
          return APIHelper()._rest_paged_request(self.sca_base_url,"GET",params=request_params,element="workspaces")

     def create(self,name):
          #pass payload with name, return guid to workspace
          payload = json.dumps({"name": name})
          r = APIHelper()._rest_request(self.sca_base_url,"POST",body=payload,fullresponse=True)
          loc = r.headers.get('location','')
          return loc.split("/")[-1]

     def add_team(self,workspace_guid,team_id):
          return APIHelper()._rest_request(self.sca_base_url + "/{}/teams/{}".format(workspace_guid,team_id),"PUT")

     def delete(self,workspace_guid):
          return APIHelper()._rest_request(self.sca_base_url + "/{}".format(workspace_guid),"DELETE") 

     def get_teams(self):
          return APIHelper()._rest_paged_request("srcclr/v3/teams","GET","teams",{})

     def get_projects(self,workspace_guid):
          return APIHelper()._rest_paged_request(self.sca_base_url + '/{}/projects'.format(workspace_guid),"GET","projects",{})

     def get_project(self,workspace_guid,project_guid):
          uri = self.sca_base_url + '/{}/projects/{}'.format(workspace_guid,project_guid)
          return APIHelper()._rest_request(uri,"GET")

     def get_project_issues(self,workspace_guid,project_guid):
          uri = self.sca_base_url + '/{}/projects/{}/issues'.format(workspace_guid,project_guid)
          return APIHelper()._rest_paged_request(uri,"GET","issues",{})

     def get_project_libraries(self,workspace_guid,project_guid):
          uri = self.sca_base_url + '/{}/projects/{}/libraries'.format(workspace_guid,project_guid)
          return APIHelper()._rest_paged_request(uri,"GET","libraries",{})

     def get_agents(self,workspace_guid):
          return APIHelper()._rest_paged_request(self.sca_base_url + '/{}/agents'.format(workspace_guid),"GET","agents",{})

     def get_agent(self,workspace_guid,agent_guid):
          uri = self.sca_base_url + '/{}/agents/{}'.format(workspace_guid,agent_guid)
          return APIHelper()._rest_request(uri,"GET")

     def create_agent(self,workspace_guid,name,agent_type='CLI'):
          if agent_type not in Constants().AGENT_TYPE:
               raise ValueError("{} is not in the list of valid agent types ({})".format(agent_type,Constants().AGENT_TYPE))
          uri = self.sca_base_url + '/{}/agents'.format(workspace_guid)
          body = {'agent_type': agent_type, 'name': name}
          return APIHelper()._rest_request(uri,"POST",body=json.dumps(body))

     def delete_agent(self,workspace_guid,agent_guid):
          uri = self.sca_base_url + '/{}/agents/{}'.format(workspace_guid,agent_guid)
          return APIHelper()._rest_request(uri,"DELETE")

     def get_agent_tokens(self,workspace_guid,agent_guid):
          uri = self.sca_base_url + '/{}/agents/{}/tokens'.format(workspace_guid,agent_guid)
          return APIHelper()._rest_paged_request(uri, "GET" )

     def get_agent_token(self,workspace_guid,agent_guid,token_id):
          uri = self.sca_base_url + '/{}/agents/{}/tokens/{}'.format(workspace_guid,agent_guid,token_id)
          return APIHelper()._rest_paged_request(uri, "GET" )

     def regenerate_agent_token(self,workspace_guid, agent_guid):
          uri = self.sca_base_url + '/{}/agents/{}/tokens:regenerate'.format(workspace_guid,agent_guid)
          return APIHelper()._rest_request(uri,"POST")

     def revoke_agent_token(self,workspace_guid, agent_guid, token_id):
          uri = self.sca_base_url + '/{}/agents/{}/tokens/{}'.format(workspace_guid,agent_guid,token_id)
          return APIHelper()._rest_request(uri,"DELETE")

     def get_issues(self,workspace_guid):
          uri = self.sca_base_url + '/{}/issues'.format(workspace_guid)
          return APIHelper()._rest_paged_request(uri,"GET","issues",{})

     def get_issue(self,issue_id):
          uri = self.sca_base_url + '/issues/{}'.format(issue_id)
          return APIHelper()._rest_request(uri,"GET")

     def get_libraries(self,workspace_guid,unmatched):
          if unmatched:
               uri = self.sca_base_url + '/{}/libraries/unmatched'.format(workspace_guid)
          else:
               uri = self.sca_base_url + '/{}/libraries'.format(workspace_guid)
          return APIHelper()._rest_paged_request(uri,"GET",'libraries',{})

     def get_library(self,library_id):
          uri = "srcclr/v3/libraries/{}".format(library_id)
          return APIHelper()._rest_request(uri,"GET")

     def get_vulnerability(self,vulnerability_id):
          uri = "srcclr/v3/vulnerabilities/{}".format(vulnerability_id)
          return APIHelper()._rest_request(uri,"GET")

     def get_license(self,license_id):
          uri = "srcclr/v3/licenses/{}".format(license_id)
          return APIHelper()._rest_request(uri,"GET")

     def get_scan(self,scan_id):
          return APIHelper()._rest_request("srcclr/v3/scans/{}".format(scan_id),"GET")

     def get_events(self, date_gte=None, event_group=None, event_type=None):
          baseuri = "srcclr/v3/events"
          params = {}
          if event_group != None:
               if event_group not in Constants().SCA_EVENT_GROUP:
                    raise ValueError("{} is not in the valid list of SCA event groups ({})".format(event_group,Constants().SCA_EVENT_GROUP))
               params["group"]  = event_group

          if event_type != None:
               params["type"] = event_type

          if date_gte != None:
               params["date_gte"] = date_gte

          return APIHelper()._rest_paged_request(baseuri,"GET","events",params)
