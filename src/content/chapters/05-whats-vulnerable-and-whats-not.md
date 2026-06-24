---
title: "What’s Vulnerable and What’s Not"
displayTitle: "Chapter 2: What’s Vulnerable and What’s Not"
section: "Chapters"
chapter: 2
order: 5
words: 2652
readingMinutes: 12
excerpt: "Chapter 1 explained why quantum computing threatens our cryptographic infrastructure. This chapter answers the next logical question: what, specifically, is at risk?"
---

Chapter 1 explained why quantum computing threatens our cryptographic infrastructure. This chapter answers the next logical question: what, specifically, is at risk?

Not everything breaks. That’s important to understand upfront. Quantum computing breaks certain categories of cryptographic algorithms while leaving others largely intact. Knowing which is which (and understanding how they’re layered inside the protocols you actually run) is the foundation of every migration decision you’ll make.

![figure](/book-media/img-04.png)

*Figure 2.1 — TLS Protocol Stack: What’s Quantum-Vulnerable?*

## The Quantum Risk Scorecard

We can classify every cryptographic algorithm currently in widespread use into one of three categories based on its vulnerability to quantum attack:

> **❌  BROKEN: Destroyed by Shor’s Algorithm**
> All public-key algorithms based on integer factorization, discrete logarithms, or elliptic curve discrete logarithms. A cryptographically relevant quantum computer (CRQC) renders these completely insecure: no reasonable increase in key size can help.

> **⚠  WEAKENED: Reduced by Grover’s Algorithm**
> All symmetric encryption and hash functions. Grover’s algorithm halves their effective security strength. The fix is straightforward: double the key size. AES-256 remains safe; AES-128 needs upgrading.

> **✅  SAFE: No Known Quantum Advantage**
> Post-quantum algorithms (ML-KEM, ML-DSA, SLH-DSA) and sufficiently strong symmetric algorithms (AES-256, SHA-384/512). These are built on mathematical problems for which no efficient quantum algorithm is known.

## Algorithm-by-Algorithm: The Vulnerability Map

The following table is your reference sheet. Tear this page out and tape it to your monitor if you have to. This is the single most important classification in the book.

| **Algorithm** | **Type** | **Quantum Threat** | **Status** | **Action Required** |
| --- | --- | --- | --- | --- |
| **RSA (all key sizes)** | Key exchange, digital signatures | **Shor’s: Broken** | Deprecated 2030, disallowed 2035 | Replace with ML-KEM (key exchange) or ML-DSA (signatures) |
| **ECDSA / EdDSA** | Digital signatures | **Shor’s: Broken** | Deprecated 2030, disallowed 2035 | Replace with ML-DSA or SLH-DSA |
| **ECDH / X25519 / X448** | Key agreement | **Shor’s: Broken** | Deprecated 2030, disallowed 2035 | Replace with ML-KEM |
| **DH / DHE** | Key exchange | **Shor’s: Broken** | Deprecated 2030, disallowed 2035 | Replace with ML-KEM |
| **DSA** | Digital signatures | **Shor’s: Broken** | Already deprecated by NIST | Replace with ML-DSA |
| **AES-128** | Symmetric encryption | **Grover’s: Weakened** | Upgrade recommended | Upgrade to AES-256 |
| **SHA-1** | Hash function | **Grover’s + classical weaknesses** | Already broken classically | Replace immediately (SHA-256 minimum) |
| **3DES / Blowfish** | Symmetric encryption | **Grover’s: Unacceptable** | Already deprecated | Replace immediately (AES-256) |
| **AES-256** | Symmetric encryption | **Grover’s: Adequate** | 128-bit effective, safe | No change needed |
| **SHA-256 / SHA-384 / SHA-512** | Hash functions | **Grover’s: Adequate** | 128-bit+ effective, safe | No change needed (avoid SHA-1) |
| **HMAC-SHA-256+** | Message authentication | **No known quantum advantage** | Safe | No change needed |

Source: Classification based on NIST IR 8547 (Transition to Post-Quantum Cryptography) and NIST SP 800-131A Rev. 3.<sup>1</sup>

## Protocol by Protocol: Where Quantum Hits Your Network

Algorithms don’t exist in isolation. They’re embedded inside protocols. The same RSA key might appear in a TLS certificate, an IPsec IKE negotiation, and an SSH login. Understanding which protocols are affected, and where inside each protocol the vulnerable algorithms sit, is essential for planning your migration.

### TLS (Transport Layer Security)

