---
title: "Day-2 Operations: Monitoring, Rotation, and Long-Term Assurance"
displayTitle: "Chapter 9: Day-2 Operations: Monitoring, Rotation, and Long-Term Assurance"
section: "Chapters"
chapter: 9
order: 12
words: 3045
readingMinutes: 14
excerpt: "Deploying post-quantum cryptography is a milestone, not a finish line. Once PQC is live in your environment—hybrid TLS on the edge, updated SSH key exchanges, new certificate chains in the pipeline—a new set of operation"
---

Deploying post-quantum cryptography is a milestone, not a finish line. Once PQC is live in your environment—hybrid TLS on the edge, updated SSH key exchanges, new certificate chains in the pipeline—a new set of operational challenges begins. This chapter covers what happens after the migration: how you monitor PQC in production, manage certificates that are 10× larger, protect long-lived signed artifacts, keep your vendor ecosystem aligned, and build the institutional knowledge to sustain the program.

## Protecting Long-Lived Signed Artifacts

Most of the PQC migration discussion focuses on data in transit—TLS sessions, VPN tunnels, SSH connections. But some of the most consequential cryptographic artifacts in your environment aren’t protecting live traffic. They’re protecting evidence: signed firmware images, software bills of materials (SBOMs), audit logs, legal contracts, code signing certificates, and regulatory filings that must remain verifiable for years or decades.

These artifacts face a threat that live TLS connections do not: **harvest-now, forge-later**. An adversary who captures a classically signed firmware image today could, with a future quantum computer, forge an altered version with a valid signature—retroactively compromising the trust chain. This isn’t theoretical; it’s the signature-side analog of the HNDL attack we described in Chapter 1.<sup>1</sup>

### What Needs Protection

| **Artifact Type** | **Typical Retention** | **Quantum Risk** |
| --- | --- | --- |
| **Firmware images** | 10–20+ years (embedded/OT) | Forged firmware accepted as authentic; supply chain compromise |
| **Code signing certificates** | 5–10 years | Malicious code signed with forged certificate trusted by endpoints |
| **SBOMs / build manifests** | Lifetime of deployed software | Tampered SBOM hides vulnerable or malicious components |
| **Audit logs / compliance records** | 7–25 years (regulatory) | Forged or altered audit trail; repudiation of signed actions |
| **Legal contracts / e-signatures** | Decades | Signatory repudiates contract; forged amendments accepted as valid |
| **Timestamping authority records** | Decades | Forged timestamps alter the provable sequence of events |

### Migration Patterns for Legacy Evidence

Researchers have formalized three practical patterns for protecting existing signed artifacts:<sup>2</sup>

**Pattern 1: Hybrid signatures for new artifacts.** Starting now, sign all new firmware, SBOMs, audit records, and code releases with both a classical signature and a PQC signature (ML-DSA). If the classical signature is later broken, the PQC signature preserves integrity. This is the CNSA 2.0 approach for software and firmware signing, with a “prefer PQC by 2025” target.<sup>3</sup>

**Pattern 2: Re-signing legacy artifacts.** For existing signed artifacts that must remain verifiable beyond Q-Day, re-sign them with a PQC key inside a trusted environment (HSM or TEE). This retroactively extends the evidentiary lifetime of legacy records. The trust assumption: the original artifacts were unmodified at the time of re-signing.

**Pattern 3: Merkle root anchoring.** For large batches of legacy records, compute a Merkle tree over the batch and sign only the root with a PQC signature. Individual records are verified via compact inclusion proofs against the signed root. This amortizes the cost of PQC signatures across thousands of records—a practical approach for audit log archives.

> **PLAIN-LANGUAGE SIDEBAR**
> Think of re-signing legacy artifacts like a notary re-stamping old documents with a new, tamper-proof seal. The original signatures are still there—they prove the document was authentic when it was first signed. The new PQC seal proves it hasn’t been altered since, even if someone eventually finds a way to forge the original stamp.

