from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CWE:
    id: Optional[int]
    name: Optional[str]
    href: Optional[str]


@dataclass
class FindingCategory:
    id: Optional[int]
    name: Optional[str]
    href: Optional[str]


@dataclass
class FindingDetails:
    severity: Optional[int]
    cwe: Optional[CWE]
    file_path: Optional[str]
    file_name: Optional[str]
    module: Optional[str]
    relative_location: Optional[int]
    finding_category: Optional[FindingCategory]
    procedure: Optional[str]
    exploitability: Optional[int]
    attack_vector: Optional[str]
    file_line_number: Optional[int]


@dataclass
class FindingStatus:
    first_found_date: Optional[datetime]
    status: Optional[str]
    resolution: Optional[str]
    mitigation_review_status: Optional[str]
    new: Optional[bool]
    resolution_status: Optional[str]
    last_seen_date: Optional[datetime]


@dataclass
class FindingsEntity:
    issue_id: Optional[int]
    scan_type: Optional[str]
    description: Optional[str]
    count: Optional[int]
    context_type: Optional[str]
    context_guid: Optional[str]
    violates_policy: Optional[bool]
    finding_status: Optional[FindingStatus]
    finding_details: Optional[FindingDetails]
    build_id: Optional[int]

    _element: str = 'findings'
