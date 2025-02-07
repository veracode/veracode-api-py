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
     
     SCA_ANNOTATION_TYPE = ["VULNERABILITY", "LICENSE"]

     SCA_ANNOT_ACTION = ["BYENV", "BYDESIGN", "FP", "ACCEPTRISK", "LEGAL", "COMMERCIAL", "EXPERIMENTAL", "INTERNAL", "APPROVE", "REJECT", "COMMENT"]

     SCA_ANNOT_STATUS = ["PROPOSED", "ACCEPTED", "REJECTED"]

     SCA_LICENSE_RISK = [ "HIGH", "MEDIUM", "LOW", "NON_OSS", "UNRECOGNIZED"]

     AGENT_TYPE = ["CLI", "MAVEN", "GRADLE", "JENKINS", "BAMBOO", "CIRCLECI", "CODESHIP", "PIPELINES", "TRAVIS", "WINDOWSCI"]

     SCA_EVENT_GROUP = [ 'WORKSPACE', 'AGENT', 'SCAN', 'PROJECT', 'RULES']

     SEVERITIES = [ "VERY_HIGH", "HIGH", "MEDIUM", "LOW", "VERY_LOW", "INFORMATIONAL"]

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

     DEV_STAGE = [ 'DEVELOPMENT', 'TESTING', 'RELEASE']

     BUSINESS_CRITICALITY = [ 'VERY HIGH', 'HIGH', 'MEDIUM', 'LOW', 'VERY LOW', 'VERY_HIGH', 'VERY_LOW']

     DAST_TARGET_TYPE = [ 'WEB_APP', 'API']

     DAST_CRAWLER_MODE = [ 'SMART', 'EXHAUSTIVE' ]

     DAST_PROTOCOL = [ 'HTTP', 'HTTPS']

     DAST_SCAN_TYPE = [ 'QUICK', 'FULL']

     DAST_SCANNERS = [ 'fingerprinting', 'ssl', 'http_header', 'portscan', 'fuzzer', 'sql_injection',
                      'xss', 'file_inclusion', 'deserialization', 'xxe', 'command_injection', 
                      'csrf', 'ldap_injection']