## Certificate Lifecycle Management at Scale

PQC certificates are larger, expire more frequently (per the CA/Browser Forum’s tightening validity schedule), and involve new algorithms that your existing tooling may not fully support. The certificate lifecycle—issuance, distribution, installation, monitoring, renewal, and revocation—becomes more demanding across every step.

### Key Operational Changes

**Storage and memory.** Certificate stores on endpoints, load balancers, and HSMs will consume significantly more space. A PQC certificate chain that once fit in 3–4 KB now requires 17–25 KB. At scale, this affects memory allocation per TLS session and certificate cache sizing.

**Renewal velocity.** With publicly trusted certificates shrinking to 47-day maximum validity by 2029, automated certificate management becomes non-optional. Manual renewal processes will collapse under the volume.<sup>4</sup> The tooling landscape has traditionally concentrated in three places: standalone ACME clients (certbot, acme.sh), Kubernetes controllers (cert-manager), and enterprise CLM platforms (Venafi, Keyfactor, AppViewX). A newer pattern worth tracking is native ACME support inside the TLS enforcement point itself. Apache HTTP Server has supported it since 2.4.30; Caddy and Traefik treat automatic certificate management as default behavior; NGINX released the ngx_http_acme_module in August 2025.<sup>5</sup> This shift matters because it removes a class of external orchestration: the server or reverse proxy that terminates TLS also handles its own certificate renewal, with no intermediate automation tier to maintain. Expect native ACME support to expand across enterprise ADC platforms as 47-day validity approaches.

**Revocation checking.** OCSP responses and CRLs that carry PQC signatures will also be larger. Stapling OCSP responses (where the server pre-fetches and attaches the OCSP response to the TLS handshake) becomes even more important to avoid per-client OCSP lookup overhead.

**HSM compatibility.** The five HSM readiness questions from Chapter 6 remain critical in Day-2 operations. Ongoing firmware updates from HSM vendors (Thales, Entrust, Marvell/Cavium) will add PQC algorithm support incrementally. Track vendor release notes and plan HSM firmware upgrades into your maintenance windows.<sup>6</sup>

> **MANDATE ALERT**
> Microsoft announced general availability of PQC APIs (ML-KEM and ML-DSA) in Windows Server 2025 and Windows 11 (24H2/25H2) via CNG, with Active Directory Certificate Services (ADCS) PQC support targeted for early 2026. If you run a Microsoft PKI, this is your on-ramp for issuing PQC certificates from your enterprise CA.
> AWS KMS and Google Cloud KMS both support ML-DSA for digital signatures. These services can sign firmware, SBOMs, and other artifacts with PQC today—no HSM upgrade required.

## Performance Monitoring and Regression Detection

PQC introduces measurable performance changes. In most cases, they’re small enough to be invisible to end users (1–2 ms on a TLS handshake). But in edge cases—high-latency networks, mobile connections, mTLS-heavy service meshes, or misconfigured initial congestion windows—the impact can compound.

### What to Monitor

| **Metric** | **What to Watch For** | **Action Threshold** |
| --- | --- | --- |
| **TLS handshake latency (p50/p95/p99)** | Increase after enabling PQC certificates or hybrid key exchange | p95 increase >50 ms suggests congestion window or cert size issue |
| **TLS handshake failure rate** | Middlebox or client incompatibility with larger handshakes | Any increase >0.1% warrants investigation of specific client/path |
| **Certificate chain size on the wire** | Unexpected growth (e.g., dual-signed hybrid certs larger than expected) | Chains exceeding 20 KB on IW10 systems need initcwnd tuning |
| **SSH key exchange duration** | Baseline change after mlkem768x25519 becomes default | Typically <5 ms increase; larger suggests network or library issue |
| **VPN tunnel establishment time** | IKEv2 rekeying with ML-KEM or PPK overhead | Monitor per-tunnel and aggregate; flag rekeying storms |
| **Memory consumption per connection** | Larger cert chains stored in session memory | Correlate with connection count; plan for 5–10× cert memory growth |

