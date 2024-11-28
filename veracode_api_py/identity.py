#identity.py - API classes for Identity API calls

import json
import logging
from urllib import parse
from uuid import UUID

from .apihelper import APIHelper

logger = logging.getLogger(__name__)

class Users():
   USER_URI = "api/authn/v2/users"

   def get_all(self):
      #Gets a list of users using the Veracode Identity API        
      request_params = {'page': 0} #initialize the page request
      return APIHelper()._rest_paged_request(self.USER_URI,"GET","users",request_params)

   def get_self (self):
      #Gets the user info for the current user, using the Veracode Identity API
      return APIHelper()._rest_request(self.USER_URI + "/self","GET")

   def get(self,user_guid: UUID):
      #Gets an individual user provided their GUID, using the Veracode Identity API
      uri = self.USER_URI + "/{}".format(user_guid)
      return APIHelper()._rest_request(uri,"GET")

   def get_by_name(self,username):
      #Gets all the users who match the provided email address, using the Veracode Identity API
      request_params = {'user_name': parse.quote(username)} #initialize the page request
      return APIHelper()._rest_paged_request(self.USER_URI,"GET","users",request_params)

   def get_user_search(self,search_term: str=None, api_id: UUID=None, role_id: UUID=None, login_status=None, saml_user=None, team_id: UUID=None, detailed=False, user_type=None, request_params=None):
      if request_params == None:
         request_params = {'detailed': detailed}
      
      if search_term != None:
         request_params['search_term'] = parse.quote(search_term)

      if api_id != None:
         request_params['api_id'] = api_id

      if role_id != None:
         request_params['role_id'] = role_id
      
      if login_status != None:
         request_params['login_status'] = login_status

      if saml_user != None:
         request_params['saml_user'] = saml_user

      if team_id != None:
         request_params['team_id'] = team_id

      if user_type != None:
         request_params['user_type'] = user_type
         
      return APIHelper()._rest_paged_request(self.USER_URI + "/search","GET","users",request_params)

   def create(self,email,firstname: str,lastname: str,username: str=None,type="HUMAN",roles=[],teams=[],mfa=False):
      user_def = { "email_address": email, "first_name": firstname, "last_name": lastname, "active": True }

      rolelist = []
      if len(roles) > 0:
         for role in roles:
               rolelist.append({"role_name": role})
         user_def.update({"roles":rolelist})

      if type == "API":
         user_def.update({"user_name": username})
         user_def.update({"permissions": [{"permission_name": "apiUser"}]})
         if len(roles) == 0:
            rolelist.append({"role_name": "uploadapi"})
            rolelist.append({"role_name":"apisubmitanyscan"})
      else:
         if len(roles) == 0:
            rolelist.append({"role_name":"submitter"}) 

      if username is not None:
         user_def.update({"user_name": username})
      else:
         user_def.update({"user_name": email})

      teamlist = []
      if len(teams) > 0:
         for team in teams:
               teamlist.append({"team_id": team})
         user_def.update({"teams": teamlist})

      user_def.update({"roles": rolelist})

      if mfa:
         user_def.update({"pin_required":True})

      payload = json.dumps(user_def)
      return APIHelper()._rest_request(self.USER_URI,'POST',body=payload)

   def update_roles(self,user_guid: UUID,roles: list):
      request_params = {'partial': 'TRUE',"incremental": 'FALSE'}
      uri = self.USER_URI + "/{}".format(user_guid)

      rolelist = []
      for role in roles:
            rolelist.append({"role_name": role})

      payload = json.dumps({"roles": rolelist})
      return APIHelper()._rest_request(uri,"PUT",request_params,body=payload)

   def update(self,user_guid: UUID,changes):
      request_params = {'partial':'TRUE',"incremental": 'TRUE'}
      uri = self.USER_URI + "/{}".format(user_guid)
      payload = json.dumps(changes)
      return APIHelper()._rest_request(uri,"PUT",request_params,body=payload)

   def update_email_address(self,user_guid: UUID,email_address,ignore_verification=False):
      request_params = {'partial':'TRUE',"incremental": 'FALSE'}
      if ignore_verification:
         request_params['adminNoVerificationEmail'] = 'TRUE'
      uri = self.USER_URI + "/{}".format(user_guid)
      user_def = {'email_address': email_address}
      payload = json.dumps(user_def)
      return APIHelper()._rest_request(uri,"PUT",request_params,body=payload)

   def reset_password(self,user_legacy_id):
      # Sends a password reset email for the specified user
      # If user has not yet activated, re-sends activation email instead
      uri = self.USER_URI + "/{}/resetPassword".format(user_legacy_id)
      return APIHelper()._rest_request(uri,"POST")

   def disable(self,user_guid: UUID):
      request_params = {'partial':'TRUE'}
      uri = self.USER_URI + '/{}'.format(user_guid)
      payload = json.dumps({'active': False})
      return APIHelper()._rest_request(uri,"PUT",request_params,payload)

   def delete(self,user_guid: UUID):
      uri = self.USER_URI + '/{}'.format(user_guid)
      return APIHelper()._rest_request(uri,"DELETE")

