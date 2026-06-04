---
title: "Hybrid Mode: Bridging Classical and Quantum-Safe"
displayTitle: "Chapter 7: Hybrid Mode: Bridging Classical and Quantum-Safe"
section: "Chapters"
chapter: 7
order: 10
words: 2942
readingMinutes: 13
excerpt: "In an ideal world, you’d flip a switch and every system in your environment would instantly use post-quantum algorithms. In the real world, migration happens gradually—and during that transition, classical and post-quant"
---

In an ideal world, you’d flip a switch and every system in your environment would instantly use post-quantum algorithms. In the real world, migration happens gradually—and during that transition, classical and post-quantum cryptography need to coexist. That coexistence is called **hybrid mode**, and it’s the dominant deployment pattern for PQC today.

This chapter explains what hybrid mode is, why it matters, how it works across TLS, IPsec, and SSH, and where the approach has limitations. It also addresses a question you’ll inevitably encounter: “What about Quantum Key Distribution?”

## Why Hybrid? The Belt-and-Suspenders Argument

The post-quantum algorithms in FIPS 203, 204, and 205 have been rigorously evaluated through an eight-year international competition. But they are younger than the classical algorithms they replace. RSA has been scrutinized for over 40 years. ML-KEM has been scrutinized for roughly 8. The cryptographic community has high confidence in the new algorithms—but not 40 years of confidence.

Hybrid mode provides a hedge: **combine a classical algorithm with a PQC algorithm so that the system remains secure as long as at least one of them holds.** If ML-KEM is someday broken by a novel attack, the classical X25519 component still protects the session. If a quantum computer arrives and breaks X25519, the ML-KEM component protects it. You need to break both to compromise the connection.1

> **PLAIN-LANGUAGE SIDEBAR**
> Think of hybrid mode like a deadbolt paired with a smart lock on your front door. If someone picks the deadbolt, the smart lock still holds. If someone hacks the smart lock, the deadbolt still holds. An attacker has to defeat both to get in. That’s the security guarantee of hybrid cryptography.

NIST IR 8547 explicitly supports hybrid implementations during the transition period.2 ENISA recommends hybrid schemes for EU organizations. The UK NCSC endorses hybrid key exchange. And the real-world deployment numbers speak for themselves: as of September 2025, approximately 43% of human-generated HTTPS connections to Cloudflare used hybrid PQC key exchange.3

## Hybrid TLS: Already in Your Browser

If you’re reading this chapter in Chrome, Edge, Brave, or another Chromium-based browser, there’s a good chance your current connection is already using hybrid PQC key exchange—and you didn’t do a thing to enable it.

The dominant hybrid TLS key exchange is **X25519MLKEM768**, which combines the classical X25519 elliptic curve key agreement with ML-KEM-768 post-quantum key encapsulation. The IETF has formalized this in draft-ietf-tls-ecdhe-mlkem, specifying three hybrid groups:4

| **Hybrid Group** | **Components** | **Client Key Share Size** | **Security Level** |
| --- | --- | --- | --- |
| **X25519MLKEM768** | X25519 + ML-KEM-768 | 1,216 bytes | Level 3 (AES-192) |
| **SecP256r1MLKEM768** | P-256 + ML-KEM-768 | 1,249 bytes | Level 3 (FIPS) |
| **SecP384r1MLKEM1024** | P-384 + ML-KEM-1024 | 1,665 bytes | Level 5 (AES-256) |
| X25519 alone (classical) | X25519 only | 32 bytes | — (broken by Shor’s) |

The overhead is modest: X25519MLKEM768 adds approximately 1.1 KB to the client’s key share compared to classical X25519. In practice, this adds only 1–2 milliseconds to the TLS handshake—imperceptible to users. Multiple studies and production deployments have confirmed that the performance impact of hybrid key exchange is negligible on modern networks.5

### Who’s Already Deployed

- **Google Chrome:** Enabled X25519MLKEM768 by default for TLS 1.3 connections. Previously used the pre-standard X25519Kyber768Draft00, now migrating to the final standard.

- **Cloudflare:** 43% of human HTTPS traffic using hybrid PQC as of September 2025. Scanning origins to enable hybrid edge-to-origin connections automatically.3

- **AWS:** Hybrid TLS support in s2n-tls and AWS services. Contributors to the IETF hybrid TLS draft.

- **Apple:** Secured iMessage with PQ3 protocol (PQC key exchange) since iOS 17.4. Safari hybrid TLS in progress.

- **Signal:** Integrated X25519 + Kyber hybrid key exchange into the Signal Protocol.

The point: hybrid PQC isn’t experimental. It’s production-grade infrastructure that billions of connections use daily. The question for your organization isn’t whether hybrid works—it’s when you’ll enable it on your own infrastructure.