The key principle: **baseline before you migrate**. Capture your current TLS handshake latency distribution, failure rates, and memory profiles before enabling PQC. Without a clean baseline, you can’t distinguish PQC-induced regressions from unrelated changes.<sup>7</sup>

## Vendor and Supply Chain Readiness

Your PQC migration is only as strong as your weakest vendor. If a third-party SaaS provider, payment processor, or API gateway still uses RSA-2048, your data transiting that interface remains quantum-vulnerable regardless of your internal readiness.<sup>8</sup>

### The Vendor PQC Readiness Conversation

For each critical vendor and supplier, your procurement and security teams should be asking:

- **Algorithm support:** Do your products support ML-KEM and ML-DSA? Which versions? Is the support FIPS-validated or pending validation?

- **Timeline:** What is your published PQC migration roadmap? When will PQC be available in production releases?

- **Hybrid support:** Can your product operate in hybrid mode during the transition, or is it PQC-only?

- **Crypto-agility:** If a PQC algorithm is broken or deprecated, how quickly can you swap to an alternative? Is algorithm selection configurable by the customer, or does it require a vendor release?

- **CBOM disclosure:** Can you provide a Cryptographic Bill of Materials documenting which algorithms, key sizes, and protocols your product uses?

The USDA has already embedded explicit PQC procurement language in its acquisition regulations—requiring that products in CISA-listed categories support PQC.<sup>9</sup> Other federal agencies will follow. For vendors selling to the public sector, PQC readiness is quickly becoming a contract requirement, not a differentiator.

## Building Institutional Knowledge

PQC is not a one-time project that can be handed to a contractor and forgotten. It’s a permanent shift in the cryptographic foundation of your infrastructure. The people who maintain your systems need to understand what changed and why.

### Who Needs Training and What They Need to Know

| **Role** | **Core Knowledge** | **Depth** |
| --- | --- | --- |
| **Network / infrastructure engineers** | Hybrid TLS configuration, initcwnd tuning, cert compression, IPsec PPK setup, SSH key migration | Hands-on configuration and troubleshooting |
| **PKI / identity team** | PQC certificate issuance, CA hierarchy changes, HSM firmware updates, ACME automation, hybrid certificate formats | Deep operational expertise |
| **Security operations (SOC)** | Recognizing PQC-related handshake failures, cipher suite anomalies, and algorithm downgrade attacks | Detection and triage |
| **Application developers** | Library updates (OpenSSL 3.5+, BoringSSL, Windows CNG), API changes for PQC key generation, and testing strategies | Integration and testing |
| **Leadership / CISO** | Risk posture, compliance timeline, budget implications, vendor readiness assessment | Strategic awareness and decision authority |

The CCOE (Cryptographic Center of Excellence) model from Chapter 6 provides the organizational structure; training fills it with capability. Consider tabletop exercises that simulate a PQC deployment failure—a certificate chain that breaks a critical application, a middlebox that drops hybrid handshakes, or an HSM that doesn’t support ML-DSA yet. These exercises build muscle memory before the pressure of production.

## The Crypto-Agility Feedback Loop

Chapter 6 introduced crypto-agility as an architectural principle. In Day-2 operations, crypto-agility becomes a continuous process: a feedback loop that keeps your cryptographic posture aligned with evolving standards, emerging threats, and real-world performance data.

The loop has four steps:

![figure](/book-media/img-12.png)

*Figure 9.1 — The Crypto-Agility Feedback Loop*

**1. Monitor.** Continuously track which algorithms, key sizes, and protocols are in use across your environment. Your CBOM from Chapter 5 is a living document, not a one-time deliverable. Update it as systems change.<sup>10</sup>

**2. Evaluate.** Watch for NIST advisories, IETF draft updates, and cryptanalytic research. If a new attack weakens ML-KEM or ML-DSA, your team needs to assess the impact within days, not months. Subscribe to the NIST PQC mailing list, IETF TLS working group updates, and your vendors’ security advisories.

