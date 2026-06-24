---
title: "The New Algorithms: A Practitioner’s Guide"
displayTitle: "Chapter 3: The New Algorithms: A Practitioner’s Guide"
section: "Chapters"
chapter: 3
order: 6
words: 2835
readingMinutes: 13
excerpt: "In Chapter 1, we learned that quantum computing breaks the math behind today’s encryption, not the concept of encryption itself. In Chapter 2, we mapped exactly which algorithms and protocols are vulnerable. Now we answer"
---

In Chapter 1, we learned that quantum computing breaks the math behind today’s encryption, not the concept of encryption itself. In Chapter 2, we mapped exactly which algorithms and protocols are vulnerable. Now we answer the next question: what are we replacing them with?

The good news is that the replacements are already here. NIST finalized the first three post-quantum standards in August 2024 and selected a fourth in March 2025, with a fifth in draft. These aren’t experimental. They’re the result of an eight-year international competition involving 82 submissions from 25 countries, whittled down through multiple rounds of analysis, attack, and optimization.<sup>1</sup>

This chapter introduces each algorithm in plain language: what mathematical problem it’s built on, what it does, how big its keys and signatures are, and when to use it. We’re not going to teach you the math; we’re going to give you the intuition you need to make architecture and procurement decisions.

## New Math, Same Mission

As we discussed in Chapter 1, today’s public-key cryptography relies on trapdoor functions built from two mathematical problems: **integer factorization** (RSA) and **discrete logarithms** (DH, ECC). Shor’s algorithm cracks both. The solution is to build trapdoor functions from different mathematical problems: problems that resist both classical and quantum attack.

NIST’s post-quantum standards draw from three distinct mathematical families, each offering a different set of tradeoffs:

![figure](/book-media/img-05.png)

*Figure 3.1 — PQC Algorithm Families*

| **Math Family** | **Core Problem** | **Algorithms** | **Tradeoff Profile** |
| --- | --- | --- | --- |
| **Lattice-Based** | Shortest Vector Problem (SVP) in high-dimensional lattices | ML-KEM (FIPS 203), ML-DSA (FIPS 204), FN-DSA (FIPS 206 draft) | Fast, moderate key sizes. The workhorse family. Most algorithms use this. |
| **Hash-Based** | Security of cryptographic hash functions (SHA-2/SHA-3) | SLH-DSA (FIPS 205), LMS/XMSS (SP 800-208) | Ultra-conservative security. Small keys, very large signatures. Slower. |
| **Code-Based** | Syndrome decoding in error-correcting codes | HQC (selected March 2025) | Backup KEM. Larger keys than lattices. Different math for diversity. |

NIST deliberately chose algorithms from multiple mathematical families. If a future breakthrough cracks lattice problems, the hash-based and code-based backups still stand. This **algorithmic diversity** is a core design principle of the post-quantum landscape.<sup>2</sup>

> **PLAIN-LANGUAGE SIDEBAR**
> Think of it like building three separate bridges across a canyon, each using different engineering principles: one suspension, one arch, one cantilever. If an earthquake reveals a flaw in suspension bridge design, the arch and cantilever bridges still hold. NIST built multiple mathematical bridges for the same reason.

## ML-KEM: The New Key Exchange (FIPS 203)

**What it replaces:** RSA key exchange, ECDH, X25519, Diffie-Hellman: any algorithm used to establish a shared secret between two parties.

**What it is:** ML-KEM stands for Module-Lattice-Based Key-Encapsulation Mechanism. It’s based on the CRYSTALS-Kyber algorithm, which won NIST’s competition and was renamed for standardization.<sup>3</sup>

### How It Works (The Intuition)

ML-KEM’s security is based on the **Module Learning With Errors (MLWE)** problem. Here’s the intuition: imagine a system of equations where the answers are slightly wrong: each one has a small random error added to it. Given the noisy answers, recovering the original secret is computationally infeasible, even for a quantum computer.

> **PLAIN-LANGUAGE SIDEBAR**
> Think of it this way: someone gives you the results of 1,000 math equations, but each answer is slightly off by a random amount. Could you figure out the original variables? For low-dimensional problems, maybe. But in the high-dimensional spaces ML-KEM operates in (hundreds of dimensions), the noise makes the problem impossibly hard. That hardness is the trapdoor.

Technically, ML-KEM is a **Key Encapsulation Mechanism (KEM)**, not a traditional key exchange. The distinction matters: in a KEM, one party generates a shared secret and “encapsulates” it using the other party’s public key. The recipient “decapsulates” it with their private key. The result is the same (a shared secret both parties can use for symmetric encryption), but the mechanics are slightly different from Diffie-Hellman’s interactive exchange.<sup>4</sup>

### The Numbers

