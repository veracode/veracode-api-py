#constants.py - contains constant values for lookups

class Constants():
     # translate between annotation types in Findings API v2 and in Mitigations API (XML)
     ANNOT_TYPE = {"APPDESIGN":"appdesign",\
          "NETENV": "netenv",\
          "OSENV":"osenv",\
          "APPROVED":"accepted",\
          "REJECTED":"rejected",\
          "FP":"fp", \
          "LIBRARY":"library", \
          "ACCEPTRISK": 'acceptrisk'}

     AGENT_TYPE = [ "CLI", "MAVEN", "GRADLE", "JENKINS", "BAMBOO", "CIRCLECI", "CODESHIP", "PIPELINES", "TRAVIS", "WINDOWSCI" ]

     SCA_EVENT_GROUP = [ 'WORKSPACE', 'AGENT', 'SCAN', 'PROJECT', 'RULES']

     REGIONS = {
          'global': {
               'base_xml_url': 'https://analysiscenter.veracode.com/api',
               'base_rest_url': 'https://api.veracode.com/'
          },
          'eu': {
               'base_xml_url': 'https://analysiscenter.veracode.com/eu',
               'base_rest_url': 'https://api.veracode.eu/'
          },
          'fedramp': {
               'base_xml_url': 'https://analysiscenter.veracode.us/api',
               'base_rest_url': 'https://api.veracode.us/'
          }
     }