# Security Log Analyzer

A Python tool for reviewing authentication logs and identifying patterns that warrant investigation.

## Purpose

Authentication logs can contain more activity than an administrator can efficiently review manually. Security Log Analyzer will summarize login outcomes and highlight repeated failures, providing evidence to help administrators decide what to investigate.

Alerts indicate suspicious patterns, not confirmed attacks.

## Target users

System administrators and DevOps engineers responsible for application operations and security. They can use the reports to review authentication activity, investigate unusual login attempts, and identify problems with log data.

## MVP scope

The first release will:

- Analyze one application’s CSV file per manual run.
- Read UTC timestamps, source IPs, usernames, and login outcomes.
- Process valid events chronologically.
- Detect at least three failed login attempts from the same IP within five seconds, including the boundary.
- Prevent the same failed attempt from contributing to multiple alerts.
- Summarize successful and failed attempts, successful IPs, and unresolved-failure IPs.
- Report invalid rows and warn when their count reaches a configurable threshold.
- Print a readable terminal report and save a structured JSON report.

Each suspicious-login alert will include the source IP, affected accounts, first and last attempt times, and failure count.

## Outside the MVP

The first release will not include:

- Scheduled or continuous monitoring.
- Multiple applications analyzed in a single run.
- Automatic discovery of new log files.
- A background service.
- Automated blocking or account remediation.

## Current status

**Milestone 1: Requirements and MVP definition — Completed.**

The local Git repository has been initialized. Requirements and design are being documented; analysis functionality has not yet been implemented.