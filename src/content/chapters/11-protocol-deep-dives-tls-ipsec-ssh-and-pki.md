---
title: "Protocol Deep Dives: TLS, IPsec, SSH, and PKI"
displayTitle: "Chapter 8: Protocol Deep Dives: TLS, IPsec, SSH, and PKI"
section: "Chapters"
chapter: 8
order: 11
words: 6399
readingMinutes: 29
excerpt: "This is the engineering chapter. The previous seven chapters built the case for why migration matters, what algorithms replace the vulnerable ones, and how to plan the program. This chapter goes inside the protocols them"
---

This is the engineering chapter. The previous seven chapters built the case for why migration matters, what algorithms replace the vulnerable ones, and how to plan the program. This chapter goes inside the protocols themselves—byte by byte where it matters—to show exactly what changes when post-quantum cryptography enters the picture.

We’ll focus on the areas that have the greatest operational impact: the TLS certificate size problem (which may be the single biggest deployment challenge in the entire PQC transition), the DNSSEC fragmentation cascade, IPsec IKEv2 key exchange changes, SSH authentication migration, and PKI chain restructuring.

## The Certificate Size Problem: Why PQC Authentication Is Hard

Chapter 7 explained that hybrid key exchange is solved—X25519MLKEM768 adds roughly 1.1 KB to the client’s key share and the performance impact is negligible. But key exchange is only half the TLS handshake. The other half is authentication—the certificate chain the server sends to prove its identity. That’s where PQC creates a genuine engineering crisis.

### The Math: Classical vs. PQC Authentication Data

A typical TLS 1.3 handshake today transmits approximately **1,248 bytes** of authentication data: five signatures and two public keys across the certificate chain and Certificate Transparency SCTs (Signed Certificate Timestamps). This fits easily inside the initial TCP flight.<sup>1</sup>

Replacing these with ML-DSA changes the picture dramatically. Here’s the byte-by-byte accounting for a standard three-certificate chain (root CA, intermediate CA, leaf server certificate):<sup>2</sup>

| **Component** | **ECDSA P-256** | **ML-DSA-44** | **ML-DSA-65** |
| --- | --- | --- | --- |
| **Public key (leaf)** | 64 bytes | 1,312 bytes | 1,952 bytes |
| **Public key (intermediate)** | 64 bytes | 1,312 bytes | 1,952 bytes |
| **Signature × 3 (chain)** | 64 × 3 = 192 bytes | 2,420 × 3 = 7,260 bytes | 3,309 × 3 = 9,927 bytes |
| **SCT signatures × 2** | 64 × 2 = 128 bytes | 2,420 × 2 = 4,840 bytes | 3,309 × 2 = 6,618 bytes |
| **TLS handshake signature** | 64 bytes | 2,420 bytes | 3,309 bytes |
| **X.509 metadata/extensions** | ~740 bytes | ~740 bytes | ~740 bytes |
| **TOTAL AUTH DATA** | **~1,248 bytes** | **~17,884 bytes** | **~25,138 bytes** |

That’s roughly a **14× increase with ML-DSA-44 and a 20× increase with ML-DSA-65** compared to today’s classical certificates. The authentication data that currently fits in a kilobyte now consumes 17–25 KB.

![figure](/book-media/img-10.png)

*Figure 8.1 — PQC Certificate Chain Sizes vs. TCP Congestion Window Thresholds*

> **PLAIN-LANGUAGE SIDEBAR**
> Imagine shipping a letter versus shipping a small package. The letter fits in any mailbox. The package might not—you might need to ring the doorbell, wait for someone to come to the door, and hand it over personally. That extra step is what happens when PQC certificates exceed the network’s initial delivery window: the server has to pause, wait for an acknowledgment, and then continue. That pause adds a full round trip to every new connection.

### The TCP Congestion Window Problem

When a TCP connection opens, the server doesn’t flood the network with data. It starts with a limited **initial congestion window (initcwnd)**—the maximum amount of data it can send before waiting for the first acknowledgment from the client.

RFC 6928 standardized this at **IW10: 10 segments × 1,460 bytes = approximately 14.6 KB**. Many production servers, CDNs, and cloud load balancers now run IW20 (~29 KB), but IW10 remains the default on most Linux systems and many enterprise appliances.<sup>3</sup>

Here’s the collision: a classical TLS 1.3 server response (ServerHello + certificate chain + key share + Finished) typically totals 4–6 KB—well within IW10. With PQC certificates:

- **ML-DSA-44 chain (~17 KB):** Exceeds IW10. Requires an extra round trip. Fits within IW20.

- **ML-DSA-65 chain (~25 KB):** Exceeds IW10 significantly. Marginal even for IW20 when combined with application data.

- **ML-DSA-87 chain (~33 KB):** Exceeds even IW20. Multiple extra round trips on default configurations.

Cloudflare’s testing measured the real-world impact: adding approximately 9 KB to TLS handshakes caused roughly a 15% slowdown. Crossing the 10 KB threshold triggered an extra round trip that slowed handshakes by over 60%.<sup>4</sup> At scale—millions of new connections per second—that extra round trip adds measurable latency to every first page load, every API call, and every mobile app launch.

