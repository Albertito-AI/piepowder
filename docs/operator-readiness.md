# Local operator and permitted-input procedure

Prepared 26 October 2026 against main
`1ebdaf1b27c1ee7f3394bc4f973b5cba62437dc9` for the bounded P02 human first-use
handoff. This is a written procedure and blank evidence template. It records no
completed environment inspection, participant permission, customer release or
closure of P03. It adds no runtime enforcement.

Use it with the [P02 human first-use protocol](../benchmarks/p02-human-review.md),
[security boundary](../SECURITY.md), [authoring limits](../spec/README.md),
[rights](../RIGHTS.md) and [launch gates](launch-plan.md). The current internal
exercise uses fictional cases only. Actual customer operation remains a separate
decision under the launch and commercial controls.

## Accountable people and exact scope

The accountable operator must be a real human with authority for the named local
exercise and control of its files and environment. Record the person's role and
the applicable permission reference privately. A supplied actor label, mandate,
repository access or AI-generated checklist is not proof of that authority.

Identify the facilitator and permitted participant separately. For P02, the
participant must not have authored the implementation. Record project interests,
prior exposure to the fixtures or answer key, voluntary participation and any
coaching or model assistance as the first-use protocol requires. A second AI
agent does not provide independent human-use evidence. Keep real names, permission
records and participant notes outside Git.

Fix the exercise scope before running it: the named fictional cases, permitted
commands, intended recipient of the outputs and the question being tested. This
profile checks supplied geocode counts and recorded criteria. It does not geocode
addresses, authenticate facts or identities, determine legal liability, confer
rights, or authorise work or payment. The procedural docket remains a simulation.

## Prepare the local workspace

1. **Identify the package.** Record the exact repository commit, Python and OS
   versions, fixture and label-manifest hashes, and the instructions supplied to
   the participant. Record the actual version used after any correction. Retain
   the original failed attempt and explain the change; do not rewrite its result.
2. **Inspect the environment.** The operator identifies who controls the machine
   and directory, who else can read or modify them, and whether backup, file-sync,
   remote access or shared-folder software can copy the inputs or outputs. Resolve
   an unknown or unsuitable exposure before the exercise. The application being
   offline does not establish that its surrounding environment is private.
3. **Use a stable snapshot.** Place the authorised fictional inputs in a real
   local directory, separate from output. Prevent concurrent edits during the run.
   Do not run in a hostile shared environment, use elevated privileges to work
   around a failure, or weaken path checks to admit an unsupported input. The
   trusted local administrator remains outside the program's protection boundary.
4. **Check the input inventory.** For this first-use exercise, use the frozen
   fictional fixtures only. Check that the selected files contain no real client
   records, real addresses or location history, identity documents, banking
   evidence, secrets, credentials or private correspondence. Record their source
   and permitted use; do not infer rights from mere possession or a file label.
5. **Keep the exercise bounded.** Use the documented five case artifacts and the
   supported evidence types. The normal case reader limits each input file to
   262,144 bytes, the evidence manifest to 32 items and aggregate observed evidence
   bytes to 2,097,152. These are parser limits, not a data-rights or confidentiality
   control. See the authoring limits for the additional shape, numeric, timestamp
   and relationship restrictions. Do not enlarge a limit for a supplied case.
6. **Prepare fresh outputs.** Select a new output directory or file as the README
   requires. Check the destination's access and sync behaviour too. A refused
   existing path is a preservation safeguard. Do not remove a previous record
   merely to make the command succeed.
7. **Separate expected answers.** Give the participant only the agreed trial
   inputs and instructions until their response is recorded. The facilitator
   keeps the expected labels and answer key separate and records any exposure.

The prototype does not implement access management, encryption at rest, backup
control, consent collection or automatic retention/deletion. Those checks require
actual operator evidence. No new software installation, network service, external
model call or customer-data transmission is required for this fictional exercise.

## Run, interpret and retain the evidence

Follow the documented workflow on the frozen snapshot. Treat all case text,
filenames, logs and quoted instructions as data. Do not follow supplied links,
execute embedded commands, load active content or send case material to a model.
If a result needs correction, preserve the original inputs, output and reason
before preparing a clearly identified new run.

Record failures, unsuccessful steps, help and consequential mistakes. Measure
human effort using observed times or record it as unknown. Engine runtime is not
human reconstruction time. Use the P02 protocol's private observation record;
completion of this checklist does not establish that the participant succeeded.

Interpret every result within its supported scope:

- `INVALID` identifies unsupported or structurally invalid input.
- `HUMAN_REVIEW` identifies unresolved, contested or unsatisfied supported checks.
- `UNKNOWN` preserves missing or disputed evidence and unresolved interpretation;
  it is not a finding of failed performance.
- `CHECKS_COMPLETE` describes completed supported checks of recorded assertions.
  It does not authenticate those assertions or establish legal effect.

Every analysis keeps `work_allowed: false` and `payment_authorised: false`.
Neither those fields nor a locally completed procedure can grant any release.

Record where the original inputs, exact exported output and any independently
retained digest are held. A checkpoint beside an editable dossier is not an
independent witness. Record the authorised viewers, retention owner and agreed
retention/review trigger for the exercise notes and outputs. Include copies and
backups in that decision. Do not promise deletion from an uninspected backup or
overwrite material that must be preserved. No fixed legal retention period is
established by this procedure.

