---
title: "Algorithm Cheat Sheet"
displayTitle: "Algorithm Cheat Sheet"
section: "Appendices & Reference"
chapter: null
order: 16
words: 285
readingMinutes: 1
excerpt: "One-page reference for algorithm selection. Sizes are approximate and include DER/X.509 encoding overhead where applicable."
---

One-page reference for algorithm selection. Sizes are approximate and include DER/X.509 encoding overhead where applicable.

## Key Exchange / Encapsulation (replacing ECDH, DH, RSA key transport)

| **Algorithm** | **Public Key** | **Ciphertext** | **Security Level** | **Notes** |
| --- | --- | --- | --- | --- |
| **ML-KEM-512** | 800 bytes | 768 bytes | Level 1 (AES-128) | Fastest/smallest. Not recommended for high-value. |
| **ML-KEM-768** | 1,184 bytes | 1,088 bytes | Level 3 (AES-192) | **★ RECOMMENDED default for most use cases.** |
| **ML-KEM-1024** | 1,568 bytes | 1,568 bytes | Level 5 (AES-256) | Required for CNSA 2.0 / NSS. |
| **HQC (expected ~2027)** | ~2,249 bytes | ~4,481 bytes | Level 1/3 | Code-based backup KEM. Algorithmic diversity from ML-KEM. |

## Digital Signatures (replacing RSA, ECDSA, EdDSA, DSA)

| **Algorithm** | **Public Key** | **Signature** | **Security Level** | **Notes** |
| --- | --- | --- | --- | --- |
| **ML-DSA-44** | 1,312 bytes | 2,420 bytes | Level 2 (AES-128) | Smallest ML-DSA. Suitable where Level 3 not required. |
| **ML-DSA-65** | 1,952 bytes | 3,309 bytes | Level 3 (AES-192) | **★ RECOMMENDED default for general-purpose signing.** |
| **ML-DSA-87** | 2,592 bytes | 4,627 bytes | Level 5 (AES-256) | Required for CNSA 2.0 / NSS root CAs. |
| **SLH-DSA-SHA2-128s** | 32 bytes | 7,856 bytes | Level 1 (AES-128) | Hash-based. Conservative backup. Very large signatures. |
| **FN-DSA-512 (draft)** | 897 bytes | 666 bytes | Level 1 (AES-128) | Most compact signatures. Complex implementation (floating-point). Best for CA-level signing. |
| **FN-DSA-1024 (draft)** | 1,793 bytes | 1,280 bytes | Level 5 (AES-256) | Level 5 Falcon variant. Same implementation complexity caveats. |

### The 80/20 Rule

For 80% of enterprise migration scenarios, two algorithms cover your needs: **ML-KEM-768 for key exchange + ML-DSA-65 for signatures.** Start there. Optimize later.

### Appendix C
