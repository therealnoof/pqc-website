---
title: "The Regulatory Landscape"
displayTitle: "Chapter 4: The Regulatory Landscape"
section: "Chapters"
chapter: 4
order: 7
words: 4052
readingMinutes: 18
excerpt: "If the first three chapters answered “why should we care?” and “what’s at risk?”, this chapter answers the question that gets CISOs and program managers out of their chairs: “Who says we have to do this, and by when?”"
---

If the first three chapters answered “why should we care?” and “what’s at risk?”, this chapter answers the question that gets CISOs and program managers out of their chairs: “Who says we have to do this, and by when?”

The PQC regulatory landscape is complex and actively evolving. It spans federal law, executive policy, agency-specific mandates, standards body timelines, and international frameworks—each with different enforcement mechanisms and deadlines. This chapter organizes all of it so you can determine exactly which requirements apply to your organization.

## First Principles: Law vs. Policy vs. Guidance

Before we map the specific mandates, we need to establish a critical distinction that the PQC conversation often blurs: **not all mandates are created equal.** Understanding the hierarchy matters because it tells you what survives a change in administration and what doesn’t.

| **Type** | **What It Is** | **Can It Be Rescinded?** | **PQC Examples** |
| --- | --- | --- | --- |
| **Federal Law** | Passed by Congress, signed by the President. Requires an act of Congress to repeal. | **No. Survives any administration change.** | Quantum Computing Cybersecurity Preparedness Act |
| **National Security Memorandum** | Presidential directive on national security policy. Binding on federal agencies. | Yes, by the sitting President. But rarely done. | NSM-10 (not rescinded by Trump admin) |
| **Executive Order** | Presidential directive on federal operations. Binding on executive branch agencies. | Yes. Commonly modified or rescinded by subsequent presidents. | EO 14306 (Trump, June 2025) |
| **OMB Memo** | Implementation guidance from the Office of Management and Budget. Binding on federal agencies. | Yes, by OMB. But typically remains until replaced. | M-23-02 (crypto inventories) |
| **Agency Guidance / Standard** | Recommendations and standards from NIST, NSA, CISA. Compliance often required by federal procurement or accreditation frameworks. | Standards can be revised but rarely fully withdrawn. | NIST IR 8547, CNSA 2.0, CISA PQC product list |

This hierarchy matters enormously. The Quantum Computing Cybersecurity Preparedness Act is **federal law**—no executive order can override it. NSM-10 has not been rescinded. NIST standards are embedded in federal procurement requirements across the entire government. Understanding which mandates are durable versus which are politically contingent is essential for building a migration plan that survives the next election cycle.<sup>1</sup>

## United States: The Federal PQC Framework

### The Quantum Computing Cybersecurity Preparedness Act (Federal Law)

Signed into law on December 21, 2022, this is the **bedrock of US PQC policy**—the one mandate that cannot be rescinded by any president.<sup>2</sup>

The Act requires:

- OMB to issue guidance on migrating federal IT systems to PQC (due within one year of NIST standards publication—approximately August 2025)

- Federal agencies to maintain cryptographic inventories of systems vulnerable to quantum attack

- Agencies to develop and submit PQC migration plans

- Annual progress reports to Congress

Whether OMB actually met the August 2025 statutory deadline for issuing migration guidance remains unclear in the public record as of early 2026. But the legal obligation on agencies to inventory and plan is active regardless.<sup>3</sup>

### NSM-10: The Policy Foundation

National Security Memorandum 10, “Promoting United States Leadership in Quantum Computing While Mitigating Risks to Vulnerable Cryptographic Systems,” was signed by President Biden on May 4, 2022.<sup>4</sup> NSM-10 established the **2035 end-state target** for completing the transition to quantum-resistant cryptography across federal systems.

Key requirements include:

- FCEB agencies submit annual inventories of quantum-vulnerable IT systems

- Agencies develop and submit transition plans with specific timelines

- NSA provides CNSA 2.0 guidance for National Security Systems

- CISA engages critical infrastructure partners on PQC readiness

> **⚠  MANDATE ALERT**
> NSM-10 has not been rescinded by the Trump administration. EO 14306 (June 2025) explicitly references NSM-10 as the foundational document for the PQC transition. The January 20, 2025 mass rescission of Biden-era executive orders did not target NSM-10.

### Executive Order 14306 (June 2025): What Changed

President Trump’s EO 14306, “Sustaining Select Efforts to Strengthen the Nation’s Cybersecurity,” modified the Biden-era PQC framework in important ways.<sup>5</sup> Understanding what was kept, what was removed, and what was added is critical for compliance planning:

