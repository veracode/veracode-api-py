from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CWE:
    id: int
    name: str
    href: str


@dataclass
class FindingCategory:
    id: int
    name: str
    href: str


@dataclass
class FindingDetails:
    severity: int
    cwe: CWE
    file_path: str
    file_name: str
    module: str
    relative_location: int
    finding_category: FindingCategory
    procedure: str
    exploitability: int
    attack_vector: str
    file_line_number: int


@dataclass
class FindingStatus:
    first_found_date: datetime
    status: str
    resolution: str
    mitigation_review_status: str
    new: bool
    resolution_status: str
    last_seen_date: datetime


@dataclass
class FindingsEntity:
    issue_id: int
    scan_type: str
    description: str
    count: int
    context_type: str
    context_guid: str
    violates_policy: bool
    finding_status: FindingStatus
    finding_details: FindingDetails
    build_id: int

    _element: str = 'findings'