TLS is the most widely deployed security protocol on the planet. It protects web traffic (HTTPS), API calls, email transmission (STARTTLS), and countless other connections. In Chapter 1, we walked through the TLS 1.3 handshake in two acts. Here’s where quantum hits each act:

**Handshake (key exchange):** TLS 1.3 uses ECDHE (X25519 or P-256) for key agreement. **Broken by Shor’s.** Must be replaced with ML-KEM or a hybrid (ML-KEM + X25519).<sup>2</sup>

**Handshake (authentication):** Server certificates typically use ECDSA or RSA signatures. **Broken by Shor’s.** Must be replaced with ML-DSA or SLH-DSA signatures.<sup>3</sup>

**Bulk encryption:** AES-128-GCM or AES-256-GCM. AES-256 is **safe.** AES-128 should be upgraded to AES-256 as a precaution.

**Record integrity:** HMAC or AEAD (built into GCM). **Safe.** No change needed.

> **PLAIN-LANGUAGE SIDEBAR**
> In a TLS session, the handshake is the vulnerable part. Once the handshake completes and symmetric keys are established, the bulk data transfer is quantum-safe (assuming AES-256). This is why the PQC migration for TLS focuses almost entirely on the handshake: replacing ECDHE with ML-KEM and replacing ECDSA/RSA certificate signatures with ML-DSA.

### IPsec / IKEv2

IPsec protects site-to-site VPNs, remote access VPNs, and classified network tunnels (including many DoD and federal environments). The IKEv2 protocol handles key exchange and authentication before the IPsec tunnel is established.

**IKE key exchange:** Uses DH or ECDH groups. **Broken by Shor’s.** Must be replaced with ML-KEM. The IETF is developing PQC profiles for IKEv2, and the NSA’s CNSA 2.0 specifies ML-KEM-1024 for IPsec.<sup>4</sup>

**IKE authentication:** Typically RSA or ECDSA certificate-based, or pre-shared keys (PSKs). Certificate-based auth is **broken by Shor’s.** PSK-based authentication is **quantum-safe** (symmetric). This is why the NSA has recommended post-quantum pre-shared keys (PPKs) as an interim measure.<sup>5</sup>

**ESP encryption:** AES-256-GCM or AES-256-CBC. **Safe.**

### SSH (Secure Shell)

SSH is the primary remote administration protocol for Linux/Unix systems, network devices, and cloud infrastructure. It’s also widely used for secure file transfer (SFTP/SCP) and Git operations.

**Key exchange:** Typically ECDH (curve25519-sha256) or DH. **Broken by Shor’s.** OpenSSH 9.0+ introduced a hybrid post-quantum key exchange (sntrup761x25519-sha512) using a lattice-based algorithm. OpenSSH 10.0 defaults to mlkem768x25519-sha256.<sup>6</sup>

**Authentication:** RSA, ECDSA, or Ed25519 keys for user/host auth. **Broken by Shor’s.** Must be replaced with PQC signature algorithms. Note: password-based auth (derived via symmetric hashing) is not directly affected by Shor’s but has its own well-known security limitations.

**Session encryption:** AES-256 (chacha20-poly1305 or aes256-gcm). **Safe.**

### PKI and Digital Certificates

Public Key Infrastructure is the trust fabric of the internet. Every TLS certificate, code signing certificate, email certificate, and device identity certificate relies on public-key cryptography for its digital signature.

This is arguably the most complex PQC migration challenge. Certificates are everywhere: embedded in web servers, load balancers, API gateways, IoT devices, mobile apps, firmware, smart cards, and hardware security modules (HSMs). They’re issued by Certificate Authorities (CAs) in hierarchical trust chains, and changing the signature algorithm means updating every link in that chain.<sup>7</sup>

**Root and intermediate CA signatures:** RSA or ECDSA. **Broken by Shor’s.** Every certificate in the chain must eventually use PQC signatures.

**End-entity certificates:** RSA or ECDSA public keys and signatures. **Broken by Shor’s.** Certificate sizes will increase significantly: ML-DSA-87 signatures are 4,627 bytes vs. 64 bytes for ECDSA P-256.<sup>8</sup>

> **⚠  MANDATE ALERT**
> Certificate size explosion is a real operational concern. An ML-DSA-87 public key is 2,592 bytes; an ML-DSA-87 signature is 4,627 bytes. Compare that to ECDSA P-256: 64-byte public key, 64-byte signature. A TLS certificate chain with three PQC certificates could exceed 20 KB, potentially fragmenting the TLS handshake across multiple TCP packets and causing performance issues on constrained networks. Chapter 8 covers this in detail.