**What was preserved:**

- CISA must maintain and regularly update a list of product categories where PQC-capable products are widely available (published January 2026)

- NSA and OMB must issue requirements for TLS 1.3 or successor support by January 2, 2030

- The quantum threat language—including identification of China as the most active cyber threat—was retained verbatim

**What was removed:**

- The requirement for agencies to adopt PQC “as soon as practicable” upon vendor support

- The mandate for agencies to require vendors to implement PQC in procurement

- Provisions for international promotion of NIST algorithm adoption

The practical effect: EO 14306 loosened the federal urgency of PQC adoption while preserving the direction. Agencies retain latitude on implementation pace, but the destination (quantum-resistant cryptography by 2035) remains unchanged.

## CNSA 2.0: The NSA’s Timeline for National Security Systems

For organizations operating in or selling to National Security Systems (NSS) environments—DoD, intelligence community, classified networks—the NSA’s Commercial National Security Algorithm Suite 2.0 is the binding standard.<sup>6</sup> CNSA 2.0 is more aggressive than the general federal timeline:

| **System Category** | **Support & Prefer CNSA 2.0 By** | **Exclusively Use CNSA 2.0 By** | **Notes** |
| --- | --- | --- | --- |
| **Software & firmware signing** | **2025 (now)** | **2030** | Earliest mandatory deadline |
| **Web browsers, servers, cloud** | **2025 (now)** | 2033 |  |
| **Networking (VPNs, routers)** | **2026** | **2030** | F5 BIG-IP, NGINX in scope |
| **Operating systems** | 2027 | 2033 |  |
| **New NSS acquisitions** | **January 1, 2027** | — | All new purchases must be CNSA 2.0 |
| **Niche / constrained devices** | 2030 | 2033 | IoT, PKI systems |
| **Legacy / custom applications** | — | 2033 (update or replace) | Hard deadline |

CNSA 2.0 specifies exact algorithms: **ML-KEM-1024** for key establishment and **ML-DSA-87** for general-purpose digital signatures (Level 5 security). For software and firmware signing specifically, **LMS and XMSS** (stateful hash-based signatures from SP 800-208) are approved for immediate use, with ML-DSA approved once FIPS-validated implementations become available.<sup>7</sup>

## DoW CIO Direction: The November 2025 Memorandum

CNSA 2.0 specifies the algorithms. NSM-10 sets the destination. But for organizations that operate or deliver into Department of War networks, a third document now sits on top of both: the DoW CIO memorandum *Preparing for Migration to Post Quantum Cryptography*, issued November 18, 2025 by Katherine Arrington (Performing the Duties of the CIO).<sup>13</sup>

The memo creates a new, DoW-specific approval gate. Every DoW Component—Services, Combatant Commands, Defense Agencies, and Field Activities—must now coordinate cryptographic migration through a centralized **DoW CIO PQC Directorate**, led by Dr. Britta Hale. Any “engagement” with PQC technology—defined broadly as testing, evaluating, piloting, researching, investing in, prototyping, demonstrating, implementing, integrating, or any planned or actual acquisition—requires two new authorizations issued by the Directorate:

- **Cryptographic intake approval,** before any test, evaluation, pilot, investment, or acquisition begins.

- **Cryptographic deployment approval,** before any PQC-enabling or PQC-related technology is deployed. Deployment approval is informed by Intelligence Community, NIST, and NSA certification outcomes—meaning FIPS 140-3, NIAP Common Criteria, and NSA CSfC validation are inputs to the decision, not substitutes for it.

If the Directorate identifies issues that cannot be mitigated, the technology is removed from engagement and use immediately. This is a real cessation authority, not a comment-and-recommend role.

The memo also issues three immediate prohibitions and two phase-out deadlines that affect every DoW Component’s procurement pipeline today:

- **Quantum confidentiality and keying technologies are out, effective immediately.** No testing, piloting, use, or procurement of QKD; QKD combined with other cryptographic key establishment; quantum communications or networking; non-local quantum randomness generation; or non-FIPS random number generation for confidentiality, authenticity, integrity, key distribution, or randomness generation—absent specific Directorate exception. Chapter 7 explains why this technical position is not new; the November 2025 memo makes it binding for DoW.

- **Commercial PSK-based “quantum resistance” solutions are out, effective immediately.** Pre-shared keys provisioned through NSA KMI for Type 1 devices remain permitted. All other commercial PSK-based quantum-resistance approaches are prohibited from new test, pilot, use, or procurement actions.