class Teams():
   def get_all(self, all_for_org=False):
      #Gets a list of teams using the Veracode Identity API       
      if all_for_org:
         request_params = {'all_for_org': True}
      else:
         request_params = {'page': 0} #initialize the page request
      return APIHelper()._rest_paged_request("api/authn/v2/teams","GET","teams",request_params)

   def get(self, team_id):
      uri = "api/authn/v2/teams/{}".format(team_id)
      return APIHelper()._rest_request(uri,"GET")
   
   def create(self, team_name: str, business_unit=None, members=[]):        
      team_def = {'team_name': team_name}
      
      if len(members) > 0:
         # optionally pass a list of usernames to add as team members
         users = []
         for member in members:
               users.append({'user_name': member})
         team_def.update({'users': users})

      if business_unit != None:
         bu = {'bu_id': business_unit}
         team_def.update(bu)

      payload = json.dumps(team_def)
      return APIHelper()._rest_request('api/authn/v2/teams','POST',body=payload)

   def update(self, team_guid: UUID, team_name: str="", business_unit: UUID=None, members=[], incremental=True, partial=True):
      requestbody = {}
      
      if team_name != "":
         requestbody.update({"team_name": team_name})

      if business_unit != None:
         requestbody.update({"business_unit": {"bu_id": business_unit}})

      if len(members) > 0:
         users = []
         for member in members:
               users.append({"user_name": member})
         requestbody.update({"users": users})

      if requestbody == {}:
         logging.error("No update specified for team {}".format(team_guid))

      payload = json.dumps(requestbody)
      params = {"partial": partial, "incremental": incremental}
      uri = 'api/authn/v2/teams/{}'.format(team_guid)
      return APIHelper()._rest_request(uri,'PUT',body=payload,params=params)

   def delete(self, team_guid: UUID):
      uri = 'api/authn/v2/teams/{}'.format(team_guid)
      return APIHelper()._rest_request(uri,"DELETE")

class BusinessUnits():
   base_uri = "api/authn/v2/business_units"

   def get_all(self):
      request_params = {'page': 0}
      return APIHelper()._rest_paged_request(self.base_uri,"GET","business_units",request_params)

   def get(self,guid: UUID):
      return APIHelper()._rest_request(self.base_uri + "/{}".format(guid),"GET")

   def create(self,name: str,teams=[]):
      payload = {"bu_name":name}

      if len(teams)>0:
         team_list = []
         for team in teams:
            team_list.append({"team_id": team})
         payload["teams"] = team_list

      return APIHelper()._rest_request(self.base_uri,"POST",body=json.dumps(payload))

   def update(self,guid: UUID,name: str="",teams=[]):
      payload = {}

      if name != "":
         payload["bu_name"] = name
      
      if len(teams)>0:
         team_list = []
         for team in teams:
            team_list.append({"team_id": team})
         payload["teams"] = team_list

      return APIHelper()._rest_request(self.base_uri + "/{}".format(guid),"PUT",body=json.dumps(payload),params={"partial":True, "incremental":True})

   def delete(self,guid: UUID):
      return APIHelper()._rest_request(self.base_uri + "/{}".format(guid),"DELETE")

class APICredentials():
   base_uri = "api/authn/v2/api_credentials"
   def get_self (self):
      return APIHelper()._rest_request(self.base_uri,"GET")

   def get (self, api_id):
      return APIHelper()._rest_request(self.base_uri + '/{}'.format(api_id),"GET")
   
   def create (self, user_guid: UUID):
      return APIHelper()._rest_request("{}/user_id/{}".format(self.base_uri,user_guid),"POST",body=json.dumps({}))

   def renew (self):
      return APIHelper()._rest_request(self.base_uri,"POST",body=json.dumps({}))

   def revoke (self, api_id):
      return APIHelper()._rest_request(self.base_uri + '/{}'.format(api_id), "DELETE")