| **Parameter Set** | **Public Key** | **Ciphertext** | **Secret Key** | **NIST Security Level** |
| --- | --- | --- | --- | --- |
| **ML-KEM-512** | 800 bytes | 768 bytes | 1,632 bytes | Level 1 (AES-128) |
| **ML-KEM-768** | 1,184 bytes | 1,088 bytes | 2,400 bytes | Level 3 (AES-192) |
| **ML-KEM-1024** | 1,568 bytes | 1,568 bytes | 3,168 bytes | Level 5 (AES-256) |
| **X25519 (classical)** | 32 bytes | 32 bytes | 32 bytes | — (broken by Shor’s) |

The size increase is real but manageable. ML-KEM-768 (the recommended default for most applications) adds about 1.1 KB to each side of a handshake. For a TLS connection, that’s barely noticeable. The performance story is actually encouraging: **ML-KEM is often faster than the elliptic curve algorithms it replaces** for key generation and encapsulation operations.<sup>5</sup>

> **⚠  MANDATE ALERT**
> CNSA 2.0 requires ML-KEM-1024 for National Security Systems (not ML-KEM-768). Commercial and non-NSS federal systems may use ML-KEM-768. Plan your parameter set selection based on your compliance requirements.

## ML-DSA: The New Digital Signature (FIPS 204)

**What it replaces:** RSA signatures, ECDSA, EdDSA: any algorithm used to prove identity and verify data integrity in certificates, code signing, and authentication.

**What it is:** ML-DSA stands for Module-Lattice-Based Digital Signature Algorithm, based on CRYSTALS-Dilithium. It’s NIST’s primary recommended signature scheme: the general-purpose workhorse.<sup>6</sup>

### How It Works (The Intuition)

ML-DSA uses a technique called **Fiat-Shamir with Aborts.** The signer creates a mathematical commitment, generates a challenge by hashing the message and commitment together, then computes a response. The clever part is the “aborts” mechanism: before publishing the response, the algorithm checks whether it would leak any information about the private key. If it does, it throws the result away and tries again with fresh randomness. This rejection sampling ensures the final signature is mathematically independent of the secret key’s internal structure.<sup>7</sup>

### The Numbers

| **Parameter Set** | **Public Key** | **Signature** | **Secret Key** | **NIST Level** |
| --- | --- | --- | --- | --- |
| **ML-DSA-44** | 1,312 bytes | 2,420 bytes | 2,560 bytes | Level 2 (AES-128) |
| **ML-DSA-65** | 1,952 bytes | 3,309 bytes | 4,032 bytes | Level 3 (AES-192) |
| **ML-DSA-87** | 2,592 bytes | 4,627 bytes | 4,896 bytes | Level 5 (AES-256) |
| **ECDSA P-256 (classical)** | 64 bytes | 64 bytes | 32 bytes | — (broken) |

This is where the sticker shock hits. An ML-DSA-65 signature is **3,309 bytes versus 64 bytes for ECDSA P-256**: a 50x increase. Public keys grow from 64 bytes to nearly 2 KB. For a TLS certificate chain with three certificates, the total signature and key payload could exceed 15–20 KB. We’ll dig into the protocol-level implications of this in Chapter 8.

The silver lining: **ML-DSA is actually faster than RSA-2048 for both signing and verification**—roughly 10x faster for signing operations.<sup>8</sup> The performance penalty compared to ECDSA exists but is modest on modern hardware. The real challenge isn’t CPU time. It’s bandwidth and packet size.

## SLH-DSA: The Conservative Backup (FIPS 205)

**What it replaces:** Same use cases as ML-DSA (digital signatures), but intended as a backup with a different security foundation.

**What it is:** SLH-DSA stands for Stateless Hash-Based Digital Signature Algorithm, based on SPHINCS+. Its security rests entirely on the strength of hash functions (SHA-2 or SHAKE), mathematical objects that have been studied intensively for decades and are extremely well understood.<sup>9</sup>

### Why It Matters

SLH-DSA is NIST’s insurance policy. If a future mathematical breakthrough weakens lattice-based cryptography (threatening both ML-KEM and ML-DSA), SLH-DSA remains standing because it’s built on completely different mathematics. Its security assumptions are the most conservative in the entire PQC portfolio.

The tradeoff is severe: SLH-DSA signatures are enormous. At the NIST Level 1 security (“small” variant), a signature is 7,856 bytes. At Level 5 with the “fast” variant, signatures can reach nearly 50 KB.<sup>10</sup> Public keys are tiny (32–64 bytes), but the signing process is significantly slower than ML-DSA.

SLH-DSA comes in two flavors for each security level: **"f" (fast)** optimizes for speed at the cost of larger signatures, and **"s" (small)** optimizes for signature size at the cost of speed.