- **Commercial symmetric key establishment, key agreement, and key distribution protocols for quantum resistance are out, effective immediately—**same prohibition scope as PSKs.

- **By December 31, 2030,** non-KMI PSK solutions and symmetric key establishment/agreement/distribution protocols must be phased out and replaced with NIST-approved (CNSA 2.0–listed for NSS) asymmetric PQC key establishment.

- **By December 31, 2031,** the same phase-out applies to solutions currently registered with NSA CSfC. Pre-2010 symmetric key distribution use cases are explicitly grandfathered as legacy.

A DoW PQC Strategy is referenced repeatedly throughout the memo and is in preparation. It will be the master execution document. As of this writing, it has not been published; new requirements, approval processes, and updates are being maintained centrally at https://cybersecurityks.osd.mil/DoDcs/pqc. Component-level PQC migration leads were due to the Directorate within twenty days of the memo’s issuance, with annual updates each September 30.<sup>14</sup>

> **⚠  MANDATE ALERT**
> The DoW CIO PQC Directorate’s intake and deployment approvals are an **additional** gate on top of FIPS 140-3, NIAP Common Criteria, and NSA CSfC—not a replacement. A DoW Component cannot lawfully acquire, pilot, deploy, or use any PQC-enabling or PQC-related technology without explicit Directorate approval, even when the underlying product holds every existing federal certification. As of this writing, the operational machinery for this approval (forms, criteria, SLAs, vendor-facing process documentation) is still being stood up; expect this to evolve as the DoW PQC Strategy is published and the Directorate matures.

The practical implication for vendors and integrators: a product that has cleared FIPS 140-3, NIAP CC, and CSfC is no longer sufficient on its own to be acquired or deployed by a DoW Component for PQC purposes. The Directorate’s intake and deployment approvals are now decision points in the procurement path, and the artifacts the Directorate will demand—test plans, test results, acquisition artifacts, risk mitigations—should be assembled in parallel with traditional certification work, not after.<sup>15</sup>

## NIST IR 8547: The Deprecation Timeline

Published in November 2024 as an initial public draft, NIST IR 8547 (“Transition to Post-Quantum Cryptography Standards”) established for the first time a formal deprecation schedule for quantum-vulnerable algorithms.<sup>8</sup>

- **Deprecated after 2030:** All quantum-vulnerable algorithms at the 112-bit security level (RSA-2048, ECC P-256, DH-2048, etc.). “Deprecated” means the algorithm is still permitted but actively discouraged; new systems should not use it.

- **Disallowed after 2035:** All quantum-vulnerable public-key algorithms at any security strength. “Disallowed” means NIST-compliant systems cannot use the algorithm at all. Period.

NIST IR 8547 also supports hybrid cryptographic solutions during the transition—combining classical and PQC algorithms so that the system remains secure as long as at least one algorithm holds. This is particularly relevant for organizations that want to begin migration now without waiting for full PQC ecosystem maturity.

## International: The Global Picture

### United Kingdom — NCSC Three-Phase Roadmap

The UK’s National Cyber Security Centre (part of GCHQ) published its PQC migration timeline in March 2025—the first major regulatory jurisdiction to endorse NIST’s standardized algorithms and set concrete deadlines.<sup>9</sup>

- **By 2028:** Complete discovery—identify all cryptographic services needing upgrades, build a migration plan, create a cryptographic inventory.

- **By 2031:** Execute high-priority upgrades for critical systems and refine migration plans as PQC standards mature.

- **By 2035:** Complete migration across all systems, services, and products.

The NCSC prioritizes critical national infrastructure: NHS healthcare systems, City of London financial services, defense, and government. For most SMEs, the transition will happen through routine vendor updates. Larger organizations must take active ownership.

### European Union — NIS2 PQC Roadmap

The EU’s approach is structured through the NIS Cooperation Group’s coordinated implementation roadmap, published in early 2025.<sup>10</sup>

- **By end of 2026:** Member states initiate national PQC transition strategies.

- **By 2030:** Transition critical infrastructure to PQC.

- **By 2035:** Complete migration for as many systems as practically feasible.

In January 2026, the European Commission published a proposed directive amending NIS2 to include **explicit post-quantum cryptography requirements** written directly into the directive text for the first time. ENISA has published guidance recommending hybrid PQ/T schemes (combining classical algorithms with PQC) to smooth interoperability during transition.

