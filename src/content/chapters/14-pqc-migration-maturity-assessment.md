---
title: "PQC Migration Maturity Assessment"
displayTitle: "PQC Migration Maturity Assessment"
section: "Appendices & Reference"
chapter: null
order: 14
words: 752
readingMinutes: 3
excerpt: "This self-assessment tool helps organizations evaluate their current readiness for the PQC migration across eight key dimensions. It is adapted from the TNO/AIVD PQC growth model and designed for use by your CCOE (Chapte"
---

This self-assessment tool helps organizations evaluate their current readiness for the PQC migration across eight key dimensions. It is adapted from the TNO/AIVD PQC growth model and designed for use by your CCOE (Chapter 6) as a quarterly or semi-annual checkpoint.

For each dimension, identify the stage (1–5) that best describes your organization’s current state. The assessment highlights which areas need attention and provides a structured framework for tracking progress over time.

### How to Use This Scorecard

- **Assess each dimension independently.** Your organization may be at Stage 4 in Awareness but Stage 1 in PQC Availability, and that’s normal.

- **Focus on the lowest-scoring dimensions first.** These are your bottlenecks. Improvements in one area often unblock progress in others.

- **Reassess quarterly.** The PQC landscape is evolving rapidly. What was “not available” six months ago may now be generally available.

## Dimension 1: Awareness & Leadership

| **Stage** | **Description** |
| --- | --- |
| **1** | No awareness of quantum threat within leadership or technical teams. |
| **2** | Individual contributors aware; no executive sponsorship or budget allocation. |
| **3** | CISO/CTO briefed. Quantum threat included in risk register. Initial budget discussion underway. |
| **4** | Executive sponsor assigned. Dedicated budget approved. PQC migration in organizational roadmap. |
| **5** | Board-level reporting. PQC integrated into enterprise risk management. Regular progress reviews. |

## Dimension 2: Governance & Organization

| **Stage** | **Description** |
| --- | --- |
| **1** | No dedicated team or ownership for cryptographic migration. |
| **2** | Ad hoc responsibility assigned to existing security team as side duty. |
| **3** | CCOE established (Chapter 6) with defined roles. Migration plan drafted. |
| **4** | CCOE operating with cross-functional representation. Phased roadmap approved and in execution. |
| **5** | CCOE integrated into permanent security operations. Crypto-agility policies enforced across the org. |

## Dimension 3: Cryptographic Discovery & Inventory

| **Stage** | **Description** |
| --- | --- |
| **1** | No inventory of cryptographic assets. Unknown what algorithms are in use. |
| **2** | Partial manual inventory of high-priority systems. No CBOM format established. |
| **3** | Automated discovery running on priority systems. CBOM format defined. Quantum risk scores assigned. |
| **4** | Comprehensive CBOM covering all systems. Continuously updated. Integrated with risk management. |
| **5** | Real-time cryptographic observability. CBOM auto-updated from network telemetry. Drift detection alerts. |

## Dimensions 4–8: Quick-Reference Stages

For the remaining five dimensions, assess your organization against the same 1–5 scale:

| **Dimension** | **Stage 1–2** | **Stage 3** | **Stage 4** | **Stage 5** |
| --- | --- | --- | --- | --- |
| **4. Policies & Compliance** | No PQC policy. Crypto policies outdated. | PQC policy drafted. Regulatory gaps identified. | PQC procurement requirements in contracts. | Full compliance with NIST/CNSA 2.0 timelines. |
| **5. PQC Availability** | No PQC-capable products in environment. | Vendor PQC roadmaps collected. Lab testing begun. | PQC-capable products deployed in pilot/hybrid. | PQC standard across production. Pure PQC for new systems. |
| **6. Hybrid Deployment** | No hybrid crypto deployed. | Hybrid TLS enabled on edge/pilot systems. | Hybrid across all internet-facing and priority internal systems. | Transitioning from hybrid to pure PQC per NIST timeline. |
| **7. Crypto-Agility** | Hard-coded algorithms. No abstraction layer. | Crypto-agility policy defined. New systems designed for agility. | Algorithm changes via config, not code. CBOM feedback loop active. | Proven agility: algorithm swap completed in <30 days across environment. |
| **8. Knowledge & Skills** | No PQC training. Reliance on external consultants. | Core team trained. Tabletop exercises conducted. | Role-specific training (Ch9 matrix) complete. Internal PQC expertise. | Organization self-sufficient. Contributing to community/standards. |

## Interpreting Your Score

Sum your scores across all 8 dimensions (max 40). This gives an overall maturity snapshot:

- **8–15 (Early Stage):** You’re at the beginning. Focus on awareness, establishing the CCOE, and starting cryptographic discovery. Chapters 1–5 are your priority reading.

- **16–24 (In Progress):** You have a foundation. Focus on completing discovery, deploying hybrid mode, and engaging vendors. Chapters 6–7 are your next steps.

- **25–32 (Advanced):** You’re executing. Focus on protocol deep dives (Chapter 8), Day-2 operations (Chapter 9), and closing gaps in the lowest-scoring dimensions.

- **33–40 (Mature):** You’re a leader. Focus on transitioning from hybrid to pure PQC, contributing to standards, and mentoring your supply chain partners.

Track scores over time. The goal is steady progress across all dimensions, not perfection in any single one. A balanced approach reduces the risk of being caught with a critical gap when a quantum milestone arrives.

> **PLAIN-LANGUAGE SIDEBAR**
> This scorecard is a conversation starter, not a compliance checklist. Print it, bring it to your next security review, and have each stakeholder independently score the eight dimensions. Where scores differ by 2 or more stages, you’ve found a gap in shared understanding, and that’s the most valuable outcome of the exercise.

### Appendix A
