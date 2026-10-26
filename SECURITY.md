# Security and trust boundary

Version 0.1.0a1 is an offline research prototype for local fictional cases.
The person controlling the computer and the case directory is a trusted local
administrator. The program is not a network service or a secure multi-tenant vault.

The [local operator procedure](docs/operator-readiness.md) makes the permitted
fictional first-use exercise and required private evidence record explicit. It
documents human handling responsibilities; it adds no runtime enforcement and
does not close the customer-readiness or wider P03 trust gates.

The parser bounds JSON size, depth, item counts and numeric range. It rejects
duplicate object keys, non-integer JSON numbers and unsupported fields. Evidence
must use a portable relative path under the case's `evidence/` directory. The reader
rejects traversal, links, reparse points, duplicate paths and duplicate filesystem
objects, and checks the opened regular file before and after reading.

These checks bind the bytes observed during a local run. They are not a filesystem
transaction against a hostile administrator. Place case snapshots in a stable
directory. The v0.1 trust model does not claim resistance to an administrator
who rewrites every artifact and every retained checkpoint.

Neither hashes nor actor labels authenticate principals, the authority delegated to
an agent, factual evidence or time. Per-event delegation, credential compromise,
key revocation, trusted timestamping, external witnesses, encryption at rest,
tenant isolation and access control remain production requirements.

Quoted text is retained by digest and triggers human review. It is never executed,
sent to a model or used as an instruction. The HTML report escapes embedded data,
renders supplied values through textContent and has a content security policy.
No live URLs, scripts or commands from a case are followed.

The procedural simulator rejects unsupported execution and award actions. It
retains late answers, records timeout review requirements and requires a logged
reopening before the closed record can be reconsidered. Local acknowledgements
are recorded claims, not proof of legally sufficient notice.

Use only synthetic or expressly permitted non-sensitive material during internal
development. Do not place vulnerability details or private evidence in public
issues. Report a vulnerability privately to the repository owner through an
established private channel. A dedicated confidential reporting route must be
verified before public release; this file does not claim that one is configured.