### Financial Sector — G7 Roadmap

The G7 Cyber Expert Group released a financial sector PQC roadmap on January 13, 2026, co-chaired by the US Treasury and Bank of England.<sup>11</sup> It targets critical financial systems for migration by 2030–2032 and full transition by 2035. FINRA, FS-ISAC, and national financial regulators are expected to align sector-specific guidance with this framework.

## Sector-Specific Considerations

The PQC mandates don’t apply uniformly. Your migration urgency depends on your sector:

| **Sector** | **Primary PQC Drivers** | **Key Dates** |
| --- | --- | --- |
| **DoD / Intelligence** | CNSA 2.0, NSM-10, CNSSP 15, DoW CIO PQC Memo (Nov 2025). Mandatory. DoW Components must obtain intake and deployment approval from the DoW CIO PQC Directorate. No waivers without explicit Directorate or NSA approval. | New acquisitions: Jan 2027. Networking: 2030. Full: 2033–2035. |
| **Federal Civilian (FCEB)** | Preparedness Act, NSM-10, M-23-02, EO 14306, NIST IR 8547. Compliance tracked via FISMA. | Transition plans: Apr 2026. Deprecated: 2030. Disallowed: 2035. |
| **Federal Contractors** | CISA PQC product list, DFARS/CMMC for DoD suppliers, agency-specific acquisition rules (e.g., USDA AGAR). | PQC readiness expected: Jan 2027. Procurement pressure accelerating. |
| **Financial Services** | G7 roadmap, FINRA guidance, FS-ISAC publications. HNDL risk acute for transaction data. | G7 targets critical systems: 2030–2032. Full: 2035. |
| **Healthcare** | HIPAA “reasonable safeguards” (evolves with technology). Long data lifetimes (medical records are permanent). | No explicit PQC mandate yet. HNDL risk is extreme due to data lifetime. |
| **Critical Infrastructure** | CISA PQC Initiative, EU NIS2. OT/ICS environments have unique migration challenges. | EU: critical infrastructure by 2030. US: varies by sector. |
| **Private Sector (General)** | No direct federal mandate (unless federal contractor). Market pressure from PQC-ready competitors and customers. | Follow NIST standards. Plan with 2030 deprecation in mind. |

### Sector Acquisition Lifecycles: When PQC Requirements Bite

The mandates described above ride on top of existing acquisition frameworks. Understanding when a regulatory date (“CNSA 2.0 for all new NSS acquisitions by January 1, 2027”) intersects a program’s actual procurement lifecycle matters because the framework, not the calendar, governs when PQC requirements get baked into contracts, solicitations, and systems engineering reviews. Three frameworks dominate federal sector acquisition.<sup>12</sup>

**FAA Acquisition Management System (AMS).** Codified at fast.faa.gov, the AMS governs FAA capital investments through six lifecycle phases (Service Analysis & Strategic Planning, Concept & Requirements Definition, Initial Investment Analysis, Final Investment Analysis, Solution Implementation, In-Service Management) with decision points overseen by the Joint Resources Council. PQC requirements typically enter at Concept & Requirements Definition through the Information Systems Security Engineering (ISSE) process and are finalized in the Final Investment Analysis phase as part of the Solicitation Information Request, Statement of Work, and Contract Data Requirements List.

**DoDI 5000.02 Adaptive Acquisition Framework (AAF).** Reissued January 23, 2020 with Change 1 (June 8, 2022), DoDI 5000.02 replaced the traditional one-size-fits-all model with six tailorable pathways: Urgent Capability Acquisition, Middle Tier of Acquisition (rapid prototyping and rapid fielding), Major Capability Acquisition, Software Acquisition, Defense Business Systems, and Acquisition of Services. PQC entry points vary by pathway. Major Capability Acquisition has the most structured milestone gates (Milestone A/B/C) at which PQC requirements can be specified; Software Acquisition moves fastest through iterative deliveries; Middle Tier rapid fielding programs must complete within five years of program start and typically inherit PQC requirements from the parent system.

**NASA NPR 7120.5F (Space Flight Program and Project Management).** NASA space flight programs follow a two-phase structure—Formulation and Implementation—subdivided into Phase A through Phase F with Key Decision Points (KDPs) as approval gates. PQC requirements for NASA systems enter primarily at Phase A (Concept & Technology Development) for new missions; for existing missions in Phase E (Operations & Sustainment), PQC arrives through capability upgrades or technology refresh cycles. Ground systems supporting space flight operations are explicitly within NPR 7120.5F scope.