**Best use cases:** Firmware signing, long-term document authentication, root CA certificates, and any context where the signature is created once and verified rarely but must remain trustworthy for decades. Not ideal for high-volume, latency-sensitive applications like TLS handshakes.

## FN-DSA: Compact Signatures (FIPS 206 — Draft)

**What it is:** FN-DSA stands for FFT over NTRU-Lattice-Based Digital Signature Algorithm, based on the FALCON submission. It offers the smallest signatures of any PQC signature scheme (roughly 666 bytes at Level 1 and 1,280 bytes at Level 5), making it attractive for bandwidth-constrained environments.<sup>11</sup>

**Why it isn’t the primary standard:** FN-DSA’s implementation requires Gaussian sampling using floating-point arithmetic, which is notoriously difficult to implement correctly and prone to side-channel attacks. NIST selected ML-DSA as the primary standard specifically because it is easier to implement securely. FN-DSA is the specialist tool, not the default.<sup>12</sup>

**Best use cases:** IoT devices, embedded systems, DNSSEC, and other environments where signature size is a critical constraint and the implementation team has deep cryptographic expertise.

## HQC: The Backup KEM (Expected 2027)

**What it is:** HQC stands for Hamming Quasi-Cyclic, a Key Encapsulation Mechanism built on **error-correcting codes** rather than lattices. NIST selected HQC in March 2025 as a backup to ML-KEM, with a finalized standard expected in 2027.<sup>13</sup>

HQC serves the same purpose as ML-KEM (establishing shared secrets for symmetric encryption) but uses fundamentally different mathematics. If a cryptanalytic breakthrough ever compromised lattice-based schemes, HQC would provide an alternative path to quantum-safe key exchange.

The tradeoff: HQC’s keys and ciphertexts are 3–4x larger than ML-KEM at equivalent security levels (roughly 4,500 bytes for a public key at Level 3, compared to 1,184 bytes for ML-KEM-768).<sup>14</sup> It also requires more computation. For now, ML-KEM remains the clear default for production deployments, with HQC as the strategic fallback.

> **PLAIN-LANGUAGE SIDEBAR**
> You don’t need to deploy HQC today. Think of it as the spare tire in your trunk: you hope you never need it, but you’re glad it’s there. Organizations designing for crypto-agility (covered in Chapter 6) should ensure their architectures can accommodate HQC if ML-KEM ever needs to be swapped out.

## Which Algorithm, When: The Practitioner’s Decision Guide

With five algorithms across three mathematical families, choosing the right one for each use case can feel overwhelming. It doesn’t need to be. Here’s the decision tree:

| **Use Case** | **Primary Algorithm** | **Backup / Alternative** | **Notes** |
| --- | --- | --- | --- |
| **TLS key exchange** | ML-KEM-768 (hybrid with X25519) | HQC (when standardized) | Hybrid mode recommended during transition |
| **TLS / web certificates** | ML-DSA-65 | SLH-DSA (if conservative posture needed) | Watch for certificate size impacts |
| **IPsec / VPN (NSS)** | ML-KEM-1024 + ML-DSA-87 | — (CNSA 2.0 mandates these) | Level 5 required for National Security Systems |
| **Code signing / firmware** | ML-DSA-65 or SLH-DSA | LMS/XMSS (stateful, if supported) | CNSA 2.0 prioritizes this use case first |
| **SSH key exchange** | ML-KEM-768 (hybrid with X25519) | — (OpenSSH 10.0 default) | Already deployed in latest OpenSSH |
| **Email encryption (S/MIME)** | ML-KEM-768 | HQC (future) | Awaiting S/MIME protocol updates |
| **IoT / embedded devices** | FN-DSA (when finalized) or ML-DSA-44 | SLH-DSA-128s (if signature frequency low) | Evaluate FN-DSA for size-constrained use cases |
| **Long-term archival signatures** | SLH-DSA | — (most conservative choice) | Hash-based security, highest long-term confidence |

### The 80/20 Rule

If the table above feels complex, here’s the simplification: **for 80% of use cases, you need exactly two algorithms:**

- **ML-KEM-768** for key exchange (replacing ECDH/X25519/DH)

- **ML-DSA-65** for digital signatures (replacing ECDSA/RSA signatures)

If you’re in a CNSA 2.0 environment, bump both to Level 5 (ML-KEM-1024 and ML-DSA-87). If you have specialized needs (ultra-conservative security, bandwidth constraints, firmware signing), the other algorithms fill those niches. But ML-KEM + ML-DSA covers the vast majority of the migration surface area.