### Google’s Viability Threshold

Google’s Chrome team has published a candid assessment of what’s deployable:<sup>5</sup>

- **Adding ~2 KB to TLS handshakes:** “Very painful, but plausible.”

- **Adding ~7 KB:** “Implausible unless a cryptographically relevant quantum computer is tangibly imminent.”

- **No standardized PQC signature scheme** can stay under 7 KB for a full TLS certificate chain with Certificate Transparency. ML-DSA-65 pushes past 20 KB.

This is why Chrome is not simply dropping PQC signatures into the existing X.509 certificate infrastructure. The math doesn’t work. Instead, Google has announced a fundamentally different architecture.

## Merkle Tree Certificates: Google’s Architectural Answer

In February 2026, Google announced **Merkle Tree Certificates (MTCs)**—a new certificate format that shrinks quantum-resistant TLS authentication data from roughly 14,700 bytes down to as little as 736 bytes. That’s potentially smaller than today’s classical certificate chains.<sup>6</sup>

The core insight: instead of every certificate carrying its own large post-quantum signature, a Certification Authority signs a single cryptographic commitment—a “Tree Head”—representing many certificates organized in a Merkle tree. Browsers receive compact inclusion proofs rather than full signature chains. The heavy ML-DSA signatures are applied once per batch of certificates, not once per individual certificate.

![figure](/book-media/img-11.png)

*Figure 8.2 — Merkle Tree Certificates: Traditional PQC (~25 KB) vs. MTCs (~736 bytes)*

MTCs also integrate Certificate Transparency directly into the issuance model. Because certificates must be included in a public tree, transparency becomes inherent—eliminating the separate SCT overhead that currently adds two extra signatures to every handshake.

> **PLAIN-LANGUAGE SIDEBAR**
> Think of today’s certificate system like a notary who hand-signs every single document individually. Each signature is big and bulky, and every person who needs proof has to carry the full signed original. Merkle Tree Certificates work more like a notary who signs a single master ledger containing thousands of documents. Instead of carrying around the full signed original, you just carry a small receipt that proves your document is in the ledger. The notary’s signature is just as trustworthy—but the receipt fits in your pocket.

### The Rollout Timeline

| **Phase** | **Timeline** | **What Happens** |
| --- | --- | --- |
| **Phase 1** | 2026 (underway) | Live feasibility study with Cloudflare. ~1,000 TLS certificates enrolled. Cloudflare operates as a “mock MTCA.” Every MTC connection backed by traditional X.509 as fail-safe. |
| **Phase 2** | Q1 2027 (target) | Invite existing CT Log operators to bootstrap public MTC infrastructure. Only operators with a “usable” Chrome CT log before Feb 1, 2026 eligible. |
| **Phase 3** | Q3 2027 (target) | Launch Chrome Quantum-resistant Root Store (CQRS)—a separate trust store supporting only MTCs. Operates alongside existing Chrome Root Program. |

The standardization work is proceeding through the IETF’s newly formed **PLANTS working group**, jointly developed by Google and Cloudflare. This is the most significant structural change to the Web PKI since Certificate Transparency itself.<sup>7</sup>

> **MANDATE ALERT**
> MTCs are a Chrome/Cloudflare initiative—not yet a universal standard. Non-browser TLS clients (API consumers, IoT devices, mobile apps, server-to-server traffic) will still need to handle traditional PQC certificates for the foreseeable future. Your migration plan must account for both paths: MTCs for web-facing traffic and traditional PQC certificates for everything else.

## Mitigations for Traditional PQC Certificate Chains

While MTCs are the long-term architectural answer for web browsers, there are near-term techniques to reduce the impact of large PQC certificates in traditional deployments:

**Increase the initial congestion window.** Raising from IW10 to IW20 accommodates approximately 29 KB of server response in the first flight—enough for ML-DSA-44 and most ML-DSA-65 chains to complete in a single round trip. On Linux, this is a sysctl or ip route change.<sup>8</sup>

**TLS certificate compression.** RFC 8879 defines certificate compression for TLS 1.3. Compression can reduce on-the-wire certificate chain sizes by 40–60%, potentially keeping PQC chains within IW10. Both client and server must support it, but adoption is growing in modern browsers and web servers.<sup>9</sup>

**Intermediate certificate suppression.** If browsers pre-load known intermediate CA certificates, servers don’t need to send them during the handshake. Firefox already pre-loads over 1,400 intermediate certificates. Suppressing the intermediate saves 4–5 KB per handshake—a substantial reduction when every kilobyte matters.

**Use ML-DSA-44 where Level 3 isn’t required.** ML-DSA-44 provides NIST Security Level 2 (equivalent to AES-128) with 1,312-byte public keys and 2,420-byte signatures—roughly 35% smaller than ML-DSA-65. For web-facing TLS where certificate lifetimes are short and CNSA 2.0 compliance isn’t mandated, Level 2 may be sufficient.

