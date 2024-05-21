# SCA Agent

The following methods call Veracode REST APIs and return JSON.

_Note_: SCA APIs must be called with a human user, since the SCA Agent APIs do not currently support being called by an API Service User.

## Workspaces, Projects, Issues, and Agents

- `Workspaces().get_all(include_metrics(opt))`: get a list of SCA Agent workspaces for the organization. The `include_metrics` parameter can add counts of issues and other attributes in the response, at some cost to performance, and defaults to `False`.
- `Workspaces().get_by_name(name)`: get a list of SCA Agent workspaces whose name partially matches `name`.
- `Workspaces().create(name)`: create an SCA Agent workspace named `name`. Returns the GUID for the workspace.
- `Workspaces().add_team(workspace_guid,team_id)`: add the team identified by `team_id` (int) to the workspace identified by `workspace_guid`.
- `Workspaces().get_teams(workspace_guid(opt))`: get a list of teams. If no `workspace_guid` is provided, return all available teams.
- `Workspaces().remove_team(workspace_guid,team_id)`: remove the team identified by `team_id` (int) from the workspace identified by `workspace_guid`.
- `Workspaces().delete(workspace_guid)`: delete the workspace identified by `workspace_guid`.
- `Workspaces().get_projects(workspace_guid,project_name(opt))`: get a list of projects for the workspace identified by `workspace_guid`.
- `Workspaces().get_agents(workspace_guid)`: get a list of agents for the workspace identified by `workspace_guid`.
- `Workspaces().get_agent(workspace_guid,agent_guid)`: get the agent identified by `agent_guid` in the workspace identified by `workspace_guid`.
- `Workspaces().create_agent(workspace_guid,name,agent_type(opt))`: create an agent in the workspace identified by `workspace_guid`. Default for `agent_type` is `CLI`.
- `Workspaces().delete_agent(workspace_guid,agent_guid)`: delete the agent identified by `agent_guid`.
- `Workspaces().get_agent_tokens(workspace_guid, agent_guid)`: get token IDs for the agent identified by `agent_guid` in the workspace identified by `workspace_guid`.
- `Workspaces().get_agent_token(workspace_guid, agent_guid, token_id)`: get the token ID identified by `token_id`.
- `Workspaces().regenerate_agent_token(workspace_guid, agent_guid)`: regenerate the token for the agent identified by `agent_id`.
- `Workspaces().revoke_agent_token(workspace_guid, agent_guid, token_id)`: revoke the token identified by `token_id`.
- `Workspaces().get_issues(workspace_guid, branch(opt), direct(opt), created_after(opt), ignored(opt), vuln_method(opt), project_id (opt array))`: get the list of issues for the workspace identified by `workspace_guid`.
- `Workspaces().get_issue(issue_id)`: get the issue identified by `issue_id`.
- `Workspaces().get_scan(scan_id)`: get the scan identified by `scan_id` (returned in `get_issue`).
- `Workspaces().get_libraries(workspace_guid,unmatched(bool,opt))`: get the libraries associated with the workspace identified by `workspace_guid`.
- `Workspaces().get_library(library_id)`: get the library identified by `library_id` (e.g. "maven:commons-fileupload:commons-fileupload:1.3.2:")
- `Workspaces().get_vulnerability(vulnerability_id)`: get the vulnerability identified by `vulnerability_id` (an integer value, visible in the output of `get_issues`).
- `Workspaces().get_license(license_id)`: get the license identified by `license_id` (a string, e.g. "GPL30").
- `Workspaces().get_events(date_gte,event_group,event_type)`: get the audit events for the arguments passed. Be careful with the arguments for this and try to limit by date as it will fetch all pages of data, which might be a lot.

## Component Activity

- `ComponentActivity().get(component_id)`: get the activity for the component identified by `component_id` (similar to `library_id` above, e.g. "maven:net.minidev:json-smart:1.3.1").

## SBOM

- `SBOM().get(app_guid,format(opt),linked(opt),vulnerability(opt),dependency(opt))`: generate an SBOM in either CycloneDX (default) or SPDX format for the application represented by `app_guid`. Get the `app_guid` from the Applications API. The following options are available:
  - `linked` (CycloneDX only): if `True`, returns an SBOM based on the linked SCA Agent project. Defaults to `False`.
  - `vulnerability`: if `True`, returns an SBOM containing vulnerability information. Defaults to `True`.
  - `dependency` (SPDX only): if `True`, returns an SBOM that includes dependency information. Defaults to `True`.
- `SBOM().get_for_project(project_guid,format(opt),vulnerability(opt))`: generate an SBOM in CycloneDX (default) or SPDX format for the SCA Agent project represented by `project_guid`. Get the `project_guid` from the SCA Agent API (e.g. `get_projects(workspace_guid)`). The following options are available:
  - `vulnerability`: if `True`, returns an SBOM containing vulnerability information. Defaults to `True`.
  - `dependency` (SPDX only): if `True`, returns an SBOM that includes dependency information. Defaults to `True`.
- `SBOM().scan(sbom)`: (EXPERIMENTAL) Scan an SBOM (pass the filename, including absolute path, as the `sbom` parameter) and return an updated SBOM with additional vulnerability information from the Veracode SCA Database.

## Application Info

_Note_: You can also access these methods from the `SCAApplications` class.

- `SCAApplications().get_projects(app_guid)`: get the list of linked SCA projects for an application. (This API call is also available on the SCAApplications object as `SCAApplications().get_projects()`.)
- `SCAApplications().link_project(app_guid, project_guid)`: link the application to the project. (This API call is also available on the SCAApplications object as `SCAApplications().link_project()`.)
- `SCAApplications().unlink_project(app_guid, project_guid)`: unlink the application from the project. (This API call is also available on the SCAApplications object as `SCAApplications().unlink_project()`.)
- `SCAApplications().get_annotations(app_guid, annotation_type, annotation_reason(opt), annotation_status(opt),cve_name(opt), cwe_id(opt), severities(opt array), license_name(opt), license_risk(opt))`: get the list of annotations (mitigations and comments) for an application. (This API call is also available on the SCAApplications object as `SCAApplications().get_annotations()`.)
- `SCAApplications().add_annotation(app_guid, action, comment, annotation_type, component_id, cve_name (required for VULNERABILITY type), license_id (required for LICENSE type))`: add an annotation (mitigation or comment) to an SCA vulnerability or license finding. Note that ability to APPROVE or REJECT requires the mitigation approver role. (This API call is also available on the SCAApplications object as `SCAApplications().add_annotation()`.)

[All docs](docs.md)