## The Bridge Architecture: Front-Side PQC, Back-Side Classical

For most enterprises, the fastest path to PQC progress is not upgrading every application, library, and origin server simultaneously. It’s upgrading the edge—the TLS termination point where internet traffic enters your environment.

The **bridge architecture** works like this: your TLS termination device (load balancer, reverse proxy, ADC) negotiates hybrid TLS 1.3 with modern clients on the front side while maintaining classical TLS 1.2 or TLS 1.3 connections to backend origins. The internet-exposed leg is PQC-hardened against HNDL; the internal leg remains classical until origins are upgraded. In federal and enterprise architecture vocabulary, this pattern is also called a **cryptographic proxy layer**—a dedicated enforcement point that performs cryptographic upgrade on behalf of downstream systems that aren’t yet PQC-capable. Both terms describe the same architecture; “bridge” emphasizes the temporal aspect (carrying systems across the migration), while “cryptographic proxy layer” emphasizes the structural aspect (a distinct layer in the trust architecture).6

![figure](/book-media/img-09.png)

*Figure 7.1 — The Bridge Architecture: Front-Side PQC, Back-Side Classical*

| **Leg** | **Protocol State** | **What It Means** |
| --- | --- | --- |
| **Browser → Edge Device** | TLS 1.3 + hybrid key exchange (X25519MLKEM768) | Front door is PQC-hardened. HNDL risk mitigated for the internet-facing leg. |
| **Inside Edge Device** | Traffic terminated and decrypted | Policy enforcement, inspection, logging, and routing continue unchanged. |
| **Edge Device → Origin** | Classical TLS 1.2 or TLS 1.3 (separate session) | Backend is NOT post-quantum hardened. Useful bridge, not end-to-end PQ. |

> **F5 PERSPECTIVE**
> **BIG-IP as the PQC Bridge**
> This bridge architecture maps directly to BIG-IP’s deployment model. BIG-IP 17.5.1 added support for X25519MLKEM768 hybrid key exchange in TLS 1.3 on both client and server sides. BIG-IP v21.1 expands PQC cipher support with hybrid TLS cipher groups and adds quantum-resistant TLS/SSL VPN tunneling through BIG-IP Zero Trust Access.
> The operational value: a small number of internet-facing VIPs can be upgraded to hybrid TLS before hundreds of origin servers are touched. Application teams gain runway to upgrade Apache, Java, OpenSSL, PKI workflows, and HSM dependencies in a controlled sequence. BIG-IP preserves its existing visibility—decrypted traffic remains available for routing, security policy, logging, and application controls.
> **An honest assessment:** this architecture hardens the front door first. It does not make the full application path post-quantum safe if the backend is still classical. The backend leg, while less exposed to external interception, still requires migration on the timeline established in Chapter 6. BIG-IP is the starting point, not the whole program.

## Hybrid IPsec: Pre-Shared Keys as a Stopgap

IPsec environments—particularly in DoD and federal networks—face a different hybrid challenge. Full PQC integration into IKEv2 is still maturing through IETF drafts, and many VPN devices don’t yet support ML-KEM in their key exchange.

The interim solution is **Post-Quantum Pre-Shared Keys (PPKs)**, specified in RFC 8784. PPKs add a quantum-resistant pre-shared secret to the IKEv2 key derivation process—effectively layering a symmetric (quantum-safe) secret on top of the existing classical key exchange. Even if an adversary captures the IKE handshake and later breaks the DH/ECDH component with a quantum computer, the PPK ensures the derived session keys are still protected.7

PPKs are a bridge, not a destination. The long-term solution is native ML-KEM integration in IKEv2, which the IETF and NSA are actively developing through the CNSA 2.0 IPsec profile.8 But for organizations that need quantum-resistant VPN tunnels today, PPKs are the fastest path available and are already supported by multiple VPN vendors.

## Hybrid SSH: Already the Default

SSH may be the simplest hybrid success story. OpenSSH introduced hybrid post-quantum key exchange earlier than most protocols, and it’s now the default.

- **OpenSSH 9.0 (April 2022):** Introduced sntrup761x25519-sha512 as the default key exchange. This combined a lattice-based algorithm (NTRU Prime) with X25519.

- **OpenSSH 10.0 (April 2025):** Switched the default to mlkem768x25519-sha256, aligning with NIST’s ML-KEM standard.9

If your servers are running a current OpenSSH version, your SSH key exchanges are already quantum-safe in hybrid mode. Authentication (host and user keys) still uses classical algorithms and will need migration to PQC signatures—but the key exchange leg is handled.

## Hybrid Certificates: The Harder Problem

Hybrid key exchange is solved. Hybrid authentication—specifically, hybrid certificates—is significantly harder.

