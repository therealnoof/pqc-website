---
title: "Quantum Risk Scoring Methodology"
displayTitle: "Quantum Risk Scoring Methodology"
section: "Appendices & Reference"
chapter: null
order: 13
words: 1122
readingMinutes: 5
excerpt: "This appendix provides a reusable, quantitative risk scoring methodology for assessing the quantum threat to specific systems and applications. It is adapted from the TNO/AIVD quantum risk methodology and designed to plu"
---

This appendix provides a reusable, quantitative risk scoring methodology for assessing the quantum threat to specific systems and applications. It is adapted from the TNO/AIVD quantum risk methodology and designed to plug into your organization’s existing risk management framework (NIST RMF, ISO 27005, or agency-specific processes).

The quantum risk score combines three factors: **algorithm weakness** (how vulnerable is the cryptography?), **impact severity** (what happens if it’s broken?), and **migration difficulty** (how hard is it to fix?). Each is scored independently, then combined into an overall 0–4 risk score.

## Factor 1: Algorithm Weakness Score (0–3)

| **Score** | **Classification** | **Examples** |
| --- | --- | --- |
| **0** | Quantum-safe. No migration needed. | AES-256, SHA-384, SHA-512, ML-KEM, ML-DSA, SLH-DSA |
| **1** | Theoretically weakened by quantum, but not practically broken. Future attention needed. | AES-128 (Grover’s halves effective strength), SHA-256 (collision resistance reduced but still adequate), 3DES |
| **2** | Broken by quantum computer running Shor’s algorithm. Migration required within NIST timeline. | RSA-2048+, ECDSA P-256/P-384, ECDH, DH, DSA — all quantum-vulnerable asymmetric algorithms |
| **3** | Broken by quantum AND already weakened classically. Immediate migration regardless of quantum timeline. | RSA-1024, SHA-1 signatures, DES, RC4, MD5 — deprecated algorithms still found in legacy systems |

## Factor 2: Impact Severity Score (0–4)

Assess the impact if the cryptographic protection on this system were completely compromised. Consider both the security function (confidentiality, integrity, authentication) and the data sensitivity.

| **Score** | **Impact Level** | **Description** |
| --- | --- | --- |
| **0** | Negligible | Public data. No confidentiality, integrity, or authentication requirement. |
| **1** | Low | Internal data with limited sensitivity. Breach causes minor operational disruption. Short data lifespan (<2 years). |
| **2** | Moderate | Business-sensitive data. Breach causes financial loss, reputational damage, or regulatory penalty. Data lifespan 2–10 years. |
| **3** | High | Classified data, PII at scale, critical infrastructure control systems, or high-value IP. Data lifespan 10–25 years. HNDL risk is significant. |
| **4** | Critical | National security data, weapons systems, intelligence sources and methods, long-lived infrastructure (satellites, OT/ICS). Data lifespan 25+ years. HNDL risk is severe and immediate. |

## Factor 3: Migration Difficulty Score (0–4)

Estimate the time, effort, and complexity required to migrate this system to PQC. Higher scores indicate harder migrations that need earlier starts.

| **Score** | **Difficulty** | **Description** |
| --- | --- | --- |
| **0** | Trivial | Already quantum-safe or requires only a configuration change (e.g., enabling hybrid TLS on a modern load balancer). |
| **1** | Low | Software update or library upgrade. Vendor provides PQC-ready release. Standard testing and rollout cycle. |
| **2** | Moderate | Requires coordinated changes across multiple systems (e.g., PKI hierarchy + application servers + clients). Interoperability testing needed. |
| **3** | High | Custom protocols, embedded/OT systems, vendor dependencies with no PQC roadmap, or HSM replacements required. Multi-year effort. |
| **4** | Extreme | Cannot be migrated in place. Requires full system replacement, contract renegotiation, or physical hardware swap (satellites, deployed military systems, legacy SCADA). |

## Computing the Overall Quantum Risk Score (0–4)

The overall quantum risk score is derived by combining the three factors. This is not a simple average—algorithm weakness gates the assessment, while impact and difficulty determine urgency:

**Step 1:** If Algorithm Weakness = 0, the system is quantum-safe. Overall Risk = 0 regardless of other factors. No further assessment needed.