**FN-DSA (FIPS 206) for compact signatures.** Falcon produces 666-byte signatures at Level 1—3.6× smaller than ML-DSA-44. A full FN-DSA chain adds only 5–8 KB. The trade-off: Falcon’s signing algorithm requires precise floating-point arithmetic that makes constant-time implementation difficult, so it’s best suited for infrequent CA-level signing rather than high-volume leaf certificate issuance.<sup>10</sup>

## DNSSEC: The UDP Fragmentation Cascade

If TLS has a certificate size problem, DNSSEC has a certificate size crisis. DNS operates primarily over UDP, where the constraints are far tighter than TCP.

The recommended maximum DNS message size to avoid IP fragmentation is **1,232 bytes** (based on IPv6’s minimum MTU of 1,280 bytes minus 48 bytes for headers). Classical DNSSEC signatures from ECDSA P-256 (64 bytes) or RSA-2048 (256 bytes) fit comfortably.<sup>11</sup>

Post-quantum signatures do not. Even the smallest NIST-standardized PQC signature—FN-DSA-512 at 666 bytes per signature—exceeds the 1,232-byte limit when a DNSSEC response contains two or three signatures (as NSEC/NSEC3 denial-of-existence responses do). ML-DSA-44 signatures at 2,420 bytes each make the problem far worse.<sup>12</sup>

When a DNSSEC response exceeds the UDP limit, one of two things happens:

- **IP fragmentation:** The response is split across multiple UDP packets. Approximately 10% of resolvers fail to reassemble IP fragments correctly, and many firewalls and middleboxes drop them entirely.

- **TCP fallback:** The server sets the truncation (TC) bit, and the resolver retries the query over TCP. This adds a three-way handshake plus at least one additional round trip—roughly doubling DNS resolution time for affected queries.

Research presented at IETF hackathons and the NIST PQC conferences has shown that even Falcon-512 can trigger TCP fallback in some DNSSEC scenarios. ML-DSA variants consistently force fallback.<sup>13</sup>

### What the Community Is Exploring

DNSSEC’s PQC migration is further behind than TLS. The IETF has established a dedicated mailing list (pq-dnssec@ietf.org) and hosted multiple PQC DNSSEC hackathons. Several approaches are under active investigation:

- **QNAME-based fragmentation (QBF):** Application-layer fragmentation that splits large responses into manageable DNS-native chunks, resolving queries in roughly half the time of standard TCP fallback.

- **SLH-DSA in Merkle Tree Ladder (MTL) mode:** Amortizes the large SLH-DSA signature across many DNS records, using compact inclusion proofs for individual queries—conceptually similar to MTCs for TLS.

- **Smaller signature algorithms:** NIST’s additional signature call includes candidates like MAYO, Hawk, and SNOVA that may offer better size profiles for DNS. These are still under evaluation.

The DNS root zone’s Key Signing Key (KSK) rollover—the most consequential DNSSEC event—is expected around 2028–2029. Whether that rollover will incorporate PQC algorithms or remain classical is an open question with significant implications for the entire DNS hierarchy.<sup>14</sup>

## IPsec IKEv2: ML-KEM Integration

Chapter 7 introduced Post-Quantum Pre-Shared Keys (PPKs) as the immediate stopgap for IPsec environments. The long-term destination is native ML-KEM integration in IKEv2, which replaces the classical Diffie-Hellman key exchange with post-quantum key encapsulation.

The CNSA 2.0 IPsec profile specifies **ML-KEM-1024** for key establishment in National Security Systems. The protocol changes are relatively contained compared to TLS: IKEv2 already supports pluggable key exchange mechanisms through its Transform Type 4 (Diffie-Hellman Group) negotiation. Replacing a classical DH group with ML-KEM-1024 follows the same negotiation flow—the primary difference is message size.<sup>15</sup>

ML-KEM-1024 produces a 1,568-byte public key and 1,568-byte ciphertext—substantially larger than the 256-byte DH group 14 or 32-byte X25519 shares used in classical IPsec. For typical site-to-site VPN tunnels with long-lived SAs, this per-SA overhead is manageable. For deployments with thousands of dynamic tunnels (large SD-WAN fabrics, hub-and-spoke architectures), the aggregate key exchange bandwidth becomes a capacity planning consideration.

Authentication in IKEv2 also requires PQC migration. When ML-DSA certificates replace RSA or ECDSA certificates for IKE authentication, the same certificate size challenges from TLS apply—amplified in mutual TLS scenarios where both sides present certificate chains.<sup>16</sup>

## SSH: The Simplest Migration Path

SSH continues to be the protocol with the smoothest PQC transition, as we previewed in Chapter 7.

**Key exchange** is already PQC-ready. OpenSSH 10.0 (April 2025) defaults to mlkem768x25519-sha256. The hybrid exchange adds roughly 2.3 KB to the key exchange—noticeable in theory, but in practice, SSH sessions are long-lived and the one-time handshake overhead is amortized over the session’s lifetime.<sup>17</sup>