A **hybrid certificate** carries two public keys and two signatures: one classical (e.g., ECDSA) and one post-quantum (e.g., ML-DSA). Old clients that don’t understand PQC can validate the classical signature and ignore the PQC component. New clients can validate both. This ensures backward compatibility during the transition.

The challenge: hybrid certificates are even larger than pure PQC certificates. A certificate with both an ECDSA and ML-DSA-65 signature carries the overhead of both—roughly 5+ KB for a single certificate, compared to ~1 KB for today’s ECDSA certificates. In a three-certificate chain, the overhead becomes significant and can trigger TLS handshake fragmentation. Chapter 8 covers this in detail.10

For now, the industry approach is: deploy hybrid key exchange first (it’s the HNDL priority) and defer hybrid certificate migration until the size and interoperability challenges are resolved. Chrome, NIST, and the IETF are all aligned on this sequencing.

## What About Quantum Key Distribution?

In customer conversations about PQC, someone will inevitably ask: “Why don’t we just use Quantum Key Distribution instead?” It’s a fair question. QKD uses the physics of quantum mechanics—not mathematical trapdoors—to distribute encryption keys, and its security is theoretically guaranteed by the laws of nature rather than computational hardness. That sounds like the ultimate solution.

It’s not. At least not for most organizations. Here’s why.

**QKD requires dedicated physical infrastructure** —typically fiber optic links or satellite channels—between every pair of communicating parties. It cannot operate over the existing internet. It cannot protect a connection between a mobile device and a web server. It cannot secure email. It doesn’t scale to the millions of connections per second that modern applications demand.11

**QKD provides key distribution only.** It does not authenticate. It cannot verify that the other party is who they claim to be. To use QKD securely, you still need classical or post-quantum digital signatures for authentication—which means you need PQC anyway.12

**QKD has limited range.** Current fiber-based QKD systems work over distances of roughly 100–200 km before requiring “trusted nodes” (relay points that must be physically secured). Quantum repeaters that could extend the range are still in early research stages.

**Major security agencies recommend against QKD for most use cases.** The NSA does not support QKD for protecting National Security Systems. The UK NCSC states: “PQC is the best mitigation to the threat to cryptography from quantum computers” and will not endorse QKD for government or military applications. ANSSI (France), BSI (Germany), and NLNCSA (Netherlands) have all taken similar positions.13 The November 18, 2025 DoW CIO memorandum *Preparing for Migration to Post Quantum Cryptography* made this position binding for the Department of War: DoW Components are prohibited from testing, evaluating, piloting, using, or procuring QKD—or any solution combining QKD with other cryptographic key establishment—for confidentiality, authenticity, integrity, key distribution, or randomness generation, absent specific exception from the DoW CIO PQC Directorate. See Chapter 4 for the full memo treatment.14

> **PLAIN-LANGUAGE SIDEBAR**
> QKD is a real technology with genuine strengths, and it has a role in specialized, high-security, point-to-point links where dedicated fiber infrastructure already exists and the cost is justified. China has deployed a working QKD network of approximately 5,000 km and a QKD satellite. The EU’s EuroQCI initiative is building an EU-wide QKD network. These are significant investments.
> But for the vast majority of organizations—protecting web applications, VPN tunnels, API traffic, email, and cloud workloads—PQC is the answer. QKD and PQC can complement each other in specialized environments, but PQC is the practical, standards-based, deployable-today solution for enterprise cryptographic migration.

## From Hybrid to Pure PQC: When to Drop the Classical Half

Hybrid mode is a bridge, not a destination. Eventually—as confidence in PQC algorithms matures and classical algorithms are disallowed by NIST—organizations will transition from hybrid to pure PQC. The timing depends on your risk posture:

- **2026–2030:** Deploy hybrid everywhere. This is the belt-and-suspenders phase. Classical algorithms are still permitted; PQC algorithms are still accumulating cryptanalytic scrutiny. Hybrid gives you quantum safety without betting everything on the new math.

- **2030–2033:** Begin transitioning high-confidence systems to pure PQC. By this point, ML-KEM and ML-DSA will have had 6+ years of post-standardization scrutiny. NIST will have deprecated classical algorithms at the 112-bit level. New systems should default to PQC-only.

- **2033–2035:** Complete the transition. NIST disallows all quantum-vulnerable algorithms. Hybrid mode becomes unnecessary because the classical component no longer adds value—and may introduce unnecessary complexity and bandwidth overhead.

The crypto-agility principles from Chapter 6 ensure you can make this transition smoothly: if your architecture is modular and policy-driven, switching from hybrid to pure PQC is a configuration change, not a redesign.

## What’s Next

