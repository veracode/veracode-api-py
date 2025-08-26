from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class Scan:
    scan_type: str
    status: str
    modified_date: datetime
    scan_url: str
    internal_status: str


@dataclass
class BusinessUnit:
    id: int
    name: str
    guid: str


@dataclass
class BusinessOwner:
    name: str
    email: str


@dataclass
class Policy:
    guid: str
    name: str
    is_default: bool
    policy_compliance_status: str


@dataclass
class Team:
    team_id: int
    team_name: str
    guid: str


@dataclass
class CustomField:
    name: str
    value: str


@dataclass
class Settings:
    nextday_consultation_allowed: bool
    static_scan_xpa_or_dpa: bool
    dynamic_scan_approval_not_required: bool
    sca_enabled: bool
    static_scan_xpp_enabled: bool


@dataclass
class Profile:
    name: str
    tags: str
    business_unit: BusinessUnit
    business_owners: List[BusinessOwner]
    archer_app_name: Optional[str]
    enterprise_id: int
    policies: List[Policy]
    teams: List[Team]
    custom_fields: List[CustomField]
    description: str
    settings: Settings
    git_repo_url: Optional[str]
    vendor_rescan: bool
    business_criticality: str


@dataclass
class ApplicationsEntity:
    id: int
    oid: int
    last_completed_scan_date: datetime
    guid: str
    created: datetime
    modified: datetime
    alt_org_id: int
    app_profile_url: str
    scans: List[Scan]
    last_policy_compliance_check_date: datetime
    profile: Profile
    results_url: str

    _element: str = 'applications'