**Host key authentication** is the remaining migration task. SSH host keys are currently Ed25519 or RSA. Replacing them with ML-DSA host keys means larger SSH server identification payloads, but SSH doesn’t have TLS’s certificate chain overhead—there’s no intermediate CA hierarchy. A single ML-DSA-65 host key adds approximately 5.3 KB (1,952-byte public key + 3,309-byte signature), which is manageable.

**User authentication** via PQC keys follows the same pattern. If your environment uses SSH certificates (rather than bare public keys), the certificate sizes will mirror the ML-DSA figures above—but again, without the multi-level chain amplification that makes TLS certificates so challenging.

## Secure Email: S/MIME and PGP

For organizations that handle classified or sensitive communications—particularly in DoD, intelligence, and federal civilian agencies—S/MIME is the primary mechanism for signed and encrypted email. PGP (and its open standard, OpenPGP) serves a similar role in some environments.

Both protocols face the same PQC challenges as TLS and IPsec: key exchange algorithms (RSA, ECDH) must be replaced with ML-KEM, and signature algorithms (RSA, ECDSA) must be replaced with ML-DSA. The IETF has active drafts for both:

- **S/MIME:** The IETF LAMPS working group is developing composite certificate formats that bundle classical and PQC algorithms for Cryptographic Message Syntax (CMS). Draft standards for ML-KEM and ML-DSA in S/MIME are in progress.

- **OpenPGP:** RFC 9580 (the updated OpenPGP specification, published July 2024) includes provisions for PQC algorithm identifiers. The crypto-refresh working group has been preparing the groundwork for ML-KEM and ML-DSA integration.

> **PLAIN-LANGUAGE SIDEBAR**
> The certificate size challenges from TLS apply directly to encrypted email. Every S/MIME signed message carries the sender’s certificate chain. With PQC certificates, each signed email becomes significantly larger. For organizations processing millions of signed messages daily, the storage and bandwidth implications are material—and email archival systems designed for today’s certificate sizes will need capacity planning updates.

## PKI Chain Migration: The Long Pole in the Tent

The Public Key Infrastructure underpins everything above—TLS, IPsec, SSH certificates, code signing, email (S/MIME), document signing, and device identity. Migrating PKI is the deepest, most cross-cutting element of the PQC transition.

### Phased PKI Migration

The practical migration sequence, informed by the NIST NCCoE’s guidance and the CA/Browser Forum’s evolving requirements:<sup>18</sup>

- **Phase 1 — Root and Intermediate CAs:** Issue new root certificates with PQC algorithms (ML-DSA-87 for roots needing CNSA 2.0, ML-DSA-65 for general purpose). Distribute these through trust store updates. This is the slowest step—root distribution takes years.

- **Phase 2 — Leaf certificates:** Begin issuing leaf server certificates with PQC algorithms. Initially, issue hybrid certificates (dual ECDSA + ML-DSA) for backward compatibility. Transition to pure PQC as client support matures.

- **Phase 3 — Client certificates:** Migrate mutual TLS (mTLS) client certificates to PQC. This is especially impactful in Zero Trust environments where every client connection authenticates with a certificate.

- **Phase 4 — Non-web PKI:** Code signing, S/MIME email certificates, document signing, device identity certificates. Each has its own ecosystem, tooling, and migration challenges.

### The PQC Root Key Ceremony

Generating a new PQC root private key is not a routine task. Public and private CAs have operated under formal key ceremony practices for decades—tied to WebTrust for Certification Authorities audit requirements, CA/Browser Forum Baseline Requirements, and NIST SP 800-57 Part 2 key management guidance—to ensure that the act of creating the root key pair is witnessed, scripted, and auditable. PQC migration does not change this discipline; it extends it. The same ceremonial controls apply, with a few PQC-specific additions around algorithm selection, HSM firmware verification, and—for stateful hash-based signatures—state management.<sup>19</sup>

The section that follows describes the ceremony controls that organizations issuing PQC root or intermediate CA keys should plan for. It is not a replacement for your CA’s Certificate Policy (CP) and Certification Practice Statement (CPS); those documents describe what your specific organization commits to. The following checklist is the common baseline shared across public CAs, government PKIs, and large private CAs.

### Pre-Ceremony Checklist

The most common reason key ceremonies fail audit is inadequate preparation. Before convening witnesses and unsealing the HSM:

- **Algorithm and parameter selection:** Confirm the specific PQC algorithm, parameter set, and hash function (e.g., ML-DSA-87 for CNSA 2.0 roots, ML-DSA-65 for general purpose, LMS or XMSS for code signing). Document the rationale in the ceremony script.

- **HSM firmware verification:** Verify the exact HSM firmware version supports the chosen algorithm and is at a FIPS 140-3 validation state acceptable to your audit scheme. Record the firmware hash or version string in the ceremony log.

- **CP/CPS alignment:** Ensure the ceremony script implements what your CP/CPS describes. Discrepancies between script and published CPS are audit findings.

- **Physical and logical access:** Reserve the ceremony room. Verify smart-card / M-of-N token inventory. Confirm tamper-evident bags, seal numbers, and evidence-of-integrity mechanisms are on hand.

