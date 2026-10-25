# Security Log Analyzer — Requirements

## Acceptance criteria

### AC-01: Five-second boundary is included

**Given** a valid CSV containing three failed login attempts from the same source IP at:

- `2026-10-25T12:00:00Z`
- `2026-10-25T12:00:02Z`
- `2026-10-25T12:00:05Z`

**When** the analyzer processes the file,

**Then:**

- Exactly one suspicious-login alert is produced.
- The alert includes all three failures.
- Its first and last timestamps are five seconds apart.
- It identifies the source IP and affected accounts.
- The summary reports three failed attempts, zero successful attempts, and zero invalid rows.

### AC-02: Failed attempts cannot contribute to multiple alerts

**Given** a valid CSV containing six failed attempts from the same source IP at seconds **0, 1, 2, 4, 8, and 9** of the same minute,

**When** the analyzer processes the file chronologically,

**Then:**

- Exactly two alerts are produced.
- The first contains the attempts at seconds **0, 1, and 2**.
- The second contains the attempts at seconds **4, 8, and 9**.
- No attempt appears in both alerts.
- The summary still counts all six failed attempts.

### AC-03: Header-only input produces an empty report

**Given** a CSV containing only this valid header:

`timestamp,source_ip,username,outcome`

**When** the analyzer processes the file,

**Then:**

- Processing finishes without an exception.
- All event counts and IP counts are zero.
- The invalid-row count is zero.
- No suspicious-login alerts are produced.
- A file warning states: “No event records found. Check whether this is expected.”
- The report is printed in the terminal and saved as JSON.

### AC-04: Alerts and unresolved status are tracked separately

For one IP, when failures occur close enough to form the required alert groups:

| Sequence | Alert count | Unresolved IP count |
|---|---:|---:|
| Three failures | 1 | 0 |
| Four failures | 1 | 1 |
| Six failures | 2 | 0 |
| Seven failures | 2 | 1 |
| Three failures, then success | 1 | 0 |
| Four failures, then success | 1 | 0 |
| Four failures, then success, then one failure | 1 | 1 |

All failures and successes remain included in the overall event totals.

## Input contract

The MVP analyzes one application’s CSV file per manual run. The user supplies its path.

### Required columns

| Column | Valid value |
|---|---|
| `timestamp` | A real UTC date and time in the exact format `YYYY-MM-DDTHH:MM:SSZ` |
| `source_ip` | A valid IPv4 or IPv6 address |
| `username` | A nonblank account name |
| `outcome` | Exactly `success` or `failure` |

Valid events are processed chronologically. Events with identical timestamps retain their original CSV order.

### File-level errors

Reject the file with a clear message if:

- The path does not exist or cannot be read.
- The supplied path is a directory.
- The header is missing or lacks a required column.

Do not present a failed read as a successful analysis with zero events.

### Invalid records

Skip records with missing required values, invalid timestamps, invalid IP addresses, blank usernames, or unsupported outcomes.

Report each rejected record’s CSV line number and reason. Continue processing valid records.

Always include the invalid-record count in the report. Add a data-quality warning when the count reaches or exceeds a configurable threshold:

- Default threshold: 20 invalid records.
- Small test datasets may configure the threshold to 5.

The warning indicates incomplete or unsuitable input data; it does not claim a specific cause.

### Header-only files

A correct header with no event records is accepted. Produce zero totals and a warning that no event records were found.  


## Analysis requirements

### Suspicious-login detection

- Analyze failures separately for each source IP, across all usernames.
- Raise an alert when three eligible failures occur within five seconds.
- Include the exact five-second boundary.
- Remove older failures from alert consideration, while retaining them in overall totals.
- Successful logins do not reset the detection window.
- Once three failures form an alert, those events cannot contribute to another alert.
- Subsequent failures can form a new alert.

Each alert contains:

- Source IP.
- Distinct affected usernames.
- First and last failure timestamps.
- Number of failures included.

Alerts describe suspicious activity requiring investigation; they do not establish that an attack occurred.

### Summary

Report:

- Total valid events.
- Successful login count.
- Failed login count, including failures included in alerts.
- Number of distinct IPs with successful logins.
- Number of distinct IPs with unresolved failures.
- Invalid-row count.
- Alert count.

### Alert history and unresolved failures

A failure is unresolved until either:

- It is included in an alert, or
- A later successful login from the same IP clears its unresolved status, regardless of username.

An IP is counted once in the unresolved-failure IP count if it has any unresolved failures.

Successful logins never remove alerts or change historical event totals. They also do not reset the five-second detection window.

A new failure after a successful login makes the IP unresolved again, unless that failure immediately completes an alert.

An IP may appear in both the successful-IP count and unresolved-failure-IP count.



## Output requirements

Print a readable terminal report and save a JSON report containing the same findings:

- Summary counts.
- Suspicious-login alerts.
- Invalid-row line numbers and reasons.
- File and data-quality warnings.

Identify the analyzed input file and the detection settings in the report.

## Quality requirements

- Preserve the source CSV without modification.
- Produce consistent findings for identical input and settings.
- Handle expected input errors with clear messages rather than unhandled tracebacks.
- Distinguish rejected input from successfully analyzed input containing zero events.
- Keep input loading, validation, detection, and reporting responsibilities separate.