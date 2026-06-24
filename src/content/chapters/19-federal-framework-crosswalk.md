---
title: "Federal Framework Crosswalk"
displayTitle: "Federal Framework Crosswalk"
section: "Appendices & Reference"
chapter: null
order: 19
words: 1724
readingMinutes: 8
excerpt: "Federal agencies operate under multiple overlapping cybersecurity and acquisition frameworks. This appendix maps the book’s five-phase PQC migration model (Chapter 6) against the four frameworks most commonly encountered"
---

Federal agencies operate under multiple overlapping cybersecurity and acquisition frameworks. This appendix maps the book’s five-phase PQC migration model (Chapter 6) against the four frameworks most commonly encountered by federal and DoD readers: the NIST Risk Management Framework, the FAA Acquisition Management System, FedRAMP, and the DoD Risk Management Framework. A fifth crosswalk maps the model onto the Department of War PQC Strategy’s five Lines of Effort. The intent is not to replace these frameworks’ own guidance but to show PQC program managers where their migration work maps onto existing compliance artifacts: SSPs, POA&Ms, ConMon submissions, Investment Analysis reports, and ATO packages.

Use this crosswalk when building a PQC program charter, responding to RFIs or audit inquiries, or aligning budget requests with existing framework deliverables. Every row points to work your organization likely already performs; what changes is the cryptographic content of that work.

## NIST Risk Management Framework (SP 800-37 Rev 2)

The NIST RMF is a seven-step process (Prepare, Categorize, Select, Implement, Assess, Authorize, Monitor) applied at organizational, mission/business, and system tiers. The framework is mandatory for federal civilian agencies under FISMA and is adopted by reference in DoD and Intelligence Community RMF implementations. PQC migration maps directly onto existing RMF artifacts without introducing a parallel compliance track.

| **Book Phase** | **Framework Activity** | **PQC Migration Activity** |
| --- | --- | --- |
| **Phase 0: Organize** | **Prepare (org + system level)** | Establish CCOE. Identify mission-critical systems requiring PQC migration. Update risk management strategy to include quantum threat. Align PQC scope with existing authorization boundaries. |
| **Phase 0: Organize** | **Categorize** | Review existing FIPS 199 / CNSSI 1253 categorizations. Systems handling long-lifetime sensitive data warrant higher categorization for HNDL risk. |
| **Phase 1: Edge First** | **Select & Implement** | Tailor existing control baselines (NIST SP 800-53 SC-8, SC-12, SC-13, SC-17) to include PQC. Implement hybrid TLS on internet-facing TLS terminators. Update SSPs to reflect PQC additions. |
| **Phase 2: Trust Infrastructure** | **Select & Implement** | Extend control implementation to PKI (code signing, firmware signing), HSMs, VPN/IPsec. Document PQC implementation in SSP. |
| **Phase 3: Broaden** | **Assess** | Assess PQC control effectiveness. Update SAR with PQC assessment results. Track deviations and risks in POA&M. |
| **Phase 3: Broaden** | **Authorize** | Determine whether PQC-capable deployment constitutes a significant change triggering ATO reauthorization. Update ATO package. |
| **Phase 4: Complete and Sustain** | **Monitor** | Incorporate PQC posture into continuous monitoring. Track vendor PQC readiness, algorithm deprecation milestones (NIST IR 8547), and emerging side-channel findings in POA&M. |

## FAA Acquisition Management System (AMS)

The FAA AMS is the lifecycle acquisition framework governing FAA capital investments, including National Airspace System (NAS) infrastructure. Authoritative guidance resides at fast.faa.gov (FAA Acquisition System Toolset). The AMS comprises six lifecycle phases with distinct decision points overseen by the Joint Resources Council (JRC). Security work integrates via the Information Systems Security Engineering (ISSE) process, which applies NIST SP 800-53 controls to AMS deliverables such as the Preliminary and Final Requirements documents.