### Code Signing and Software Supply Chain

Every signed software package, firmware update, OS patch, and container image relies on digital signatures to prove authenticity and integrity. These signatures almost universally use RSA or ECDSA.

**Code signing signatures:** RSA or ECDSA. **Broken by Shor’s.** An attacker with a CRQC could forge signatures on malicious software, making it appear to come from a trusted vendor. This is why the NSA’s CNSA 2.0 timeline prioritizes software and firmware signing first, with exclusive use of PQC signatures required by 2030.<sup>9</sup>

This has particular implications for long-lived systems: embedded devices, SCADA controllers, medical equipment, and military platforms that may run the same firmware for a decade or more. A signature that was secure when applied in 2024 may be forgeable by 2035. The integrity of every software update these systems have ever received becomes retroactively questionable.

### Email Security (S/MIME, PGP)

Encrypted and signed email protocols rely on public-key cryptography for both confidentiality (encrypting the message to the recipient’s public key) and authentication (signing the message with the sender’s private key). Both operations are **broken by Shor’s.**

Emails encrypted with RSA or ECC and captured today can be retroactively decrypted once a CRQC is available. For organizations handling attorney-client privileged communications, classified information, medical records, or trade secrets via encrypted email, the HNDL risk is acute and present.

## Not All Data Is Equal: The HNDL Risk Matrix

Harvest Now, Decrypt Later doesn’t affect all data equally. The risk depends on two factors: **how long the data remains sensitive** and **how likely it is to have been intercepted.**

We can use these two dimensions to classify your organization’s data into quantum risk tiers:

| **Risk Tier** | **Data Sensitivity Lifetime** | **Examples** | **HNDL Urgency** |
| --- | --- | --- | --- |
| **CRITICAL** | 25+ years (classified, strategic) | National security intel, weapons designs, long-term trade secrets, diplomatic comms | **Immediate. Already at risk from HNDL. Migrate now.** |
| **HIGH** | 10–25 years | Medical records, financial data, legal privilege, M&A strategy, PII under GDPR/HIPAA | Urgent. Begin migration planning now. Prioritize HNDL-exposed channels. |
| **MODERATE** | 3–10 years | Business strategy, competitive analysis, customer databases, internal comms | Plan migration within NIST timeline. Prioritize based on exposure. |
| **LOW** | < 3 years | Session tokens, ephemeral API keys, transient web traffic, public marketing content | Migrate per normal upgrade cycles. Low HNDL exposure. |

The critical insight: **your migration priority should be driven by data sensitivity lifetime, not by when you think Q-Day will arrive.** If your organization handles data in the CRITICAL or HIGH tiers and that data crosses a network (even an encrypted one), the HNDL clock is already running.

## The Official Clock: NIST’s Deprecation Timeline

In late 2024, NIST published IR 8547, “Transition to Post-Quantum Cryptography,” which for the first time set explicit deprecation dates for quantum-vulnerable algorithms.<sup>1</sup> This document transformed PQC migration from a best-practice recommendation into a compliance requirement with hard deadlines:

- **By 2030:** RSA, ECDSA, EdDSA, DH, and ECDH will be **deprecated** at the 112-bit security level. Organizations should have migration plans in place and active.

- **By 2035:** All quantum-vulnerable public-key algorithms will be **disallowed**: completely removed from NIST standards. No exceptions.<sup>10</sup>

For context, “deprecated” means the algorithm is still technically permitted but actively discouraged: new systems should not use it. “Disallowed” means NIST-compliant systems cannot use it at all. If your organization’s compliance framework references NIST standards (and nearly all federal and most private-sector frameworks do), 2035 is the hard stop.

> **⚠  MANDATE ALERT**
> Don’t let the 2035 date create a false sense of comfort. The SHA-1 to SHA-2 migration (a far simpler cryptographic transition than PQC) took the industry over 12 years. The PQC transition involves replacing algorithms across every protocol layer, re-issuing every certificate, updating every HSM, and testing interoperability across every vendor in your stack. If you start in 2030, you are almost certainly too late for the 2035 deadline.

## What’s Not Vulnerable: A Reassuring List

It’s easy to read the preceding sections and feel like everything is on fire (insert dog in computer room on fire meme). It’s not. Here’s what you can stop worrying about:

- **AES-256 is quantum-safe.** The symmetric workhorse of the internet isn’t going anywhere. If you’re already using AES-256, you’re good.

