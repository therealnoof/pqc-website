---
title: "Know What You Have: Cryptographic Discovery"
displayTitle: "Chapter 5: Know What You Have: Cryptographic Discovery"
section: "Chapters"
chapter: 5
order: 8
words: 2791
readingMinutes: 13
excerpt: "Every PQC migration plan begins with the same question: “Where is cryptography in my environment?” The answer, invariably, is “more places than you think.”"
---

Every PQC migration plan begins with the same question: “Where is cryptography in my environment?” The answer, invariably, is “more places than you think.”

Cryptography is embedded in every layer of modern IT infrastructure—TLS certificates on web servers and load balancers, SSH keys on Linux hosts, IPsec tunnels between sites, code signing certificates in CI/CD pipelines, S/MIME certificates in email clients, API tokens, database encryption, disk encryption, HSMs, smart cards, and dozens of applications that implement their own cryptographic functions. Most organizations have no comprehensive inventory of these assets. That’s the problem this chapter solves.

Without a cryptographic inventory, you’re migrating blind. You can’t prioritize what you can’t see, you can’t track progress against what you haven’t catalogued, and you can’t prove compliance with mandates that require you to “submit cryptographic inventories.”1

## Why Discovery Is Harder Than It Sounds

If you’ve ever tried to audit certificates across an enterprise network, you know the pain. Cryptographic assets are scattered, undocumented, and often invisible to traditional IT management tools. The challenge has several dimensions:

- **Volume:** A typical enterprise has thousands to tens of thousands of certificates and keys across its environment. Federal agencies may have hundreds of thousands.

- **Diversity:** Cryptography exists in certificates, connection configurations, application code, hardware modules, firmware, IoT devices, and third-party SaaS services—each requiring different discovery techniques.

- **Opacity:** Many systems use cryptography without exposing it to administrators. An application may negotiate TLS internally without any external indication of which cipher suite or key exchange algorithm it’s using.

- **Sprawl:** Multi-cloud, hybrid, and edge architectures mean cryptographic assets span on-premises data centers, AWS/Azure/GCP regions, CDN edge nodes, and partner networks.

- **Fragmentation:** No single team owns cryptography. Network engineers own TLS termination. Security teams own certificates. Developers own code signing. IAM teams own authentication. PKI teams own the CA hierarchy. Each has partial visibility; none has the full picture.

> **PLAIN-LANGUAGE SIDEBAR**
> Think of cryptographic discovery like a building inspection for electrical wiring. You know there’s wiring in every wall—but you don’t know exactly where every wire runs, what gauge it is, or whether it meets current code. The only way to find out is to look—and to look systematically, because missing one segment could mean a fire.

## Three Approaches to Cryptographic Discovery

NIST SP 1800-38B (“Quantum Readiness: Cryptographic Discovery”) identifies a multi-faceted approach to discovery.2 No single method catches everything. A comprehensive inventory requires combining at least three techniques:

| **Discovery Type** | **What It Finds** | **Limitations** |
| --- | --- | --- |
| **Network Scanning** | TLS/SSL versions, cipher suites, certificate details, and key exchange algorithms for any connection visible on the wire. Passive or active. | Sees only what crosses the network. Misses data-at-rest encryption, application-internal crypto, and east-west traffic in microsegmented environments. |
| **Endpoint Scanning** | Installed certificates, key stores, cryptographic libraries (OpenSSL, BoringSSL, NSS, Java KeyStore), SSH keys, disk encryption configurations. | Requires agent or authenticated access to each endpoint. Incomplete for unmanaged devices, IoT, and shadow IT. |
| **Application Testing** | Crypto functions embedded in application code, API calls, hardcoded keys, custom TLS configurations, and third-party library dependencies. | Requires SAST/DAST integration or manual code review. Doesn’t scale easily across large application portfolios. |

The key insight from NIST’s work: **most of the data items required for PQC compliance (algorithm in use, key size, protocol version, certificate authority, expiration date) cannot yet be fully collected with automated tools alone.** NIST SP 1800-38B found that only three of the nine data items required by OMB M-23-02 could be collected automatically. The rest require manual effort or enrichment.3

## What to Catalog: The Cryptographic Bill of Materials

Your cryptographic inventory—sometimes called a **Cryptographic Bill of Materials (CBOM)**—should capture the following for each asset:

