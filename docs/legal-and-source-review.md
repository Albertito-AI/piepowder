# Legal design and source review

**Review date: 2026-10-25 · Prototype: v0.1**

This record reviews the *Piepowder Agent Judiciary Report* for implementation. It separates the report’s proposed mechanisms from supported legal propositions and the bounded choices for v0.1. It is a source-correction and product-design record, not customer terms or an assessment of a particular party’s rights. The report is research input, not authority for executing contracts, deciding disputes or moving money.

## 1. Human arbitration and cross-border enforcement remain conditional

The report proposes a human arbitration tier and describes its output as enforceable under the New York Convention. The supported formulation is narrower: an award **may qualify** for recognition and enforcement under the Convention and applicable arbitration law.

[Convention Articles II–V](https://sice.oas.org/DISPUTE/COMARB/Intl_Conv/caicnye.asp) preserve questions concerning a valid arbitration agreement, capacity, notice, opportunity to present a case, scope, tribunal composition, procedure, binding status, arbitrability and public policy. A human signature on an AI-generated result does not resolve these issues. The [Ciarb AI Guideline, September 2025, §§8.2–8.4 and 9.1](https://www.ciarb.org/media/bpndtcgu/guideline-on-the-use-of-ai-in-arbitration_updated-sept-2025.pdf) supports independent human judgment and responsibility; it is professional guidance subordinate to applicable law and rules.

**v0.1 choice:** export an evidence and review record, without purporting to issue an arbitral award. A live arbitration route requires a chosen seat, applicable laws, rules, valid consent, qualified decision-maker and defined AI use. No institutional affiliation or universal human-signature enforcement rule is assumed.

## 2. Machine expert determination is an unresolved legal extension

The report proposes binding machine-panel decisions as contractual expert determinations. Courts recognise expert determination and may accord substantial finality to decisions within the agreed remit. [2018 SGHC 229, §§72–73](https://www.elitigation.sg/gd/s/2018_SGHC_229) discusses material departure from instructions and the significance of fraud or collusion. That human-expert authority does not establish the treatment of a multi-model panel.

The label alone cannot settle legal character, valid appointment, permissible remit or review rights. Institutional arbitration is also not automatically an appeal from a private expert decision.

**v0.1 choice:** assessments and decisions are advisory or simulated. Preserve instructions, inputs, versions and disagreements. Before live use, define whether subsequent human review is a fresh merits determination, contractual review or arbitration, and what effect the earlier result has.

## 3. A technical mandate check is not a complete authority ruling

The report would attribute actions within signed mandates to principals and reduce authority disputes to record checks. Signature and scope evidence are useful, but do not conclusively determine identity, capacity, consent, compromised credentials or applicable agency law.

[UNCITRAL’s Model Law on Automated Contracting, Article 7](https://uncitral.un.org/sites/uncitral.un.org/files/2424674e-mlautomatedcontracting-rev1-ebook.pdf) provides an attribution framework; paragraph 4 preserves other law governing its consequences. A model law is not universally operative domestic legislation. Optional Article 8 cannot be presented as a universal unexpected-action defence.

[Quoine v B2C2, [2020] SGCA(I) 2, §§96–99](https://www.elitigation.sg/gd/s/2020_SGCAI_2) addresses deterministic algorithms and relevant programmer/operator knowledge. It does not settle every attribution question for adaptive agents. The report’s universal claim that no court has addressed the newer problem remains unverified.

**v0.1 choice:** separate technical verification from legal authority. Preserve `UNKNOWN` and `DISPUTED`; neither becomes assent, liability or permission to pay.

## 4. The Code’s defaults need agreement and jurisdiction-specific treatment

The report’s acceptance, liability and interpretation defaults are proposals, not a statement of universally applicable law.

**Silence:** initial contractual assent differs from a previously agreed delivery-acceptance procedure. [2017 SGHC 4, §54](https://www.elitigation.sg/gd/s/2017_SGHC_4) explains that silence ordinarily does not suffice, although context and conduct matter. The report also requires rejection against typed criteria where it assumes no acceptance test exists. A live mechanism needs defined delivery, criteria, notice and a suitable review period.

**Liability cap:** a contract-price ceiling is not automatically effective. Singapore UCTA, discussed in [2022 SGHC 39, §§122–124](https://www.elitigation.sg/gd/s/2022_SGHC_39), prohibits limiting death/personal-injury liability resulting from negligence and subjects relevant negligence exclusions and standard terms to reasonableness. The particular contract and applicable mandatory law matter.

**Flagged ambiguity:** allocating an unresolved ambiguity against its drafter is a proposed contractual mechanism. Model disagreement does not establish legal ambiguity. [2016 SGCA 19, §§50–53](https://www.elitigation.sg/gd/s/2016_SGCA_19) distinguishes interpretative difficulty from unresolved ambiguity and treats contra proferentem as residual.

**v0.1 choice:** show defaults as proposals with provenance, version and acceptance status. Escalate conflicts between typed fields and prose. Linter flags request clarification; they do not automatically impose adverse legal consequences. A cap requires review, and silence does not activate acceptance or payment.

## 5. Notice and deadlines need procedural safeguards

The report proposes automatic loss of evidence-submission rights after a response deadline. A dispatch log is not conclusive proof of legally sufficient notice. Defective service, system outages or a justified extension can matter. [Convention Article V(1)(b)](https://sice.oas.org/DISPUTE/COMARB/Intl_Conv/caicnye.asp) makes notice and the opportunity to present a case relevant to enforcement.

**v0.1 choice:** keep notice assertions distinct from verified notice. The current simulator retains late answers, records timeout review and permits logged reopening of the same evidence index. Pause and deadline-extension events need a later versioned design. A timeout does not determine the merits or forfeit legal rights. No execution or escrow event is implemented.

## 6. The amended EU date is supported, but its scope matters

The report’s **2 December 2027** date is supported by the Commission’s current consolidated [AI Act Article 113(c)(i)](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-113): Chapter III Sections 1–3 apply from that date to Article 6(2)/Annex III systems. Other provisions have different application dates.

[Annex III, point 8(a)](https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3) includes relevant AI uses in alternative dispute resolution. [Article 14(1)–(4)](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-14) requires effective human oversight for high-risk systems, including understanding limitations, resisting automation bias, overriding outputs and stopping operation. Human assistance does not automatically remove high-risk classification.

**v0.1 choice:** assess modules separately by intended purpose, users, territory and effects. A deterministic integrity checker and an AI merits evaluator require distinct analysis. Preserve meaningful review and stop controls; a human approval button is not proof of compliance.

## 7. Real-case publication and personal-data processing remain gated

The report proposes publishing anonymised decisions. Removing names does not establish anonymisation or permission to disclose commercial facts, privileged material, third-party data or trade secrets.

Where GDPR applies, Article 22 can affect automated decisions concerning natural persons; a business context does not settle its applicability. [CJEU C-634/21, §§43–58 and 64–68](https://juris.curia.europa.eu/juris/document/document.jsf?cid=1505002&docid=280426&doclang=EN&mode=lst&occ=first&pageIndex=0&part=1) also shows that an output labelled preparatory may still attract scrutiny when another actor relies decisively on it.

**v0.1 choice:** fictional cases, private records, minimal payloads and no external model transmission by default. Future real-case publication requires separate review. Audit integrity does not justify indefinite retention of every underlying document.

## Launch boundary and source limitations

v0.1 supports proposed terms, technical checks, simulated case progression and reviewable exports. Live assent, binding adjudication, funds movement and publication require separate legal, operational and security gates for the selected jurisdictions and service design.

Linked treaty, court and Commission text was opened. UNCITRAL’s Article 7 text was inspected through the official indexed source; direct PDF retrieval returned 403. No comprehensive enactment, subsequent-authority or enforcement-country survey was completed. These limitations preclude universal enforceability or compliance claims.