- **SHA-256 and SHA-384/512 are quantum-safe for practical purposes.** Grover’s weakens them, but the effective security levels remain computationally infeasible to attack.

- **HMAC constructions are safe.** Message authentication codes built on SHA-256+ are not meaningfully threatened.

- **Symmetric key derivation functions (HKDF, PBKDF2) are safe.** These are symmetric operations and inherit the Grover’s-halving property, but with 256-bit inputs, the remaining 128-bit security is more than sufficient.

- **Random number generation is safe.** CSPRNGs (cryptographically secure pseudorandom number generators) are not affected by known quantum algorithms. The randomness foundation of your cryptographic stack remains solid.

The quantum threat is real but targeted. It’s an asymmetric crypto problem first and foremost, with a manageable symmetric cleanup alongside it. The sky is falling on RSA, ECC, and DH. The sky is holding just fine over AES-256.

## What’s Next

Now that we know what is broken and what is safe, the next question is: what are we replacing the broken algorithms with? Chapter 3 takes you inside the new NIST post-quantum standards (ML-KEM, ML-DSA, SLH-DSA, and the upcoming FN-DSA and HQC) and explains how they work, what their tradeoffs are, and why NIST chose the mathematical foundations it did.

## Notes

The following sources support specific claims made in Chapter 2. Full bibliographic entries appear in the Bibliography.

**1.**  National Institute of Standards and Technology. NIST IR 8547 (Initial Public Draft), “Transition to Post-Quantum Cryptography.” November 2024. Tables 1–5 classify quantum-vulnerable and quantum-resistant algorithms. NIST also published SP 800-131A Rev. 3 (November 2024) updating transition guidance with PQC inclusion and setting deprecation targets. Dustin Moody (NIST) confirmed the 2030 deprecation / 2035 disallowance timeline at the RWC PQC Conference, March 2025.

**2.**  IETF draft-ietf-tls-mlkem-key-agreement specifies ML-KEM integration into TLS 1.3 key exchange. Hybrid approaches combining ML-KEM with X25519 are already deployed in Chrome (Google) and Cloudflare as of 2024.

**3.**  TLS certificate signature migration is tracked in IETF drafts and the PKI Consortium’s PQC working group. Hybrid certificates (containing both classical and PQC signatures) are under active development to ease the transition period.

**4.**  NSA CNSA 2.0 specifies ML-KEM-1024 for key establishment in IPsec (National Security Systems). See: draft-guthrie-cnsa2-ipsec-profile for the CNSA 2.0 IPsec integration profile. Traditional networking equipment must support CNSA 2.0 by 2026 and use it exclusively by 2030.

**5.**  Post-Quantum Pre-Shared Keys (PPKs) for IKEv2 are specified in RFC 8784. This allows organizations to add a quantum-resistant layer to existing IPsec tunnels without waiting for full PQC algorithm integration: effectively a stopgap measure.

**6.**  OpenSSH 9.0 (April 2022) introduced sntrup761x25519-sha512 hybrid key exchange by default. OpenSSH 10.0 (April 2025) switched the default to mlkem768x25519-sha256, aligning with NIST’s ML-KEM standard. See IETF draft-ietf-sshm-mlkem-hybrid-kex.

**7.**  NIST SP 1800-38A (Migration to Post-Quantum Cryptography, Vol. A) identifies PKI migration as one of the most complex aspects of the PQC transition, noting that certificate chains, trust hierarchies, and cross-certification relationships all require coordinated updates.

**8.**  ML-DSA-87 key and signature sizes from FIPS 204. Public key: 2,592 bytes. Signature: 4,627 bytes. Compare to ECDSA P-256: public key 64 bytes, signature 64 bytes. ML-KEM-1024 ciphertext is 1,568 bytes vs. 32 bytes for X25519. These size increases have meaningful performance implications for constrained networks and devices.

**9.**  NSA CNSA 2.0 Algorithm Guidance (PP-22-1338, Ver. 1.0, September 2022). Software and firmware signing must begin transitioning immediately, support CNSA 2.0 by 2025, and exclusively use CNSA 2.0 by 2030. This is the earliest mandatory deadline in the CNSA 2.0 timeline.

**10.**  NIST IR 8547 timeline: quantum-vulnerable algorithms at 112-bit security strength deprecated after 2030; all quantum-vulnerable algorithms at any security strength disallowed after 2035. This applies to RSA, DSA, ECDSA, EdDSA, DH, ECDH, and related schemes as listed in Tables 2 and 4 of the document.

Next: Chapter 3 — The New Algorithms: A Practitioner’s Guide
