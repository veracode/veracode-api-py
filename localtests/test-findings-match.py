from veracode_api_py import Applications, Findings

findings = Findings().get_findings('0d782d22-a35f-4520-a07c-197facd98e01')
otherfindings = Findings().get_findings('878e431e-3a1d-4e18-ae21-af59011e743c')
Findings().match(origin_finding=otherfindings[0],potential_matches=findings,approved_matches_only=False)

match_findings = Findings()._create_match_format_policy(findings,'STATIC')
match_other_findings = Findings()._create_match_format_policy(otherfindings,'STATIC')

match_findings_s = [{'cwe': pf['cwe'],
        'source_file': pf['source_file'],
        'line': pf['line']} for pf in match_findings]

match_other_findings_s = [{'cwe': pf['cwe'],
        'source_file': pf['source_file'],
        'line': pf['line']} for pf in match_other_findings]

print(match_findings_s)
print(match_other_findings_s)