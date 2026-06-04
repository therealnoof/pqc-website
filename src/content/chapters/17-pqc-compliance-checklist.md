---
title: "PQC Compliance Checklist"
displayTitle: "PQC Compliance Checklist"
section: "Appendices & Reference"
chapter: null
order: 17
words: 621
readingMinutes: 3
excerpt: "A consolidated timeline and action checklist for PQC-related mandates. Check off items as your organization completes them."
---

A consolidated timeline and action checklist for PQC-related mandates. Check off items as your organization completes them.

## Immediate Actions (Now)

| **☐** | **Action** | **Reference** |
| --- | --- | --- |
| **☐** | **Cryptographic asset discovery** | Inventory all algorithms, keys, certs, and protocols. Produce CBOM. (Ch5, NIST SP 1800-38B) |
| **☐** | **Quantum risk assessment** | Score all systems using Appendix D methodology. Identify P0 systems. |
| **☐** | **Establish CCOE** | Cross-functional team per Ch6 model. Assign executive sponsor. |
| **☐** | **Update cryptographic policies** | Incorporate PQC requirements into procurement, development, and security policies. |
| **☐** | **Enable hybrid TLS key exchange** | X25519MLKEM768 on internet-facing load balancers/CDN. (Ch7 bridge architecture) |
| **☐** | **Verify SSH key exchange** | Confirm OpenSSH 10.0+ default (mlkem768x25519). Update if needed. |
| **☐** | **Begin dual-signing firmware** | Sign new firmware/SBOMs with both classical + ML-DSA. (CNSA 2.0 “prefer by 2025”) |

## 2026–2027 Actions

| **☐** | **Action** | **Reference** |
| --- | --- | --- |
| **☐** | **Assess HSM PQC readiness** | Five questions from Ch6. Plan firmware upgrades or replacements. |
| **☐** | **Pilot PQC certificates** | Test ML-DSA certificates in non-production. Measure handshake performance. (Ch8) |
| **☐** | **Engage vendors on PQC roadmaps** | Collect PQC timelines from all critical vendors. (Appendix F template) |
| **☐** | **Evaluate Merkle Tree Certificates** | Track Chrome/Cloudflare MTC pilot (Phase 1–2). Plan for CQRS if web-facing. |
| **☐** | **Increase TCP initcwnd to 20** | On internet-facing VIPs/load balancers to accommodate PQC cert chains. (Ch8) |
| **☐** | **Deploy IPsec PPKs** | RFC 8784 post-quantum pre-shared keys on priority VPN tunnels. (Ch7) |
| **☐** | **Automate certificate lifecycle** | ACME or vendor CLM for 200-day cert validity (CA/B Forum, March 2026). |

## 2028–2030 Actions

| **☐** | **Action** | **Reference** |
| --- | --- | --- |
| **☐** | **Complete PKI hierarchy migration** | New root/intermediate CAs with ML-DSA. Begin issuing PQC leaf certificates. |
| **☐** | **Migrate IPsec to native ML-KEM** | Replace PPK stopgap with CNSA 2.0 IPsec profile (ML-KEM-1024). |
| **☐** | **Re-sign legacy evidence** | Re-sign critical audit logs, contracts, and firmware archives with PQC. (Ch9 Pattern 2/3) |
| **☐** | **Automate 47-day cert renewal** | Prepare for CA/B Forum 47-day maximum validity by March 2029. |
| **☐** | **Transition high-confidence systems to pure PQC** | Drop classical-only where ML-KEM/ML-DSA have 6+ years post-standardization scrutiny. |

## 2030–2035 Actions

| **☐** | **Action** | **Reference** |
| --- | --- | --- |
| **☐** | **NIST deprecation deadline (2030)** | All 112-bit classical algorithms deprecated. No new deployments. (NIST IR 8547) |
| **☐** | **CNSA 2.0 full compliance (2030)** | NSS: exclusive use of ML-KEM-1024 / ML-DSA-87 for networking. |
| **☐** | **Complete hybrid → pure PQC transition** | Remove classical component from hybrid deployments where no longer needed. |
| **☐** | **NIST disallow deadline (2035)** | All quantum-vulnerable public-key algorithms disallowed. NSM-10 full compliance. |
| **☐** | **Validate crypto-agility** | Confirm ability to swap algorithms within 30 days across the environment. (Appendix E Dim 7) |

## Federal Sector Additions

Federal agencies and federal service integrators should apply the following items in addition to the timeline-based actions above. These align PQC migration activities with the existing Risk Management Framework (NIST SP 800-37 Rev 2) rather than creating a parallel compliance track.

| **☐** | **Action** | **Reference** |
| --- | --- | --- |
| **☐** | **Include PQC in System Security Plans (SSPs)** | Document PQC control selection, implementation timeline, and residual risk per NIST SP 800-37 Rev 2. |
| **☐** | **Track PQC migration in POA&Ms** | Record quantum-vulnerable systems and their migration milestones in the Plan of Action and Milestones for continuous monitoring. |
| **☐** | **Submit annual quantum-vulnerable IT system inventory** | Required by NSM-10 for federal agencies. (Ch 5 Note 1) |
| **☐** | **M-23-02 cryptographic inventory reporting** | FCEB agencies submit annual cryptographic inventory to CISA per OMB Memorandum M-23-02. (Ch 5 Note 1) |
| **☐** | **FedRAMP continuous monitoring for cloud offerings** | Include PQC posture and migration progress in FedRAMP ConMon deliverables. |
| **☐** | **Reauthorize systems after PQC migration** | Treat hybrid/PQC deployment as a significant change triggering ATO reauthorization per NIST SP 800-37 Rev 2 Monitor step. |
| **☐** | **Embed PQC in procurement language** | Apply PQC readiness requirements to acquisition clauses. USDA/AGAR provides a model. (Ch 9 Note 9) |

### Appendix F
