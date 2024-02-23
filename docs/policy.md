# Policy

The following methods call Veracode REST APIs and return JSON.

_Note_: You can also access these methods from the `Policies` class.

- `Policies().get_all()`: Get a list of available policies.
- `Policies().get(guid)`: get information for the policy corresponding to `guid`.
- `Policies().create(name,description,vendor_policy(opt),finding_rules(opt),scan_frequency_rules(opt),grace_period_rules(opt))`: create a policy
- `Policies().update(guid,name,description,vendor_policy(opt),finding_rules(opt),scan_frequency_rules(opt),grace_period_rules(opt))`: edit a policy
- `Policies().delete(guid)`: delete a policy
- `Policies().format_finding_rule(rule_type,scan_types=[],rule_value='')`: formatting utility to create a valid finding rule based on the input. For more information about finding rules, see the [finding rules documentation](https://docs.veracode.com/r/Policy_API_Rules_Properties):
    - `rule_type`: one of `FAIL_ALL`, `CWE`, `CATEGORY`, `MAX_SEVERITY`, `CVSS`, `CVE`, `BLACKLIST`, `MIN_SCORE`, `SECURITY_STANDARD`, `LICENSE_RISK`
    - `scan_types`: an array of scan types to which the rule applies. Valid values are `STATIC`, `DYNAMIC`, `MANUAL`, `SCA`
    - `rule_value`: a string representing the value for the rule
- `Policies().format_scan_frequency_rule(scan_type,frequency)`: formatting utility to create a valid scan frequency rule based on the input:
    - `scan_type`: valid values are `STATIC`, `DYNAMIC`, `MANUAL`, `SCA`
    - `frequency`: valid values are `NOT_REQUIRED`, `ONCE`, `WEEKLY`, `MONTHLY`, `QUARTERLY`, `SEMI_ANNUALLY`, `ANNUALLY`, `EVERY_18_MONTHS`, `EVERY_2_YEARS`, `EVERY_3_YEARS`
- `Policies().format_grace_periods(sev5: int, sev4: int, sev3: int, sev2: int, sev1: int, sev0: int, score: int, sca_blocklist: int)`: formatting utility to create a valid grace period rule. Each argument represents a number of days in the grace period for the findings of the given severity or for the Veracode score (see [grace period documentation](https://docs.veracode.com/r/c_policy_grace_period) for more info).

[All docs](docs.md)