- **Algorithm:** Which cryptographic algorithm is in use (RSA-2048, ECDHE-P256, AES-128-GCM, SHA-1, etc.)

- **Function:** What the algorithm does (key exchange, digital signature, bulk encryption, hashing)

- **Protocol context:** Which protocol the algorithm operates within (TLS 1.2, IPsec IKEv2, SSH 2.0, S/MIME)

- **System/application:** Which system or application uses this cryptographic configuration

- **Data classification:** The sensitivity of the data protected by this algorithm (ties back to the HNDL risk matrix from Chapter 2)

- **Owner:** The team or individual responsible for the system

- **Quantum risk status:** Broken by Shor’s, weakened by Grover’s, or safe (directly from the Chapter 2 vulnerability map)

- **Migration priority:** Based on data sensitivity, exposure to HNDL, and regulatory deadline

> **⚠  MANDATE ALERT**
> OMB M-23-02 requires federal agencies to report nine specific data items for each cryptographic system. CISA’s Automated Cryptography Discovery and Inventory (ACDI) strategy is building toward automated collection, but the tools are not yet mature enough to cover the full requirement. Plan for significant manual effort in the first inventory pass, then work toward automation for ongoing maintenance.

## Don’t Boil the Ocean: A Phased Discovery Approach

![figure](/book-media/img-06.png)

*Figure 5.1 — Cryptographic Discovery: Four Phases*

Attempting to discover every cryptographic asset across your entire environment simultaneously is a recipe for paralysis. Instead, take a phased approach driven by business criticality:

### Phase 1: Critical Systems (Months 1–4)

Note: these time frames will adjust for network complexity and scope. A 20 person small business scales differently than a global 200k person enterprise.

Focus on systems that protect CRITICAL and HIGH-tier data (per Chapter 2’s HNDL risk matrix): classified networks, financial transaction systems, healthcare records, executive communications, and any system processing data with a sensitivity lifetime exceeding 10 years. Start with network-facing systems where HNDL exposure is greatest.

### Phase 2: Internet-Facing and Partner Connections (Months 3–8)

Expand to all internet-facing TLS endpoints (web applications, API gateways, CDN configurations), VPN concentrators, partner-to-partner encrypted links, and email infrastructure. These systems have the highest interception likelihood.

### Phase 3: Internal Infrastructure (Months 6–12)

Cover internal certificate infrastructure, east-west TLS between microservices, database encryption, code signing and CI/CD pipelines, SSH key estates, and endpoint disk encryption. This phase is the longest because it touches the broadest surface area.

### Phase 4: Sustain and Automate (Ongoing)

Transition from project-based discovery to **continuous inventory management.** Integrate discovery into CI/CD pipelines so new applications are inventoried at deployment. Embed cryptographic checks into security scanning (SAST/DAST). Make the CBOM a living document, not a one-time snapshot.

## Inventory at Source: The Long-Term Strategy

Discovery tools are essential for the initial inventory, but they’re not a sustainable long-term strategy on their own. The more mature approach is to **address inventory at source**—ensuring that new cryptographic assets are added to the inventory the moment they’re implemented, rather than waiting for a periodic scan to find them.4

Practical ways to implement inventory at source:

- **CI/CD integration:** Add cryptographic checks to your deployment pipeline. When a new application is deployed, its TLS configuration, certificate chain, and cipher suite preferences are automatically catalogued.

- **Certificate lifecycle management:** If you’re issuing certificates through an enterprise CA (or using a CLM platform like Venafi, Keyfactor, or AppViewX), every certificate issuance should automatically update the CBOM.

- **Infrastructure-as-Code:** If TLS configurations are defined in Terraform, Ansible, or similar tools, the inventory can be derived directly from the IaC repository.

- **Procurement requirements:** When acquiring new hardware or software, require vendors to disclose the cryptographic algorithms and library versions used. This becomes part of your supply chain risk management.

The goal is to shift discovery from being the primary method of inventory population to a validation and exception-finding mechanism. New assets are inventoried at source; discovery scans catch anything that slipped through the cracks.

## The Opportunity: Cleaning Up Cryptographic Debt

Here’s the silver lining in the PQC discovery process: **it forces you to confront cryptographic debt you’ve been carrying for years.**

When you start scanning your environment, you will find things that shouldn’t be there—and they won’t all be quantum-related. You’ll find:

- Expired certificates nobody renewed (or knew about)

- SHA-1 signatures still in production (classically broken since 2017)