| **Book Phase** | **Framework Activity** | **PQC Migration Activity** |
| --- | --- | --- |
| **Phase 0: Organize** | **Service Analysis & Strategic Planning** | Identify services with long-lifetime data or safety-critical cryptographic dependencies. Include PQC readiness in strategic planning. |
| **Phase 0: Organize** | **Concept & Requirements Definition** | Develop PQC-aware Concept of Operations. Document cryptographic requirements that support hybrid TLS, ML-DSA signing, and ML-KEM key exchange in preliminary requirements documents (pPR). |
| **Phase 1: Edge First / Phase 2** | **Initial Investment Analysis** | Include PQC capability in alternatives analysis. Develop Basis of Estimates (BOE) for PQC-capable components. Tailor NIST SP 800-53 controls to the acquisition. |
| **Phase 1: Edge First / Phase 2** | **Final Investment Analysis** | Finalize security test plans including PQC verification. Update SIR, SOW, and CDRL with PQC requirements. Obtain stakeholder sign-off on PQC scope. |
| **Phase 2: Trust Infrastructure** | **Solution Implementation** | Execute DT/OT/IOA for PQC-enabled systems. Verify hybrid TLS operation in the NAS environment. Address any PQC-induced performance regressions before In-Service Decision. |
| **Phase 3 / Phase 4** | **In-Service Management** | Include PQC posture in ongoing SCAP reporting. Plan technology refresh cycles around PQC milestones (2030 NIST deprecation, CNSA 2.0 exclusive use deadlines). Re-certify when significant PQC changes occur. |

## FedRAMP (Federal Risk and Authorization Management Program)

FedRAMP provides government-wide security assessment and authorization for cloud service offerings (CSOs) used by federal agencies. Cloud service providers (CSPs) achieve authorization via agency sponsorship or program authorization pathways. Current authorizations use the Rev 5 baselines; the FedRAMP 20x modernization initiative (announced March 2025) introduces automation-driven continuous reporting and Key Security Indicators. Core deliverables remain the System Security Plan, Plan of Action and Milestones, and monthly continuous monitoring submissions.

| **Book Phase** | **Framework Activity** | **PQC Migration Activity** |
| --- | --- | --- |
| **Phase 0: Organize** | **Authorization Boundary Definition** | Identify cloud service offerings within FedRAMP boundary that rely on quantum-vulnerable cryptography. Document cryptographic modules in SSP per FRR203. |
| **Phase 1: Edge First** | **Control Implementation (Rev 5)** | Deploy hybrid TLS on CSO-facing endpoints. Implement PQC-capable cryptographic modules aligned with FedRAMP Cryptographic Modules Guidance. Update SSP and boundary documentation. |
| **Phase 2: Trust Infrastructure** | **Annual Assessment / 3PAO** | Include PQC controls in annual assessment scope. Capture PQC evidence in Integrated Inventory Workbook (IIW). Update continuous monitoring submissions. |
| **Phase 3: Broaden** | **Significant Change Request** | Major PQC deployments (new cryptographic modules, PKI migration, cipher suite changes) trigger SCR workflow. Document per FedRAMP ConMon Playbook significant-change process. |
| **Phase 4: Complete and Sustain** | **Continuous Monitoring (ConMon)** | Monthly ConMon submissions reflect PQC posture. POA&M tracks remaining quantum-vulnerable systems with target remediation dates. Prepare for FedRAMP 20x automation-driven evidence model. |

## DoD Risk Management Framework (DoDI 8510.01)

DoDI 8510.01, reissued July 19, 2022 as “Risk Management Framework for DoD Systems,” adopts the NIST SP 800-37 Rev 2 RMF process while layering DoD-specific governance. Categorization uses CNSSI 1253 rather than FIPS 199 for National Security Systems. The framework emphasizes cybersecurity reciprocity: the reuse of authorization evidence across Components to reduce redundant testing. PQC migration for DoD/DoW Components aligns with CNSA 2.0 and the DoW PQC Strategy: systems support PQC by 2030 and use PQC by 2031, with CNSA 2.0 category deadlines running to 2033 where noted.