- **Witness identification:** Designate and identify all ceremony participants and their roles (see below). All participants should have completed background checks consistent with your CP/CPS.

- **Ceremony script review:** Walk the script end-to-end with all roles present at least 24 hours in advance. The live ceremony is not the time to discover missing steps.

### Multi-Person Control

Root key operations require multi-person control. Two related but distinct disciplines apply:

- **Split knowledge:** No single person has enough information to operate the root key alone. In practice, this means M-of-N smart-card quorums (commonly 3-of-5 or 5-of-7 for tier-1 public roots) holding HSM partition authentication material.

- **Dual control:** Every operational step on the root HSM requires at least two people present, each with independent authentication. Neither can proceed without the other.

PQC does not change these controls, but it does change what the quorum is authorizing. A ceremony to generate ML-DSA-87 keys produces fundamentally different artifacts than one generating RSA-4096: key sizes differ (ML-DSA-87 public keys are 2,592 bytes versus 512 bytes for RSA-4096), signature sizes differ (ML-DSA-87 signatures are 4,627 bytes versus 512 bytes), and—for stateful hash-based algorithms—the quorum is authorizing the creation of a state-managed key, not a stateless one. Witnesses should understand what they are attesting to.

### Script-Driven Operations

Every action during the ceremony follows a pre-approved, reviewed, and signed-off script. The script specifies exact commands, expected outputs, and decision points. Any deviation triggers a documented exception process, and material deviations halt the ceremony. Three practical requirements:

- **Command-level specificity:** The script captures the exact HSM command syntax (keygen algorithm parameters, key label, quorum requirements). Generic instructions like “generate the root key” are insufficient for audit.

- **Expected-output capture:** For each command, the script includes the expected output or success criterion. The ceremony scribe compares actual output against expected and flags discrepancies in real time.

- **Version control:** The script is a versioned artifact. The exact version number used during the ceremony is recorded in the ceremony log and retained with the audit evidence.

### Tamper-Evident Logging

Every ceremony produces a contemporaneous log—the written record that the auditor will review. The log should capture:

- **Participants and roles:** Names, roles, and ID verification method for every person in the room.

- **Timestamps:** Start and end time for each script step. Use wall-clock time from a trusted source.

- **HSM artifacts:** Key label, algorithm parameters, public key fingerprint (post-generation), firmware version, and any error messages.

- **Physical evidence:** Tamper-evident bag numbers, seal numbers, smart-card identifiers, and chain-of-custody transfers.

- **Signatures:** All participants sign each page of the log at ceremony close. Electronic signatures are acceptable where permitted by CP/CPS.

Video recording of the ceremony is common for public CAs and is usually required by WebTrust for tier-1 root ceremonies. The recording becomes part of the audit evidence.

### Witness Roles

A formal ceremony distinguishes multiple roles. The minimum set for most PKI hierarchies:

- **Ceremony Administrator (CA Officer):** Executes the script. Authenticates to the HSM. Operates the ceremony laptop or console.

- **Internal Witness:** Observes every step. Is not a smart-card holder. Independently verifies script adherence.

- **External Witness / Auditor:** For publicly trusted CAs under WebTrust, a Qualified Auditor attends and issues an opinion that the ceremony was conducted per the CA’s stated procedure. For private PKIs, this role may be an internal audit function or a trusted third party.

- **Scribe:** Maintains the contemporaneous log. Should not be the same person as the Ceremony Administrator.

- **Smart-card / Quorum Holders:** M-of-N token holders required to authenticate key operations. Physically present and identified in the log.

- **Security Officer:** Controls physical access to the ceremony room. Maintains custody of tamper-evident materials before and after the ceremony.

### Post-Ceremony Verification

The ceremony is not complete when the key is generated. Post-ceremony verification confirms that the key operates as intended and that all artifacts are sealed and stored correctly:

- **Public key fingerprint verification:** Compute the fingerprint of the newly generated public key using two independent tools. Compare against the fingerprint captured in the log. Discrepancy is a ceremony failure requiring reconvening.

- **Test signature and verification:** Sign a known test vector with the new root key. Verify the signature with the extracted public key. Record both the test vector and the verification result in the log.

- **Stateful hash-based signature state initialization:** If using LMS or XMSS for code signing, verify that the stateful signing counter is correctly initialized, that state backup and replication mechanisms are tested, and that the HSM enforces single-use of each signature state. Reusing an LMS/XMSS state is a catastrophic failure mode.

- **Artifact sealing:** Place all removable materials (smart cards, backup HSM cartridges, printed logs) into tamper-evident bags. Record seal numbers in the log. Transfer to secure storage under dual control.

- **Ceremony log finalization:** Close and sign the ceremony log. Distribute copies per CP/CPS retention policy. The log is the durable record; the ceremony cannot be reconstructed from memory.

- **Audit package assembly:** Assemble script version, ceremony log, video (if applicable), HSM firmware verification evidence, and public key fingerprint for delivery to the Qualified Auditor.

