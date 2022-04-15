#collections.py - API class for Collections API calls

import json
from urllib import parse
from uuid import UUID

from .apihelper import APIHelper

class Collections():
   compliance_titles = {
      'DID_NOT_PASS': 'Did Not Pass',
      'PASSED': 'Passed',
      'CONDITIONAL_PASS': 'Conditional Pass',
      'NOT_ASSESSED': 'Not Assessed',
      'NOT_EVALUATED': 'Not Evaluated',
      'out_of_compliance': 'Out of Compliance',
      'within_grace_period': 'Within Grace Period',
      'compliant': 'Compliant'
   }

   #public methods
   def get_all(self):
      request_params = {}
      return self._get_collections(request_params)

   def get_by_name(self,collection_name: str):
      params = {"name": parse.quote(collection_name)}
      return self._get_collections(params)

   def get_by_business_unit(self,business_unit_name: str):
      params = {"business_unit": parse.quote(business_unit_name)}
      return self._get_collections(params)

   def get_statistics(self):
      return APIHelper()._rest_request("appsec/v1/collections/statistics","GET")

   def get(self,guid: UUID):
      uri = "appsec/v1/collections/{}".format(guid)
      return APIHelper()._rest_request(uri,"GET")

   def get_assets(self,guid: UUID):
      uri = "appsec/v1/collections/{}/assets".format(guid)
      return APIHelper()._rest_paged_request(uri,"GET","assets",params={})

   def create(self,name: str,description: str="",tags='',business_unit_guid: UUID=None,custom_fields=[],assets=[]):
      return self._create_or_update(method="CREATE",name=name,description=description,
                  tags=tags,business_unit_guid=business_unit_guid,custom_fields=custom_fields,assets=assets)

   def update(self,guid: UUID,name: str,description: str="",tags: str="",business_unit_guid: UUID=None,custom_fields=[],assets=[]):
      return self._create_or_update(method="UPDATE",name=name,description=description,
                  tags=tags,business_unit_guid=business_unit_guid,custom_fields=custom_fields,assets=assets,guid=guid)

   def delete(self,guid: UUID):
      uri = "appsec/v1/collections/{}".format(guid)
      return APIHelper()._rest_request(uri,"DELETE")

   #private methods

   def _get_collections(self,params):
      return APIHelper()._rest_paged_request("appsec/v1/collections","GET","collections",params=params)

   def _create_or_update(self,method,name: str,description: str="",tags: str="",business_unit_guid: UUID=None,custom_fields=[],assets=[],guid: UUID=None):
      if method == 'CREATE':
         uri = 'appsec/v1/collections'
         httpmethod = 'POST'
      elif method == 'UPDATE':
         uri = 'appsec/v1/collections/{}'.format(guid)
         httpmethod = 'PUT'
      else:   
         return

      payload = {"name": name, "description": description}
      if tags != '':
         t = {'tags': tags}
         payload.update(t)
      if business_unit_guid != None:
         bu = {'business_unit': {'guid': business_unit_guid} }
         payload.update(bu)
      if len(custom_fields) > 0:
         cf = {'custom_fields': custom_fields}
         payload.update(cf)
      if len(assets) > 0:
         asset_list = []
         for asset in assets:
               this_asset = {'guid':asset,'type': 'APPLICATION'}
               asset_list.append(this_asset)
               al = {'asset_infos': asset_list}
               payload.update(al)
      return APIHelper()._rest_request(uri,httpmethod,params={},body=json.dumps(payload))