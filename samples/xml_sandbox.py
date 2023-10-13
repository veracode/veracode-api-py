# a simple sample to get the sandbox id
from veracode_api_py import XMLAPI
import xml.etree.ElementTree as ET

xmlApi = XMLAPI()
appListXml = xmlApi.get_app_list()
appList = ET.fromstring(appListXml)

# CHANGE BELOW TO SEARCH FOR OTHER APP NAMES / SANDBOXES
searchAppName = "VeraDemo"
searchSandboxName = "POJOs"

foundAppId = 0
for app in appList:
    appName = app.get("app_name")
    appId = app.get("app_id")
    if searchAppName == appName:
        foundAppId = appId
        break

if foundAppId == 0:
    raise Exception("Did not find app id!")

sandboxListXml = xmlApi.get_sandbox_list(foundAppId)
sandboxList = ET.fromstring(sandboxListXml)

foundSandboxId = 0
for sandbox in sandboxList:
    sandboxName = sandbox.get("sandbox_name")
    sandboxId = sandbox.get("sandbox_id")
    if searchSandboxName == sandboxName:
        foundSandboxId = sandboxId
        break

if foundSandboxId == 0:
    raise Exception("Did not find sandbox id!")

print("App '" + searchAppName + "' ID: " + foundAppId + "\nSandbox '" + searchSandboxName + "' ID: " + foundSandboxId)