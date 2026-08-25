from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class Scan:
    scan_type: Optional[str]
    status: Optional[str]
    modified_date: Optional[datetime]
    scan_url: Optional[str]
    internal_status: Optional[str]


@dataclass
class BusinessUnit:
    id: Optional[int]
    name: Optional[str]
    guid: Optional[str]


@dataclass
class BusinessOwner:
    name: Optional[str]
    email: Optional[str]


@dataclass
class Policy:
    guid: Optional[str]
    name: Optional[str]
    is_default: Optional[bool]
    policy_compliance_status: Optional[str]


@dataclass
class Team:
    team_id: Optional[int]
    team_name: Optional[str]
    guid: Optional[str]


@dataclass
class CustomField:
    name: Optional[str]
    value: Optional[str]


@dataclass
class Settings:
    nextday_consultation_allowed: Optional[bool]
    static_scan_xpa_or_dpa: Optional[bool]
    dynamic_scan_approval_not_required: Optional[bool]
    sca_enabled: Optional[bool]
    static_scan_xpp_enabled: Optional[bool]


@dataclass
class Profile:
    name: Optional[str]
    tags: Optional[str]
    business_unit: Optional[BusinessUnit]
    business_owners: Optional[List[BusinessOwner]]
    archer_app_name: Optional[str]
    enterprise_id: Optional[int]
    policies: Optional[List[Policy]]
    teams: Optional[List[Team]]
    custom_fields: Optional[List[CustomField]]
    description: Optional[str]
    settings: Optional[Settings]
    git_repo_url: Optional[str]
    vendor_rescan: Optional[bool]
    business_criticality: Optional[str]


@dataclass
class ApplicationsEntity:
    id: Optional[int]
    oid: Optional[int]
    last_completed_scan_date: Optional[datetime]
    guid: Optional[str]
    created: Optional[datetime]
    modified: Optional[datetime]
    alt_org_id: Optional[int]
    app_profile_url: Optional[str]
    scans: Optional[List[Scan]]
    last_policy_compliance_check_date: Optional[datetime]
    profile: Optional[Profile]
    results_url: Optional[str]

    _element: str = 'applications'