> **MANDATE ALERT**
> **A Note on Implementation Security: Side-Channel Attacks**
> Even a theoretically secure algorithm can be broken by a careless implementation. PQC algorithms are susceptible to **side-channel attacks:** techniques that extract secret key material by observing execution time, power consumption, or electromagnetic emissions rather than attacking the math directly. Researchers have demonstrated side-channel key recovery against ML-KEM implementations, and Falcon’s (FN-DSA) floating-point arithmetic makes constant-time implementation especially difficult.
> The practical takeaway: always use vetted, validated implementations from established cryptographic libraries (OpenSSL, BoringSSL, liboqs, Windows CNG). Never roll your own PQC. Ensure your vendors’ implementations are tested against side-channel attacks, especially if you’re deploying on hardware where physical access is possible (IoT, OT, embedded systems). The AIVD/TNO PQC Migration Handbook specifically flags this as a risk that organizations frequently underestimate.

## What’s Next

You now understand what broke (Chapter 2), what replaces it (this chapter), and why these specific algorithms were chosen. But algorithms don’t deploy themselves. The next question is: who says you have to do this, and by when?

Chapter 4 maps the full regulatory landscape (NSM-10, CNSA 2.0, the Quantum Computing Cybersecurity Preparedness Act, NIST IR 8547, and the EU and UK timelines) so you know exactly which mandates apply to your organization and when the deadlines hit.

## Notes

The following sources support specific claims made in Chapter 3. Full bibliographic entries appear in the Bibliography.

**1.**  NIST Post-Quantum Cryptography Standardization project. Initiated 2016 with 82 submissions from 25 countries. Final standards FIPS 203, 204, 205 published August 13, 2024. Fifth algorithm (HQC) selected March 2025. See: https://csrc.nist.gov/projects/post-quantum-cryptography

**2.**  NIST explicitly sought algorithmic diversity. Dustin Moody (NIST PQC project lead): “We want to have a backup standard that is based on a different math approach than ML-KEM.” NIST news release, March 11, 2025.

**3.**  FIPS 203: Module-Lattice-Based Key-Encapsulation Mechanism Standard. August 2024. Based on CRYSTALS-Kyber. Specifies ML-KEM-512, ML-KEM-768, and ML-KEM-1024 parameter sets.

**4.**  NIST SP 800-227 (draft): Recommendations for Key-Encapsulation Mechanisms. Provides formal definitions and guidance for implementing KEMs, distinguishing them from traditional key agreement protocols like DH and ECDH.

**5.**  NIST SP 1800-38C (Preliminary Draft): Quantum Readiness—Testing Draft Standards for Interoperability and Performance. Volume C reports ML-KEM-768 handshake throughput competitive with or exceeding classical ECDH at higher security levels.

**6.**  FIPS 204: Module-Lattice-Based Digital Signature Standard. August 2024. Based on CRYSTALS-Dilithium. Specifies ML-DSA-44, ML-DSA-65, and ML-DSA-87 parameter sets.

**7.**  The Fiat-Shamir with Aborts paradigm for ML-DSA is described in FIPS 204, Section 3. For an accessible explanation: Lyubashevsky, V. “Fiat-Shamir With Aborts: Applications to Lattice and Factoring-Based Signatures.” ASIACRYPT 2009.

**8.**  ML-DSA signing performance approximately 100–200 microseconds vs. RSA-2048 at 2–5 milliseconds. See benchmarks in NIST SP 1800-38C and Open Quantum Safe project: https://openquantumsafe.org

**9.**  FIPS 205: Stateless Hash-Based Digital Signature Standard. August 2024. Based on SPHINCS+. Security relies solely on the collision resistance and preimage resistance of SHA-2 or SHA-3 (SHAKE) hash functions.

**10.**  SLH-DSA signature sizes from FIPS 205: SLH-DSA-SHA2-128s = 7,856 bytes; SLH-DSA-SHA2-256f = 49,856 bytes. Public key sizes range from 32 to 64 bytes across all parameter sets.

**11.**  FN-DSA (FALCON) is specified in draft FIPS 206. FN-DSA-512 signature: approximately 666 bytes. FN-DSA-1024 signature: approximately 1,280 bytes. Compact compared to ML-DSA but implementation complexity is significantly higher.

**12.**  NIST noted that FALCON’s Gaussian sampling over floating-point arithmetic makes constant-time implementation difficult, increasing vulnerability to side-channel attacks. See NIST PQC Round 3 Report, 2022.

**13.**  NIST announcement: “NIST Selects HQC as Fifth Algorithm for Post-Quantum Encryption.” March 11, 2025. HQC is based on Hamming Quasi-Cyclic codes. Draft standard expected 2026, final standard 2027.

**14.**  HQC key and ciphertext sizes at Level 3 (≈192-bit security): public key approximately 4,522 bytes, ciphertext approximately 9,042 bytes. Compare to ML-KEM-768: public key 1,184 bytes, ciphertext 1,088 bytes. Source: HQC specification, https://pqc-hqc.org

Next: Chapter 4 — The Regulatory Landscape