PQC ceremonies differ in detail from classical ceremonies—larger keys, different HSM command syntax, stateful signature state management, new algorithm parameter sets to validate. They do not differ in discipline. The same multi-person control, the same scripted execution, the same tamper-evident logging, the same witness roles apply. Organizations that have run classical root ceremonies successfully have most of the operational muscle they need; what changes is the content of the ceremony, not its structure.

### The mTLS Amplification Effect

Most TLS performance studies focus on server authentication—the server sends its certificate chain to the client. In mTLS environments (common in Zero Trust, service mesh, and API gateway architectures), the client also sends a certificate chain. With PQC, the handshake is doubly impacted: a server chain of ~17 KB plus a client chain of ~17 KB means the handshake could exceed 34 KB of authentication data—well beyond IW20.<sup>20</sup>

For organizations running mTLS at scale (every microservice authenticating to every other microservice), this is a critical capacity planning consideration that most PQC migration guides overlook.

### Shorter Certificate Lifetimes Compound the Problem

The CA/Browser Forum’s Ballot SC-081v3 sets a schedule that shrinks publicly trusted TLS certificate validity: 200 days starting March 2026, 100 days by March 2027, and 47 days by March 2029.<sup>21</sup> Shorter lifetimes mean more frequent issuance, which means paying the PQC overhead tax more often. The combination of larger certificates and higher issuance velocity is what makes a simple drop-in replacement unsustainable at internet scale—and why architectural solutions like MTCs are necessary.

> **F5 PERSPECTIVE**
> **BIG-IP Capacity Planning for PQC Certificates**
> BIG-IP devices that terminate TLS must account for the larger PQC certificate chains in their memory and throughput planning. Key considerations:
> **Memory per connection:** Each active TLS session stores the peer’s certificate chain in memory during the handshake. With ML-DSA-65 certificates, this increases from roughly 4 KB to 20+ KB per session. At 100,000 concurrent connections, that’s an additional 1.5+ GB of memory dedicated to certificate storage alone.
> **Bandwidth:** A BIG-IP serving 10 million TLS connections per day with ML-DSA-65 certificates transmits approximately 250 GB more certificate data daily than with classical certs. For most enterprise deployments, this is well within infrastructure capacity—but it’s a line item in capacity planning, not invisible.
> **Initial congestion window:** BIG-IP supports configurable TCP profiles, including the initial congestion window size. Increasing initcwnd from 10 to 20 on internet-facing virtual servers may be the single highest-impact configuration change for PQC readiness—a one-line profile modification that eliminates the extra round trip for most PQC certificate chains.
> **TLS certificate compression:** As BIG-IP adds support for RFC 8879 TLS certificate compression, enabling it alongside PQC certificates will be a critical optimization. Monitor F5’s release notes for availability.

## Zero Trust and IAM in a Post-Quantum World

Zero Trust Architecture is predicated on a simple premise: verify every request, and let no network location confer implicit trust. NIST SP 800-207 codifies this premise through seven tenets, chief among them that all communication is secured regardless of network location, and that resource authentication and authorization are dynamic and strictly enforced. CISA’s Zero Trust Maturity Model v2.0 and OMB M-22-09 have since made Zero Trust the expected operating model for federal agencies. The premise is sound. The challenge for a PQC migration is that every Zero Trust control depends on cryptographic identity—certificates, signatures, tokens, attestations—and every one of those controls inherits the quantum-vulnerability of its underlying algorithms.<sup>22</sup>

Zero Trust does not introduce new cryptographic problems. It amplifies the ones already described in this chapter. Where a perimeter model authenticates at the edge and trusts the interior, Zero Trust authenticates at every hop. Every service-to-service call is mTLS. Every API request is signed. Every device presents a certificate. Every user session is re-evaluated. The cryptographic surface area is larger by one or two orders of magnitude, which means the PQC migration cost is larger by the same factor.

### Where the PQC Pressure Lands

- **Workload-to-workload mTLS.** Service mesh architectures (Istio, Linkerd, Consul Connect) and SPIFFE-based workload identity frameworks issue short-lived certificates to every workload. With PQC, each handshake pays the certificate-size cost (Chapter 8 certificate size section) on both sides. The mTLS amplification effect is not a corner case in Zero Trust; it is the common case.

- **Signed tokens (OIDC, OAuth 2.0, SAML).** Identity providers sign access tokens, ID tokens, and SAML assertions. Those signatures must transition to ML-DSA for long-term verifiability, especially where tokens are archived or replayed against audit logs. JWTs with RSA/ECDSA signatures remain forgeable to an adversary with a CRQC, even after the session has ended.

- **Identity provider (IdP) signing keys.** An IdP’s signing key is a single point of compromise with enormous cryptographic blast radius: compromising it forges every identity assertion the IdP issues. IdP root keys are prime candidates for early PQC migration, and their migration follows the same ceremony discipline described earlier in this chapter.