This chapter covered the deployment patterns for running classical and PQC side by side. But how do these patterns actually play out at the protocol level? What happens to TLS handshake sizes when PQC certificates enter the picture? How does IPsec IKEv2 change when ML-KEM replaces DH? What does a PQC SSH session look like on the wire?

Chapter 8 takes you inside each protocol—TLS, IPsec, SSH, and PKI—with the technical detail your engineering teams need to plan and execute the migration.

## Notes

The following sources support specific claims made in Chapter 7. Full bibliographic entries appear in the Bibliography.

**1.**  The hybrid security guarantee—secure as long as at least one component algorithm holds—is formalized in IETF draft-ietf-tls-hybrid-design. NIST IR 8547 (Section 4.1) describes hybrid approaches as combining “a classical algorithm and a PQC algorithm into a composite mechanism, intended to be secure as long as at least one of the component algorithms is secure.”

**2.**  NIST IR 8547 (Initial Public Draft), “Transition to Post-Quantum Cryptography Standards.” November 2024. Explicitly supports hybrid implementations during the transition period.

**3.**  Cloudflare Blog, “Automatically Secure: How We Upgraded 6,000,000 Domains.” September 2025. Reports approximately 43% of human-generated connections using hybrid PQC key exchange as of mid-September 2025.

**4.**  IETF draft-ietf-tls-ecdhe-mlkem (draft-04, February 2026). Specifies three hybrid groups for TLS 1.3: X25519MLKEM768 (0x11EC), SecP256r1MLKEM768, and SecP384r1MLKEM1024. Authored by Kwiatkowski (PQShield), Kampanakis (AWS), Westerbaan (Cloudflare), and Stebila (University of Waterloo).

**5.**  NIST SP 1800-38C (Preliminary Draft): Quantum Readiness—Testing Draft Standards. Performance benchmarking showed hybrid ML-KEM + ECDH key exchange added only 1–2 milliseconds to TLS handshake latency in most configurations. Cloudflare’s production data confirms negligible user-facing impact.

**6.**  Bridge architecture concept described in F5, Inc. internal PQC field guidance (2025). BIG-IP 17.5.1 supports X25519MLKEM768 hybrid key exchange in TLS 1.3 on both client and server sides. BIG-IP v21.1 expands PQC cipher support.

**7.**  RFC 8784, “Mixing Preshared Keys in the Internet Key Exchange Protocol Version 2 (IKEv2) for Post-Quantum Security.” Specifies how to incorporate a post-quantum pre-shared key into IKEv2 key derivation.

**8.**  NSA. draft-guthrie-cnsa2-ipsec-profile: CNSA Suite 2.0 Profile for IPsec. Specifies ML-KEM-1024 for key establishment in IPsec for National Security Systems.

**9.**  OpenSSH 10.0 Release Notes (April 2025). Default key exchange changed to mlkem768x25519-sha256. See: IETF draft-ietf-sshm-mlkem-hybrid-kex for the specification.

**10.**  Hybrid certificate sizes and TLS handshake fragmentation are covered in detail in Chapter 8. The PKI Consortium’s PQC working group and IETF are developing dual-key certificate formats. Chrome has explicitly stated that certificate migration requires alternative approaches (Merkle Tree Certificates, trust expressions) due to size constraints.

**11.**  NSA Cybersecurity Advisory, “Quantum Key Distribution (QKD) and Quantum Cryptography.” States that NSA “does not support the use of QKD to protect communications in National Security Systems” and recommends PQC as “a more cost effective and easily maintained solution.”

**12.**  UK NCSC, “Quantum Networking Technologies.” Updated 2025. States: “PQC is the best mitigation to the threat to cryptography from quantum computers” and “NCSC will not support the use of QKD for government or military applications.” Notes that QKD does not provide authentication.

**13.**  RAND Corporation, “U.S.-Allied Militaries Must Prepare for the Quantum Threat to Cryptography.” June 2025. Notes that cyber/comms security agencies of UK, France, Germany, Netherlands, Sweden, and Czech Republic have all stated a clear preference for PQC over QKD. NSA prohibits QKD for NSS.

**14.**  DoW CIO. Memorandum, “Preparing for Migration to Post Quantum Cryptography,” November 18, 2025. Attachment, paragraph 2(a), prohibits DoW Components from testing, evaluating, piloting, using, or procuring QKD; QKD combined with other cryptographic key establishment; quantum communications or networking; non-local quantum randomness generation; or non-FIPS random number generation for confidentiality, authenticity, integrity, key distribution, or randomness generation, absent specific exception by the DoW CIO PQC Directorate. https://dodcio.defense.gov/Portals/0/Documents/Library/PreparingForMigrationPQC.pdf

Next: Chapter 8 — Protocol Deep Dives: TLS, IPsec, SSH, and PKI