**Step 2:** If Algorithm Weakness = 3, the system has classical vulnerabilities. Overall Risk = 4 (Critical). Migrate immediately regardless of quantum timeline.

**Step 3:** For Algorithm Weakness = 1 or 2, compute:

**Overall Risk = min(4, round((Impact + Difficulty) / 2))**

Systems with Algorithm Weakness = 1 (symmetric only) generally score lower because the threat is theoretical. Multiply the computed score by 0.5 and round up for these systems.

### Risk Score Action Guide

| **Score** | **Priority** | **Recommended Action** |
| --- | --- | --- |
| **0** | None | System is quantum-safe. Document in CBOM and monitor for future changes. |
| **1** | Low (P4) | Monitor. Include in long-term migration plan. No immediate action required. |
| **2** | Medium (P2–P3) | Plan migration within 2–4 years. Include in Phase 2–3 of roadmap (Chapter 6). Begin vendor engagement. |
| **3** | High (P1) | Migrate within 1–2 years. Prioritize in Phase 1. Enable hybrid mode immediately where possible. |
| **4** | Critical (P0) | Migrate immediately. Escalate to CCOE and executive leadership. This system is actively at risk from classical and/or quantum threats. |

### Worked Examples

The following three scenarios illustrate the scoring methodology in practice. Your CBOM will produce dozens to hundreds of such assessments; these examples establish the reasoning pattern.

**Example 1: Internet-facing web application, RSA-2048 TLS, protecting PII**

A public-facing HR portal terminates TLS with an RSA-2048 certificate and ECDHE key exchange. The portal handles employee records subject to GDPR and state privacy laws, with a 7-year retention requirement.

**Algorithm Weakness = 2.** Asymmetric cryptography (RSA signatures, ECDHE key exchange) is Shor’s-vulnerable.

**Impact Severity = 4.** PII exposure triggers regulatory notification, customer trust damage, and multi-year legal exposure. Internet-facing means HNDL interception is assumed.

**Migration Difficulty = 2.** Standard TLS 1.3 migration path: enable hybrid X25519MLKEM768 at the terminator. Application stack unchanged.

Overall Risk = min(4, round((4 + 2) / 2)) = **3**, but HNDL exposure on PII with 7+ year sensitivity lifetime pulls this to P0 per Chapter 6’s priority matrix. Enable hybrid TLS immediately.

**Example 2: Internal east-west TLS 1.2 between microservices, low-sensitivity operational data**

A service mesh uses TLS 1.2 with ECDHE between internal microservices handling non-sensitive operational telemetry. Traffic is isolated to the internal VPC; no customer data transits this leg.

**Algorithm Weakness = 2.** Same asymmetric exposure as Example 1.

**Impact Severity = 2.** Non-sensitive data, short retention, limited interception surface.

**Migration Difficulty = 3.** Service mesh coordination across dozens of microservices and sidecar proxies; coordination cost dominates the effort.

Overall Risk = min(4, round((2 + 3) / 2)) = **3**. Place in P2–P3 per priority matrix. Schedule within Phase 3 of the migration roadmap; coordinate upgrades with normal service mesh refresh cycles.

**Example 3: Legacy code-signing, SHA-1 with RSA-2048, embedded firmware**

An industrial control system vendor signs firmware updates with a SHA-1 + RSA-2048 signing chain. The certificates were issued in 2018 and the signing infrastructure predates the organization’s migration to SHA-2.

**Algorithm Weakness = 3.** SHA-1 is classically broken (collision attacks demonstrated). This gates the overall score regardless of the other factors.

Impact Severity and Migration Difficulty are not computed; Step 2 of the scoring methodology sets Overall Risk = **4 (Critical)**. Migrate immediately. This scenario illustrates the scoring framework’s gating rule: systems with classical vulnerabilities jump to Critical independent of quantum timeline considerations. PQC planning does not displace classical hygiene.

Record the scores for each system in your CBOM (Chapter 5) alongside the cryptographic inventory. The risk scores feed directly into the priority matrix in Chapter 6 and help justify budget allocation to leadership.

### Appendix E