- **ZTNA brokers and the cryptographic proxy layer.** ZTNA platforms terminate TLS at a broker that evaluates policy before connecting the client to a resource. This is the cryptographic proxy layer pattern (Chapter 7). The broker is the right place to enable hybrid PQC first: one upgrade point protects many downstream resources. F5 BIG-IP Zero Trust Access, added in v21.1, is one commercial example of this pattern.

- **Device and workload attestation.** Device posture checks, TPM attestations, and workload identity proofs all produce signed claims that relying parties verify. Those signatures must become PQC before the signed-claim lifetime exceeds the attacker’s time-to-CRQC. For devices with multi-year deployment lifecycles (industrial control, medical, embedded), this is already urgent.

Zero Trust does not change the PQC migration work; it changes the scope. An organization that has built a Zero Trust Architecture has already committed to strong cryptographic identity everywhere, which means that same organization is committed to replacing every instance of quantum-vulnerable cryptography in that identity fabric. The good news: the migration maps cleanly onto existing Zero Trust investments. Policy Decision Points and Policy Enforcement Points are natural upgrade targets; cryptographic proxy layers consolidate the upgrade into fewer places; and workload identity frameworks like SPIFFE were designed with crypto-agility in mind. The Zero Trust roadmap and the PQC roadmap should not be two programs. They should be one.

## Protocol Migration Summary

| **Protocol** | **Key Exchange Status** | **Authentication Status** | **Biggest Challenge** |
| --- | --- | --- | --- |
| **TLS 1.3** | Solved — X25519MLKEM768 deployed at scale | In progress — MTCs in Phase 1 testing | Certificate size exceeds TCP initcwnd; MTCs needed for web scale |
| **IPsec** | PPK stopgap deployed; native ML-KEM in CNSA 2.0 profile | ML-DSA certs for IKE auth; mTLS amplification | Large-scale SD-WAN/hub-spoke key exchange bandwidth |
| **SSH** | Solved — mlkem768x25519 default in OpenSSH 10.0 | Host/user key migration to ML-DSA pending | Minimal — no cert chain overhead; single key per host |
| **DNSSEC** | N/A (signatures only) | Research phase — MTL mode, QBF, new algorithms | UDP 1,232-byte limit; even Falcon-512 triggers fallback |
| **PKI** | N/A | Root/intermediate CA migration beginning | Root trust store distribution takes years; mTLS doubles overhead |

## What’s Next

You now understand what changes at the protocol level and where the pain points are. Chapter 9 shifts to the operational reality: once PQC is deployed, how do you monitor it, manage certificate rotation at scale, handle performance regressions, train your team, and ensure long-lived signed artifacts remain trustworthy in a post-quantum world?

## Notes

The following sources support specific claims made in Chapter 8. Full bibliographic entries appear in the Bibliography.

**1.**  NIST PQC Conference presentation, Andrew Regenscheid & Bill Newhouse (December 2024). TLS WebPKI authentication data breakdown: server certificate (1 public key + 1 signature + 2 SCT signatures), intermediate CA certificate (1 public key + 1 signature), TLS handshake (1 signature). Classical total: ~1,248 bytes. ML-DSA-44 total: ~14,724 bytes.

**2.**  NIST FIPS 204 (ML-DSA) specifies signature and public key sizes. ML-DSA-44: 1,312-byte public key, 2,420-byte signature. ML-DSA-65: 1,952-byte public key, 3,309-byte signature. ML-DSA-87: 2,592-byte public key, 4,627-byte signature. X.509 metadata overhead varies by certificate; ~740 bytes is a representative figure including extensions.

**3.**  RFC 6928, “Increasing TCP’s Initial Window,” standardized IW10 (10 segments). Many production systems, CDNs, and cloud providers now use IW20 or higher. Default Linux initcwnd remains 10 as of kernel 6.x.

**4.**  Cloudflare infrastructure testing and NIST 5th PQC Standardization Conference paper, “The Impact of Data-Heavy Post-Quantum TLS 1.3.” Testing showed ~15% slowdown at +9 KB, 60%+ slowdown when crossing the 10 KB threshold due to extra round trip from congestion control interaction.

**5.**  Google Chrome team analysis cited in multiple sources including the MTC announcement (February 2026). Google’s threshold: +2 KB is “very painful but plausible”; +7 KB is “implausible unless a CRQC is tangibly imminent.” No standardized PQC signature scheme meets the 7 KB threshold for a full chain with CT.

**6.**  Google Security Blog, “Cultivating a Robust and Efficient Quantum-Safe HTTPS,” February 2026. Merkle Tree Certificates (MTCs) reduce authentication data from ~14,700 bytes to as low as 736 bytes. Developed jointly with Cloudflare; standardization through IETF PLANTS working group.

**7.**  IETF PLANTS (Post-quantum Lightweight Authentication for Network TLS Security) working group formed to standardize MTCs. Phase 1 testing underway with ~1,000 certificates enrolled (Cloudflare as mock MTCA). Phase 2 targets Q1 2027; Phase 3 (Chrome Quantum-resistant Root Store) targets Q3 2027.