class Roles():
   base_uri = "api/authn/v2/roles"
   def get_all(self):
      return APIHelper()._rest_paged_request(self.base_uri,"GET","roles",{'page':0})
   
   def get(self, role_guid: UUID):
      return APIHelper()._rest_request("{}/{}".format(self.base_uri,role_guid),"GET")
   
   def create(self, role_name, role_description, is_api=False, jit_assignable=True, 
              jit_assignable_default=True, permissions=[], child_roles=[]):
      return self._create_or_update("CREATE", role_name=role_name, role_description=role_description,
                                    is_api=is_api, jit_assignable=jit_assignable, 
                                    jit_assignable_default=jit_assignable_default, 
                                    permissions=permissions, child_roles=child_roles)
   
   def update(self, role_name, role_description, role_guid: UUID, is_api=False, 
              jit_assignable=True, jit_assignable_default=True, 
              permissions=[], child_roles=[]): 
      # TODO handle partial and incremental
      return self._create_or_update("UPDATE", role_name=role_name, role_description=role_description,
                                    role_guid=role_guid, is_api=is_api, jit_assignable=jit_assignable,
                                    jit_assignable_default=jit_assignable_default,
                                    permissions=permissions, child_roles=child_roles)
   
   def delete(self, role_guid: UUID):
      return APIHelper()._rest_request("{}/{}".format(self.base_uri,role_guid),"DELETE")

   def _create_or_update(self, method, role_name, role_description, role_guid: UUID=None, is_api=False,
                         jit_assignable=True,jit_assignable_default=True,
                         permissions=[], child_roles=[]):
      uri = self.base_uri
      if method == 'CREATE':
         httpmethod = 'POST'
      elif method == 'UPDATE':
         uri = uri + '/{}'.format(role_guid)
         httpmethod = 'PUT'
      else:
         return
      
      role_def = { 'role_name': role_name, 'role_description': role_description, 'is_api': is_api,
                  'jit_assignable': jit_assignable, 'jit_assignable_default': jit_assignable_default}
      
      if len(permissions) > 0:
         role_def['permissions'] = permissions

      if len(child_roles) > 0:
         role_def['child_roles'] = child_roles

      payload = json.dumps(role_def)
      return APIHelper()._rest_request(uri,httpmethod,body=payload)

class Permissions():
   base_uri = "api/authn/v2/permissions"
   def get_all(self):
      return APIHelper()._rest_paged_request( self.base_uri,"GET","permissions",{'page':0})
   
   def get(self, permission_guid: UUID):
      return APIHelper()._rest_request("{}/{}".format(self.base_uri,permission_guid),"GET")
   
class JITDefaultSettings():
   base_uri = "api/authn/v2/jit_default_settings"

   def get(self):
      return APIHelper()._rest_request( self.base_uri, "GET")
   
   def create(self, ip_restricted=False,prefer_veracode_data=True, allowed_ip_addresses=[],
              use_csv_for_roles_claim=False, use_csv_for_teams_claim=False, use_csv_for_teams_managed_claim=False,
              use_csv_for_ip_address_claim=True,teams=[],roles=[]):
      return self._create_or_update("CREATE", ip_restricted=ip_restricted, prefer_veracode_data=prefer_veracode_data,
                                    allowed_ip_addresses=allowed_ip_addresses, use_csv_for_roles_claim=use_csv_for_roles_claim,
                                    use_csv_for_teams_claim=use_csv_for_teams_claim, 
                                    use_csv_for_teams_managed_claim=use_csv_for_teams_managed_claim, 
                                    use_csv_for_ip_address_claim=use_csv_for_ip_address_claim, teams=teams, roles=roles)
   
   def update(self, jit_default_id: UUID, ip_restricted=False,prefer_veracode_data=True, allowed_ip_addresses=[],
              use_csv_for_roles_claim=False, use_csv_for_teams_claim=False, use_csv_for_teams_managed_claim=False,
              use_csv_for_ip_address_claim=True,teams=[],roles=[]):
      return self._create_or_update("UPDATE", jit_default_id = jit_default_id, ip_restricted=ip_restricted, 
                                    prefer_veracode_data=prefer_veracode_data,allowed_ip_addresses=allowed_ip_addresses, 
                                    use_csv_for_roles_claim=use_csv_for_roles_claim,
                                    use_csv_for_teams_claim=use_csv_for_teams_claim, 
                                    use_csv_for_teams_managed_claim=use_csv_for_teams_managed_claim, 
                                    use_csv_for_ip_address_claim=use_csv_for_ip_address_claim, teams=teams, roles=roles)
   
   def _create_or_update(self, method, jit_default_id: UUID=None, ip_restricted=False,prefer_veracode_data=True, allowed_ip_addresses=[],
              use_csv_for_roles_claim=False, use_csv_for_teams_claim=False, use_csv_for_teams_managed_claim=False,
              use_csv_for_ip_address_claim=True,teams=[],roles=[]):
      
      if method == "CREATE":
         uri = self.base_uri
         httpmethod = "POST"
      elif method == "UPDATE":
         uri = '{}/{}'.format(self.base_uri, jit_default_id)
         httpmethod = "PUT"
      else:
         return 
      
      params = { 'ip_restricted': ip_restricted, 'prefer_veracode_data': prefer_veracode_data, 'allowed_ip_addresses': allowed_ip_addresses,
                'use_csv_for_roles_claim': use_csv_for_roles_claim, 'use_csv_for_teams_claim': use_csv_for_teams_claim, 
                'use_csv_for_teams_managed_claim': use_csv_for_teams_managed_claim, 'use_csv_for_ip_address_claim': use_csv_for_ip_address_claim,
                'teams': teams, 'roles': roles}
      
      body = json.dumps(params)

      return APIHelper()._rest_request(url=uri, method=httpmethod, params=body)

   def delete(self, jit_default_id: UUID):
      uri = '{}/{}'.format(self.base_uri, jit_default_id)
      return APIHelper()._rest_request( uri, "DELETE")