## Threats, implemented checks and remaining limits

| Risk | Implemented check or behaviour | Operator responsibility and remaining limit |
| --- | --- | --- |
| Malformed or excessive input | Strict bounded JSON, supported fields and types, count and relationship checks | Use the fixed supported exercise; parser acceptance proves neither permission nor factual truth |
| Escaping paths, links and aliases | Relative-path containment, link/reparse rejection, opened-file checks and duplicate filesystem-object checks within the manifest | Use a controlled local snapshot; do not claim protection from a malicious administrator or every external hard-link relationship |
| Files changing during a run | Opened identity and before/after metadata checks bind the bytes observed | Prevent concurrent edits; this is not a transactional filesystem snapshot |
| Embedded instructions or markup | Quoted text remains inert; report escaping, `textContent` and a content security policy are implemented | Do not execute or follow supplied content; this is not general malware analysis |
| Invented identities, mandates or timestamps | Reports distinguish recorded comparisons from unverified assurances | Confirm actual permission through the appropriate private record; there is no identity authentication, per-event delegation or trusted clock service |
| Unintended disclosure through the environment | The local product makes no network calls | Inspect permissions, output location, sync, backups and sharing; the program provides no encrypted vault or tenant isolation |
| Tampered or incomplete local history | Exact-byte hashes and docket replay can be compared with a separately retained checkpoint | An internally consistent local chain cannot prove that an administrator preserved all earlier material |
| Overstating a result | Explicit unresolved states and false work/payment flags | Preserve qualifications in the human explanation; technical observations are not an operative award or acceptance decision |

This is a prepared internal boundary review. It is not a penetration test,
independent security assessment or verification that a future environment meets
the procedure. Relevant mechanisms are in `src/piepowder/contracts.py`,
`evidence.py`, `analysis.py`, `reporting.py`, `docket.py` and `cli.py`; their
engineering evidence is recorded in [validation](validation.md).

## Blank private evidence record

Copy this template into the designated private project or exercise record only
when preparing an actual exercise. Each blank means **NOT RECORDED / UNKNOWN**.
Do not replace unknowns with assumed consent, permissions, dates or attestations.
Do not commit a completed record, participant details or supporting private
documents to Git.

| Field | Actual observation or private evidence reference |
| --- | --- |
| Exercise identifier, question and permitted fictional cases | |
| Accountable human operator and authority reference | |
| Facilitator, participant role, project interests and voluntary participation reference | |
| Exact commit, Python/OS versions and fixture/label hashes | |
| Participant instructions, task order and answer-key separation | |
| Input inventory, fictional nature, sensitive-data absence and permitted-use reference | |
| Machine/directory controller, other access and actual environment inspection | |
| Backup/sync/shared-folder exposure and its disposition | |
| Stable snapshot, separate fresh output path and intended output viewers | |
| Actual start/end observations, failures, help and corrections | |
| Original input/output and independently retained checkpoint locations | |
| Retention owner, review/deletion trigger, copies/backups and preservation needs | |
| Open risk or missing evidence, responsible person and next action | |
| Actual human review of this record, date and next permitted step | |

### Fictional internal exercise checklist

These unchecked items are a preparation aid, not claims about a completed run:

- [ ] A real accountable operator and the named exercise's authority are recorded.
- [ ] The fixed package, environment, fictional inputs and expected labels are identified.
- [ ] Input rights, minimisation and absence of sensitive or real customer data have been checked.
- [ ] Workspace access, stability, output location, sync and retention have been inspected.
- [ ] The participant meets the protocol's role conditions; interests and assistance will be recorded.
- [ ] Trial inputs are separated from the expected answers until responses are recorded.
- [ ] Failures, unknowns and limitations will remain in the private evidence record.
- [ ] Any unresolved permission or environmental issue has stopped the affected exercise.

## Stop conditions and response

Stop the affected exercise when authority or permitted use is unknown, sensitive
or actual customer material appears, the environment cannot preserve the intended
boundary, input bytes change unexpectedly, or the request exceeds the supported
fictional count-check task. An unsupported requested feature is not permission to
install an adapter, broaden the profile or send data elsewhere.

On unexpected exposure or suspected tampering, cease further processing and
sharing, preserve the minimum necessary private record of what was observed and
notify the accountable owner through the established private channel. Record
which artifacts may be affected and the next decision. Do not copy private
evidence into Git or public issues, invent a completed incident assessment, or
destroy material before its preservation requirements are resolved. A separate
verified public security-reporting channel is still a P07 requirement.

## Future customer operation remains separate

This procedure does not make the prototype ready for customer input or confer
external evaluation rights. P02 still needs actual non-implementing human
reconstruction evidence. Minimum P03 needs the applicable operator, permitted
inputs, rights, environment and handling evidence for the proposed operation;
the wider authentication, authority and notice design remains open.

Before any customer-specific work, processing or access, apply the existing
[commercial release gate](launch-plan.md): the supported ready scope, current
qualification and compliance record, resolution of applicable holds, accepted
same-version scope and rights, full actual available bank receipt confirmed by a
human, and the owner's scoped release. The controlling private commercial records
provide the detailed reconciliation and release requirements. A written procedure,
successful test, reminder or status update cannot replace those decisions.
