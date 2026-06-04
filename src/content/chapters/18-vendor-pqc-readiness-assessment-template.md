---
title: "Vendor PQC Readiness Assessment Template"
displayTitle: "Vendor PQC Readiness Assessment Template"
section: "Appendices & Reference"
chapter: null
order: 18
words: 241
readingMinutes: 1
excerpt: "Use this template when evaluating vendors, suppliers, and third-party service providers. Distribute to procurement, security architecture, and CCOE team members."
---

Use this template when evaluating vendors, suppliers, and third-party service providers. Distribute to procurement, security architecture, and CCOE team members.

## Vendor Information

| **Vendor Name:** |  |
| --- | --- |
| **Product / Service:** |  |
| **Assessment Date:** |  |
| **Assessed By:** |  |
| **Contract Renewal Date:** |  |

## Algorithm & Protocol Support

| **Capability** | **Supported** | **Planned** | **No Plans** |
| --- | --- | --- | --- |
| ML-KEM-768 / ML-KEM-1024 key exchange | ☐ | ☐ | ☐ |
| ML-DSA-65 / ML-DSA-87 digital signatures | ☐ | ☐ | ☐ |
| SLH-DSA (hash-based backup signatures) | ☐ | ☐ | ☐ |
| X25519MLKEM768 hybrid TLS 1.3 | ☐ | ☐ | ☐ |
| TLS 1.3 certificate compression (RFC 8879) | ☐ | ☐ | ☐ |
| Hybrid certificates (dual classical + PQC) | ☐ | ☐ | ☐ |
| IPsec IKEv2 with ML-KEM or PPK (RFC 8784) | ☐ | ☐ | ☐ |
| SSH mlkem768x25519 key exchange | ☐ | ☐ | ☐ |
| FIPS 140-3 validation for PQC algorithms | ☐ | ☐ | ☐ |
| CBOM (Cryptographic Bill of Materials) disclosure | ☐ | ☐ | ☐ |

## Migration Readiness Questions

| **Question** | **Vendor Response** |
| --- | --- |
| What is your published PQC migration roadmap and timeline? |  |
| Can customers configure algorithm selection, or does it require a vendor release? |  |
| How quickly can you swap to an alternative algorithm if one is deprecated? |  |
| Do you support hybrid mode (classical + PQC simultaneously)? |  |
| What is the expected performance impact of enabling PQC? |  |
| Are your PQC implementations based on NIST-validated libraries? |  |
| Can you provide a CBOM for your product? |  |
| What HSM vendors/firmware versions are supported for PQC operations? |  |
| What is your testing/certification timeline for FIPS 140-3 PQC validation? |  |
| How does your product handle PQC certificate chain sizes (>15 KB)? |  |

## Overall Assessment

| **PQC Readiness Rating:** | ☐ Ready   ☐ In Progress   ☐ Not Ready   ☐ No Plans |
| --- | --- |
| **Risk to Our Migration:** | ☐ Low   ☐ Medium   ☐ High   ☐ Critical |
| **Recommended Action:** |  |
| **Follow-up Date:** |  |

### Appendix G