**3. Adapt.** When a change is needed—a new algorithm, a deprecated parameter, a configuration update—your crypto-agile architecture should allow it through policy and configuration changes rather than full application redeployments. This is the payoff for the modular design principles established in Chapter 6.

**4. Verify.** After any change, validate that the new configuration is operating correctly: handshakes complete, performance is within bounds, interoperability is maintained. Then update your CBOM and close the loop.

> **PLAIN-LANGUAGE SIDEBAR**
> Crypto-agility in practice is less like upgrading a jet engine mid-flight and more like rotating tires on a car. If you designed the system with standard lug nuts (modular interfaces), the swap is straightforward maintenance. If every tire is welded on (hard-coded algorithms), every change is a crisis. The architectural decisions you make during migration determine which experience your team has for the next decade.
> **F5 PERSPECTIVE**
> **Day-2 PQC Operations with BIG-IP**
> BIG-IP’s role in Day-2 PQC operations extends naturally from its position as the TLS termination and visibility point:
> **Observability:** BIG-IP telemetry (via Application Study Tool, F5 Insight, or iRules logging) can surface per-VIP cipher suite negotiation, handshake latency distributions, and certificate chain sizes. This data feeds directly into the monitoring table above—your PQC performance baseline lives on BIG-IP.
> **Algorithm policy enforcement:** SSL/TLS profiles on BIG-IP control which cipher suites and key exchange groups are offered to clients. Updating the allowed set to include (or require) X25519MLKEM768 is a profile change, not a code deployment. When the time comes to drop classical-only key exchange, it’s the same profile change in reverse.
> **Certificate rotation:** As PQC certificates enter production, BIG-IP’s certificate management capabilities handle the larger chain sizes. For automated rotation today, F5 publishes Kojot ACME, an open-source ACMEv2 client utility that runs on BIG-IP and supports HTTP-01 and DNS-01 validation, wildcard certificates, HSM/FIPS key preservation, HA deployments, and OCSP monitoring. On the NGINX side of F5’s portfolio, the ngx_http_acme_module ships natively in NGINX Open Source and NGINX Plus, enabling certificate issuance and renewal directly through NGINX configuration directives without external clients. Readers should expect F5’s native ACME footprint across the platform to continue expanding as 47-day certificate validity approaches.
> **Crypto-agility at the edge:** BIG-IP is the crypto-agility enforcement point for your internet edge. When NIST publishes an advisory, when a new IETF draft changes a code point, or when your CCOE decides to adjust PQC policy, the change is implemented on a handful of BIG-IP profiles rather than hundreds of application servers.

## Closing the Loop

This book has followed a deliberate arc: why the quantum threat demands action (Chapters 1–2), what replaces the vulnerable algorithms (Chapters 3–4), and how to discover, plan, deploy, and operate the migration (Chapters 5–9). Along the way, we’ve been honest about what’s solved (hybrid key exchange), what’s in progress (certificate authentication), and what’s genuinely hard (DNSSEC, long-lived evidence, and the sheer organizational challenge of touching every cryptographic system in an enterprise).

The PQC migration is the most significant cryptographic transition since the move from DES to AES—and arguably larger, because it touches public-key infrastructure in ways the symmetric transition never did. But it’s also a transition with clear standards, strong community momentum, and years of preparation time for organizations that start now.

The Appendices that follow provide quick-reference tools for your team: a glossary, an algorithm cheat sheet, a compliance checklist, and a vendor PQC readiness assessment template. Keep this book within arm’s reach. The migration is a multi-year journey, and the operational practices in this chapter will be your daily companion long after the deployment celebrations are over.

## Notes

The following sources support specific claims made in Chapter 9. Full bibliographic entries appear in the Bibliography.