- TLS 1.0 and 1.1 connections that should have been retired years ago

- 3DES cipher suites still negotiated by legacy clients

- Self-signed certificates in production systems with no rotation schedule

- RSA-1024 keys that haven’t been updated since they were deployed in 2008

- SSH keys that have never been rotated and are shared across teams

The PQC migration is an opportunity to clean house. Frame it that way for your leadership: “We’re not just preparing for quantum—we’re fixing the cryptographic hygiene issues we’ve been deferring for a decade.” That framing turns a compliance exercise into a genuine security improvement, which is a much easier budget conversation.

> **F5 PERSPECTIVE**
> **Strategic Points of Control: How F5 Enables Cryptographic Discovery**
> The following section describes how F5 capabilities can support the cryptographic discovery process. This is vendor-specific guidance—the methodology described above applies regardless of your infrastructure stack.
> F5 devices—BIG-IP, SSL Orchestrator, NGINX—sit at strategic control points in the network where application traffic converges: between users and applications, between applications and APIs, between sites, and between cloud environments. This positioning provides a unique vantage point for cryptographic visibility that most organizations already have deployed but aren’t fully leveraging for PQC readiness.
> **BIG-IP SSL Orchestrator (SSLO)** decrypts and re-encrypts TLS traffic at line speed using F5’s full-proxy architecture. For every connection that passes through SSLO, the system sees the complete cryptographic handshake: the cipher suite negotiated, the key exchange algorithm used, the certificate presented, the TLS version, and the certificate chain. This means SSLO already possesses the raw data needed for network-level cryptographic inventory—the question is how to extract, catalog, and act on it.
> In a PQC discovery context, SSLO can identify:
> •  Which connections still negotiate RSA, ECDHE, or DH key exchange (Shor’s-vulnerable)
> •  Which server certificates use RSA or ECDSA signatures (Shor’s-vulnerable)
> •  Which connections use AES-128 vs. AES-256 (Grover’s exposure)
> •  Which connections still use TLS 1.0/1.1 or weak cipher suites (cryptographic debt)
> •  The volume and frequency of connections by cryptographic profile (prioritization data)
> **F5 Application Study Tool (AST) and F5 Insight** extend this visibility into operational dashboards. AST is an open-source tool built on OpenTelemetry, Prometheus, and Grafana that collects telemetry data from BIG-IP devices across your fleet. F5 Insight (announced March 2026 as part of the F5 ADSP platform) builds on AST’s foundation to provide end-to-end observability with AI-assisted analysis.
> For PQC compliance, the combination of SSLO + AST/Insight enables a network-centric view of your cryptographic posture: which algorithms are in active use, at what volume, protecting what traffic categories, and—critically—which connections are still using quantum-vulnerable configurations. This data feeds directly into the CBOM and supports the risk-based prioritization framework described earlier in this chapter.
> **BIG-IP v21.1** (announced March 2026) adds NIST-compliant PQC cipher support with hybrid TLS cipher groups, allowing organizations to enable PQC protection while maintaining backward compatibility with classical configurations. BIG-IP Zero Trust Access (formerly APM) adds quantum-resistant TLS and SSL VPN tunneling. This means F5 isn’t just helping you discover your quantum exposure—it’s also providing the upgrade path for the infrastructure you’re likely using to terminate and inspect that traffic.

## Running a Discovery Pilot: Proof of Value

Before committing to a full enterprise discovery program, run a well-scoped pilot. This serves two purposes: it validates your toolset and methodology, and it produces concrete findings that justify the budget for the full inventory.5

### Pilot Scope Recommendations

- **Select 2–3 representative environments** (e.g., one internet-facing web application environment, one VPN/IPsec infrastructure, one internal certificate domain)

- **Run all three discovery types** (network scan, endpoint scan, application review) on the pilot scope to compare coverage and gap areas

- **Allocate 4–6 weeks for the pilot,** including analysis and report generation

- **Document everything you find** that wasn’t expected—this is your “cryptographic debt” evidence, and it’s your most compelling argument for broader investment

- **Expect surprises.** NIST’s NCCoE work found that automated discovery tools routinely reveal hundreds or thousands of cryptographic assets that organizations didn’t know existed6

The pilot report becomes your proof of value—evidence that the quantum-vulnerable surface area is real, quantifiable, and larger than leadership assumed. That report is how you get the resources for Phases 1–4.

