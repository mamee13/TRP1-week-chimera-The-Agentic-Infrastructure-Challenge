# Vulnerability Disclosure Policy & Flow

Purpose

This document describes how to report security vulnerabilities to Project Chimera and how we will handle reports.

Contact

- Email: mamaruyirga1394@gmail.com

How to Report

1. Send a private email to `mamaruyirga1394@gmail.com` (do NOT open a public GitHub issue).
2. Mark the email as sensitive.
3. Include the following in your report:
   - A short title and affected component (e.g., `mcp-client: unauthenticated command injection`)
   - Detailed reproduction steps and minimal PoC code or scripts
   - Exact versions and environment information (OS, Python version, dependency versions)
   - Your contact info and preferred disclosure timeline
   - Any suggested mitigation or fixes (optional)

What We Will Do

- Acknowledge receipt within 48 hours.
- Triage and classify severity within 4 business days.
- Work on mitigation and provide periodic updates while coordinating with the reporter.
- Coordinate public disclosure and CVE assignment where appropriate.

Timeline Expectations

- Acknowledgement: within 48 hours
- Initial triage: within 4 business days
- Fix deployment (critical): as soon as practicable; non-critical fixes prioritized on next maintenance cycle
- Public disclosure: coordinated with reporter, typically after fix is deployed or a mitigation is available

Coordinated Disclosure & CVE

- We welcome coordinated disclosure. If you request a CVE, include that request in your initial email.
- We will assist with CVE assignment for confirmed vulnerabilities.

Acknowledgement & Credit

- We will credit reporters who request acknowledgement, unless anonymity is requested.
- If we publicly acknowledge a reporter, we will confirm the wording before publishing.

Sensitive Data & Safe Harbor

- Do not exfiltrate or publish sensitive user data while testing. If sensitive data is discovered, report it immediately and follow our instructions.
- We will provide a safe-harbor statement to security researchers acting in good faith according to this policy.

Contact and Escalation

- Primary contact: mamaruyirga1394@gmail.com
- If you do not receive a timely response, please resend and mark `URGENT` in the subject line.

Notes


- This policy complements `SECURITY.md` and should be referenced in repository documentation.