| **Book Phase** | **Framework Activity** | **PQC Migration Activity** |
| --- | --- | --- |
| **Phase 0: Organize** | **Prepare / Tier 1–2** | OSD-level PQC policy aligns with CNSA 2.0 timeline. DoD Component CIOs integrate PQC into cybersecurity strategy. RMF TAG guidance referenced for PQC implementation. |
| **Phase 0: Organize** | **Categorize (CNSSI 1253)** | Review NSS categorizations. Systems processing Top Secret, Secret, or long-lifetime classified data prioritized for PQC migration. Align with CNSA 2.0 exclusivity requirements. |
| **Phase 1 / Phase 2** | **Select & Implement** | Select PQC controls per NIST SP 800-53 with CNSSI 1253 overlays. Deploy CNSA 2.0-compliant implementations: ML-KEM-1024 and ML-DSA-87 for NSS networking. Document in SSP. |
| **Phase 2: Trust Infrastructure** | **Assess** | Assess PQC control implementation. Leverage DoD Cybersecurity Reciprocity where possible to reduce redundant testing. Document findings for the Receiving AO. |
| **Phase 3: Broaden** | **Authorize** | AO makes risk-based authorization decision for PQC-enabled system. Reciprocity framework enables cross-Component reuse of PQC authorization evidence. |
| **Phase 4: Complete and Sustain** | **Monitor** | Continuous monitoring per DoDI 8530.01. Track CNSA 2.0 milestones (NSS exclusive PQC use by 2030–2035). Update ISRMC (DoD Risk Executive Function) on enterprise PQC posture. |

## Department of War PQC Strategy (DoDI/LOE Structure)

The DoW PQC Strategy is not a Risk Management Framework, but it carries its own structure of five Lines of Effort (LOEs) against which DoW program managers report progress. Unlike the RMF’s sequential steps, the strategy is explicit that the LOEs run concurrently; their order does not imply sequence. The crosswalk below maps the book’s five-phase model onto the LOEs so a DoW Component can show how its migration work satisfies the strategy. Two acquisition tracks (High Assurance ECU, which is NSA-certified and KMI-dependent, and Commercial Solutions, which uses NIST algorithms via CSfC and commodity IT) cut across all five LOEs.

| **Book Phase** | **DoW Line of Effort** | **PQC Migration Activity** |
| --- | --- | --- |
| **Phase 0: Organize** | **LOE 1: Optimize Governance** | Stand up the CCOE and align it to the DoW CIO PQC Directorate’s intake and deployment gates. Update acquisition authorities and prepare the workforce. |
| **Phase 0: Organize** | **LOE 2: Baseline Inventory and Plan** | Identify all NSS and non-NSS cryptography (including DIB systems that hold DoW data), conduct quantum-threat impact assessments, and build component-level migration roadmaps and response plans. |
| **Phase 1: Edge First** | **LOE 3: Develop and Analyze** | Vet commercial and DoW-developed PQC solutions against warfighting use cases (latency, jamming resilience, key-compromise resilience) and promote cryptographic agility. Engage NIST, NSA, NATO, and IETF on protocols. |
| **Phase 1: Edge First / Phase 2** | **LOE 4: Integrate Commercial Solutions** | Field PQC commodity IT through CSfC and NIAP profiles. Modernize the DoW PKI, adopt PQC software and firmware signing, and upgrade operating systems, browsers, and networking equipment. |
| **Phase 2: Trust Infrastructure / Phase 3** | **LOE 5: Deploy Quantum Resistant Devices** | Modernize the NSA KMI and field High Assurance ECUs across data links, transport, space systems, telephony, tactical radios, and edge devices. |
| **Phase 4: Complete and Sustain** | **LOE 5 + LOE 1** | Deprecate and remove legacy devices that cannot support PQC. Sustain governance, track LOE progress against the 2030 support and 2031 use deadlines, and maintain cryptographic agility for the next transition. |

## Cross-Framework Observations

Three patterns recur across all four frameworks. First, the SSP (or its framework equivalent) is always the anchor document: PQC controls must be documented there regardless of which framework governs the system. Second, the POA&M is always the tracking mechanism for incomplete PQC migration; remaining quantum-vulnerable systems should be recorded there with target remediation milestones. Third, authorization decisions (ATO, In-Service Decision, FedRAMP Authorization) are significant-change events when PQC deployment substantially alters the system’s cryptographic posture. Program managers should plan for these decision gates in the timeline.

The book’s five-phase migration model (Chapter 6) deliberately does not mirror any one framework’s step structure. This separation is intentional: PQC migration spans multiple systems, each of which may be at a different point in its own RMF/AMS/FedRAMP/DoD RMF cycle. The book’s phases describe the cryptographic work; the framework steps describe how that work is authorized and sustained within federal compliance structures. Use both views together.