**1.**  The “harvest-now, forge-later” concept for digital signatures is analogous to the “harvest-now, decrypt-later” threat for encryption. An adversary captures classically signed artifacts today and uses a future quantum computer to forge signatures, retroactively compromising integrity and non-repudiation. See: “Post-Quantum-Resilient Audit Evidence for Long-Lived Regulated Systems,” arXiv:2512.00110 (February 2026).

**2.**  Three migration patterns for legacy evidence: hybrid signatures for new artifacts, re-signing legacy artifacts with PQC keys, and Merkle root anchoring for batch re-authentication. Formalized in arXiv:2512.00110 with security proofs (Q-Audit Integrity, Q-Non-Equivocation, Q-Binding) and benchmarks on commodity hardware.

**3.**  CNSA 2.0 timeline: software and firmware signing should prefer PQC by 2025, with exclusive PQC required by 2030. NSA guidance explicitly encourages dual-signing firmware immediately. NIST SP 800-208 approves stateful hash-based signatures (LMS, XMSS) specifically for code signing and secure boot use cases.

**4.**  CA/Browser Forum Ballot SC-081v3. Certificate maximum validity shrinks to 200 days (March 2026), 100 days (March 2027), 47 days (March 2029). ACME-based automation becomes operationally essential at these renewal velocities.

**5.**  The ACME protocol is specified in RFC 8555 (Barnes, R., Hoffman-Andrews, J., McCarney, D., Kasten, J. “Automatic Certificate Management Environment (ACME).” IETF, March 2019). ACME v2 API was released in March 2018 and standardized in RFC 8555. Native ACME support in web servers and reverse proxies: Apache HTTP Server since 2.4.30; Caddy and Traefik as default behavior; NGINX ngx_http_acme_module preview released August 12, 2025 (see NGINX Community Blog, “NGINX Introduces Native Support for ACME Protocol”). F5 provides an ACMEv2 client for BIG-IP via the open-source Kojot ACME project on GitHub (f5devcentral/kojot-acme, MIT licensed), supporting HTTP-01, DNS-01, wildcard certificates, HSM/FIPS key preservation, HA, and OCSP.

**6.**  HSM readiness questions from Chapter 6: (1) Does the HSM support ML-KEM/ML-DSA? (2) Does the API map to your PKI’s calling conventions? (3) Can the HSM back up and replicate PQC keys in HA configurations? (4) What are the performance benchmarks for PQC operations? (5) Is the implementation FIPS 140-3 validated? Thales, Entrust, and Marvell/Cavium are in various stages of PQC support rollout.

**7.**  Performance baselining: capture TLS handshake latency at p50, p95, and p99 before enabling PQC. Use existing APM tools (Prometheus/Grafana, F5 AST/Insight, Datadog, New Relic) to establish clean baselines. Post-migration, compare same metrics on same paths to isolate PQC-induced changes from unrelated variables.

**8.**  Supply chain PQC risk: a third-party provider using RSA-2048 creates a quantum-vulnerable link regardless of your internal migration status. CISA and NIST NCCoE guidance recommends extending PQC assessments to third-party vendors. Multiple sources (DigiCert, Palo Alto Networks) emphasize that “your PQC migration is only as strong as your weakest vendor.”

**9.**  USDA Acquisition Regulation (AGAR), revised September 2025, contains explicit PQC procurement language: products in CISA-listed categories must support PQC. Additional agencies are expected to adopt similar language through agency-specific acquisition rules. See: postquantum.com, “The Complete US Post-Quantum Cryptography Regulatory Framework in 2026.”

**10.**  NIST CSWP 39 (Cybersecurity White Paper): “Crypto-Agility Considerations for Migrating to Post-Quantum Cryptographic Algorithms.” Recommends maintaining a living cryptographic inventory (CBOM) as part of continuous security monitoring. Integration with NIST CSF v2.0 functions: Identify, Protect, Detect, Respond, Recover.

Next: Appendices — Glossary, Algorithm Cheat Sheet, Compliance Checklist, Vendor PQC Readiness Template, and Bibliography

### Appendix D