The practical implication: a regulatory date is a constraint on when PQC capability must be present in a deployed system, not a directive for how a program acquires it. A DoD Major Capability Acquisition program starting in 2026 may not field initial operational capability until 2030–2033—so PQC must be in the requirements baseline at program start to meet CNSA 2.0’s Jan 2027 “new acquisitions” gate, even though the deployed system won’t exist until years later. Appendix G provides a detailed crosswalk mapping the book’s five-phase PQC migration model against each of these frameworks.

## The Master Timeline: Everything in One View

This is the single consolidated reference. We’ve mapped every major PQC milestone across all mandates and jurisdictions. **Tear this page out.**

| **Date** | **Milestone** | **Source** |
| --- | --- | --- |
| **Aug 2024** | NIST publishes FIPS 203/204/205—first finalized PQC standards | NIST |
| **Nov 2024** | NIST IR 8547 published—formal deprecation timeline announced | NIST |
| **Mar 2025** | NIST selects HQC as fifth PQC algorithm; UK NCSC publishes 3-phase roadmap | NIST, NCSC |
| **Jun 2025** | EO 14306 modifies federal PQC posture (preserves direction, loosens urgency) | White House |
| **Nov 2025** | **DoW CIO PQC Memo: new intake/deployment approval gate; QKD and commercial PSK/symmetric KE prohibited immediately** | DoW CIO |
| **Jan 2026** | CISA publishes PQC product categories list for federal procurement | CISA / EO 14306 |
| **Apr 2026** | **FCEB agencies submit PQC transition plans (crypto inventory + roadmap)** | NSM-10 / M-23-02 |
| **2026–2027** | CNSA 2.0: Networking equipment must support PQC. FN-DSA and HQC standards expected. | NSA, NIST |
| **Jan 2027** | **All new NSS acquisitions must be CNSA 2.0 compliant. Federal contractors demonstrate PQC readiness.** | CNSA 2.0 / EO 14306 |
| **2028** | UK NCSC Phase 1 complete: all orgs have crypto inventory and migration plan | UK NCSC |
| **Jan 2030** | **All federal systems support TLS 1.3+. CNSA 2.0 exclusive for VPNs/routers and software signing. NIST deprecates 112-bit public-key algorithms. DoW phase-out of non-KMI PSK and symmetric KE protocols complete (CSfC-registered: Dec 2031).** | EO 14306, CNSA 2.0, NIST |
| **2030–2032** | EU: critical infrastructure to PQC. G7: critical financial systems migrated. UK Phase 2 complete. | EU NIS2, G7, NCSC |
| **2033** | CNSA 2.0 exclusive for web/cloud, operating systems, niche devices, legacy replacement | NSA CNSA 2.0 |
| **2035** | **NIST disallows all quantum-vulnerable public-key algorithms. NSM-10 full migration target. EU/UK complete.** | NIST, NSM-10, EU, UK |

## What This Means for You

**If you operate NSS or sell to DoD:** CNSA 2.0 is your binding standard. New acquisitions must be compliant by January 2027. You are already behind on software signing.

**If you’re a federal civilian agency:** Your crypto inventory and transition plan should be in progress or submitted. 2030 deprecation means no new systems with RSA/ECC after that date.

**If you’re a federal contractor:** PQC readiness is becoming a procurement requirement. The CISA product categories list is already shaping buying decisions. If your products don’t support PQC, you risk being excluded from future contracts.

**If you’re in the private sector:** No direct federal mandate (unless you’re a contractor), but the NIST deprecation timeline will cascade through every compliance framework that references NIST standards—which is nearly all of them. If your customers are in regulated industries, they will require PQC from their vendors.

**If you operate internationally:** The UK, EU, and G7 timelines are converging on 2035 with intermediate milestones. Multinational organizations must track requirements across multiple jurisdictions.

> **PLAIN-LANGUAGE SIDEBAR**
> The bottom line: regardless of your sector, 2035 is the hard stop. But the real operational deadlines are earlier—January 2027 for DoD, 2028 for UK discovery, 2030 for NIST deprecation and CNSA 2.0 networking. The organizations that start now will migrate calmly. The ones that wait until 2030 will discover what panic looks like at enterprise scale.

## What’s Next

You now know why you need to migrate, what is broken, what replaces it, and who says you have to. The next question is intensely practical: how do you find all the cryptography in your environment? Chapter 5 walks through the cryptographic discovery process—building the inventory that every migration plan depends on.

## Notes