**8.**  Increasing TCP initcwnd from IW10 to IW20 accommodates ~29 KB in the first server flight. On Linux: ip route change default via <gateway> initcwnd 20 initrwnd 20. This is a well-understood optimization already deployed by many CDNs and cloud providers.

**9.**  RFC 8879, “TLS Certificate Compression.” Defines zlib, Brotli, and Zstandard compression for TLS 1.3 certificate messages. Can reduce PQC certificate chain sizes by 40–60%. Requires both client and server support.

**10.**  NIST FIPS 206 (draft), FN-DSA (Falcon). FN-DSA-512 produces 666-byte signatures—3.6× smaller than ML-DSA-44’s 2,420 bytes. Full FN-DSA chain: ~5–8 KB. Cloudflare analysis notes Falcon’s floating-point signing makes constant-time implementation extremely difficult; better suited for CA-level signing than high-volume leaf issuance.

**11.**  IETF DNS Flag Day 2020 recommendation: EDNS buffer size of 1,232 bytes avoids fragmentation on nearly all current networks. Based on IPv6 minimum MTU of 1,280 bytes minus 48 bytes for IPv6 and UDP headers.

**12.**  IETF draft-fregly-research-agenda-for-pqc-dnssec-02. Even FN-DSA-512 (666-byte signatures) exceeds the 1,232-byte limit with two or three signatures in NSEC/NSEC3 responses. ML-DSA signatures (2,420–4,627 bytes) make UDP transport of DNSSEC responses effectively impossible.

**13.**  NIST 6th PQC Standardization Conference, VeriSign/NIST presentation: “Post-Quantum Diversity for DNSSEC: Routine Performance, Resilient Fallback.” PQC DNSSEC hackathon at IETF 123 (July 2025) tested implementations in BIND, NSD, and CoreDNS with ML-DSA, FN-DSA, SLH-DSA, MAYO, SQIsign, Hawk, and SNOVA.

**14.**  DNS root zone KSK rollover expected ~2028–2029 per VeriSign/NIST presentations. Whether PQC algorithms will be incorporated into root zone DNSSEC operations is an open question under active discussion at IETF and ICANN.

**15.**  NSA, draft-guthrie-cnsa2-ipsec-profile: CNSA Suite 2.0 Profile for IPsec. Specifies ML-KEM-1024 for key establishment. ML-KEM-1024: 1,568-byte public key, 1,568-byte ciphertext.

**16.**  NIST PQC Conference presentation on mTLS impact: “The Impact of ML-KEM and ML-DSA on mTLS Connection Time-To-Last-Byte.” In mTLS (mutual TLS), both client and server send certificate chains, doubling the authentication data overhead in both directions.

**17.**  OpenSSH 10.0 Release Notes (April 2025). Default key exchange: mlkem768x25519-sha256. Adds ~2.3 KB to key exchange compared to classical X25519.

**18.**  NIST NCCoE SP 1800-38 (Preliminary Draft): Migration to Post-Quantum Cryptography. PKI migration guidance covers root CA establishment, intermediate CA issuance, leaf certificate transition, and non-web PKI considerations.

**19.**  PQC root key ceremony controls draw from three canonical sources: NIST SP 800-57 Part 2 Rev 1 (Recommendation for Key Management: Best Practices for Key Management Organizations, May 2019); WebTrust Principles and Criteria for Certification Authorities v2.2.2 (CPA Canada / AICPA); and the CA/Browser Forum Baseline Requirements, Section 8 (Audit), which requires that a Qualified Auditor opine on the CA’s key ceremony during key and certificate generation and on the controls used to ensure the integrity and confidentiality of the key pair. Publicly trusted CAs are subject to annual WebTrust audit; private and government CAs typically follow the same practices through CP/CPS commitments.

**20.**  mTLS amplification: a server chain (~17 KB with ML-DSA-44) plus client chain (~17 KB) totals ~34 KB of authentication data in a single handshake—exceeding IW20 (~29 KB). This is especially relevant in Zero Trust architectures and service mesh deployments.

**21.**  CA/Browser Forum Ballot SC-081v3. Publicly trusted TLS certificate maximum validity: 398 days (current), 200 days (March 2026), 100 days (March 2027), 47 days (March 2029). Domain validation data reuse tightens to 10 days by end of timeline.

**22.**  Zero Trust foundational references: NIST SP 800-207, “Zero Trust Architecture” (August 2020), defines the seven tenets and the Policy Engine / Policy Administrator / Policy Enforcement Point component model. NIST SP 800-207A, “A Zero Trust Architecture Model for Access Control in Cloud-Native Applications in Multi-Cloud Environments” (September 2023), extends the model for workload-identity patterns including SPIFFE. CISA Zero Trust Maturity Model v2.0 (April 2023) organizes maturity across five pillars (Identity, Devices, Networks, Applications & Workloads, Data). OMB Memorandum M-22-09 (January 2022) establishes the federal Zero Trust strategy for executive branch agencies.

Next: Chapter 9 — Day-2 Operations: Monitoring, Rotation, and Long-Term Assurance