> **PLAIN-LANGUAGE SIDEBAR**
> In highly-regulated environments, pilot work needs vocabulary that auditors and mission owners recognize. Two patterns are worth naming before you start.
> **Concurrent shadow operation means** running the new PQC-capable path alongside the classical path in production, with the classical path as the safety net. Hybrid TLS 1.3 (X25519MLKEM768) is the canonical example: the handshake negotiates both a classical and a post-quantum shared secret, and the session key is derived from both. The PQC contribution “shadows” the classical exchange—if ML-KEM fails for any reason (library bug, implementation defect, side-channel discovery), the classical portion alone is sufficient to keep connections working. You gain production evidence about PQC behavior without gambling operational stability on it.
> **Regional rollout means** enabling PQC in one region, availability zone, or mission enclave first, instrumenting it thoroughly, then expanding outward. The pattern is feature-flag management applied to cryptography—what’s new is the measurement burden: handshake latency distribution (p50/p95/p99), client failure rates, certificate-size fragmentation impact (Chapter 8), and HSM throughput under PQC load (Chapter 9). For federal and DoD environments, “region” often maps to a mission-specific enclave or security domain rather than geography.
> Both patterns carry forward into Phase 1 of the migration roadmap (Chapter 6) and are the operational foundation for the hybrid TLS work in Chapter 7.

## What’s Next

With your cryptographic inventory in hand, you now have the data needed to build a prioritized migration plan. Chapter 6 takes the discovery output and transforms it into a phased migration roadmap—complete with a recommended organizational structure (the Cryptographic Center of Excellence), risk-based prioritization, and the crypto-agility principles that ensure you’re never locked into a single algorithm again.

## Notes

The following sources support specific claims made in Chapter 5. Full bibliographic entries appear in the Bibliography.

**1.**  OMB Memorandum M-23-02 (November 18, 2022) requires FCEB agencies to submit cryptographic inventory reports. The Quantum Computing Cybersecurity Preparedness Act mandates ongoing cryptographic inventories as a statutory obligation. NSM-10 requires annual submissions of quantum-vulnerable IT system inventories.

**2.**  NIST SP 1800-38B (Preliminary Draft), “Migration to Post-Quantum Cryptography: Quantum Readiness—Cryptographic Discovery.” Describes a multi-faceted discovery approach including network scanning, endpoint analysis, and application testing. Produced in collaboration with 47+ industry partners including AWS, IBM, Microsoft, Samsung SDS, and others.

**3.**  CISA, “Strategy for Migrating to Automated Post-Quantum Cryptography Discovery and Inventory Tools.” September 2024. Notes that only three of the nine M-23-02 data items can currently be collected with automated tools; the remaining six require manual collection or enrichment.

**4.**  The “inventory at source” concept aligns with Gartner’s PQC guidance (2026), which recommends that organizations “address inventory at source so that new assets are added to the inventory when implemented, and discovery becomes more relevant to exceptions rather than the primary method for inventory additions.”

**5.**  Gartner PQC guidance (2026) recommends “use a well-scoped discovery pilot as proof of value to aid in discovery toolset evaluation” and to “allocate at least 12 months for the cryptographic discovery of critical systems.”

**6.**  SafeLogic, “NIST Publishes Next Volume of PQC Migration Guidance” (2025). Notes that automated discovery tools in the NCCoE project routinely revealed hundreds to thousands of previously unknown cryptographic assets across participant environments.

**7.**  F5, Inc. “BIG-IP SSL Orchestrator.” Product documentation. SSLO provides high-performance decryption/re-encryption of inbound and outbound TLS traffic with policy-based steering and security service chaining. See: https://www.f5.com/products/big-ip-services/ssl-orchestrator

**8.**  F5, Inc. “Application Study Tool (AST).” Open-source project on GitHub (f5devcentral/application-study-tool). Uses OpenTelemetry Collector with enhanced BIG-IP data receivers, Prometheus, and Grafana for fleet-wide telemetry and visualization.

**9.**  F5, Inc. “F5 Strengthens Its Application Delivery and Security Platform.” Press release, March 2026. Announces F5 Insight for ADSP, BIG-IP v21.1 with NIST-compliant PQC cipher support and hybrid TLS cipher groups, and quantum-resistant TLS/SSL VPN tunneling in BIG-IP Zero Trust Access.

Next: Chapter 6 — Building Your Migration Roadmap