The following sources support specific claims made in Chapter 4. Full bibliographic entries appear in the Bibliography.

**1.**  For analysis of the US PQC regulatory framework hierarchy, see: “The Complete US Post-Quantum Cryptography (PQC) Regulatory Framework in 2026,” postquantum.com (February 2026). This source provides detailed analysis of which mandates survive administration changes.

**2.**  Quantum Computing Cybersecurity Preparedness Act, Pub. L. No. 117-349, signed December 21, 2022. As federal statute, its requirements cannot be rescinded by executive order.

**3.**  Whether OMB issued the migration guidance required by the Preparedness Act by the August 2025 statutory deadline is unclear. An OMB draft memorandum circulated in July 2025 would direct agencies to fully migrate to PQC standards and require third-party vendors to disclose phased PQC transition timelines, but it has not been finalized as of March 2026.

**4.**  The White House. National Security Memorandum on Promoting United States Leadership in Quantum Computing While Mitigating Risks to Vulnerable Cryptographic Systems (NSM-10), May 4, 2022.

**5.**  Executive Order 14306, “Sustaining Select Efforts to Strengthen the Nation’s Cybersecurity and Amending Executive Order 13694 and Executive Order 14144,” signed June 6, 2025. Analysis based on comparison of EO 14144 (Biden, January 2025) with EO 14306 (Trump, June 2025).

**6.**  NSA. “Commercial National Security Algorithm Suite 2.0 (CNSA 2.0) Algorithms.” PP-22-1338, Ver. 1.0, September 2022. FAQ updated to Ver. 2.1, December 2024. Timeline by system category from the CNSA 2.0 Algorithm Guidance document.

**7.**  CNSA 2.0 approved algorithms: ML-KEM-1024 (key establishment), ML-DSA-87 (general signatures), LMS/XMSS per SP 800-208 (software/firmware signing), AES-256 (symmetric), SHA-384/512 (hashing). Note: SLH-DSA is NOT part of CNSA 2.0 and is not approved for NSS.

**8.**  NIST IR 8547 (Initial Public Draft), “Transition to Post-Quantum Cryptography Standards.” November 12, 2024. Tables 2 and 4 list quantum-vulnerable algorithms with deprecation after 2030 and disallowance after 2035.

**9.**  UK National Cyber Security Centre. “Timelines for Migration to Post-Quantum Cryptography.” Published March 2025. Three-phase roadmap: Phase 1 (to 2028), Phase 2 (2028–2031), Phase 3 (2031–2035).

**10.**  NIS Cooperation Group. “Coordinated Implementation Roadmap for the Transition to Post-Quantum Cryptography.” Published early 2025. European Commission proposed directive amending NIS2 with explicit PQC requirements published January 2026.

**11.**  G7 Cyber Expert Group. Financial Sector PQC Roadmap. Published January 13, 2026. Co-chaired by US Treasury and Bank of England. Targets critical financial systems for migration by 2030–2032.

**12.**  Sector acquisition framework references: FAA AMS authoritative policy at the FAA Acquisition System Toolset (fast.faa.gov); DoDI 5000.02, “Operation of the Adaptive Acquisition Framework,” January 23, 2020, Change 1 (June 8, 2022); NASA NPR 7120.5F, “NASA Space Flight Program and Project Management Requirements” (current revision). See Appendix G for the full crosswalk mapping these frameworks to the book’s five-phase PQC migration model.

**13.**  DoW CIO. Memorandum, “Preparing for Migration to Post Quantum Cryptography,” November 18, 2025. Signed by Katherine Arrington, Performing the Duties of the Chief Information Officer of the Department of War. https://dodcio.defense.gov/Portals/0/Documents/Library/PreparingForMigrationPQC.pdf

**14.**  Per the November 18, 2025 memo, Component PQC migration leads must be reported to the Directorate within twenty days of the memo’s issuance and updated annually by September 30. Centralized requirements and approval-process documentation are maintained at https://cybersecurityks.osd.mil/DoDcs/pqc. Point of contact: osd.pentagon.dodcio.mesg.dcio-cs-pqc@mail.mil.

**15.**  The DoW CIO memo’s authorization regime is “in addition to”—not a substitute for—Committee on National Security Systems Policy 15, “Use of Public Standards for Secure Information Sharing,” December 2024, and Chairman of the Joint Chiefs of Staff Instruction 6510.02, “Cryptographic Modernization Planning,” August 16, 2022.

Next: Chapter 5 — Know What You Have: Cryptographic Discovery
