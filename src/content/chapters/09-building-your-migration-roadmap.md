---
title: "Building Your Migration Roadmap"
displayTitle: "Chapter 6: Building Your Migration Roadmap"
section: "Chapters"
chapter: 6
order: 9
words: 4454
readingMinutes: 20
excerpt: "You’ve catalogued the threat (Chapters 1–2), learned the replacements (Chapter 3), mapped the mandates (Chapter 4), and inventoried your exposure (Chapter 5). Now comes the question that separates planning from action: “"
---

You’ve catalogued the threat (Chapters 1–2), learned the replacements (Chapter 3), mapped the mandates (Chapter 4), and inventoried your exposure (Chapter 5). Now comes the question that separates planning from action: “How do we actually do this?”

This chapter provides the organizational structure, prioritization framework, and phased migration template you need to turn your cryptographic inventory into a funded, staffed, executable program. This is not theory. It’s a migration playbook.

## Step 1: Build the Team — The Cryptographic Center of Excellence

PQC migration is not a network project. It’s not a security project. It’s not a compliance project. It’s all of them simultaneously, which means it dies in the gaps between teams unless you create a **cross-functional body with a clear mandate.**

We recommend establishing a **Cryptographic Center of Excellence (CCOE)**: a small, empowered group of strategic thinkers and complex problem solvers drawn from across the organization. The CCOE doesn’t replace existing teams. It coordinates them, sets cryptographic policy, and owns the migration roadmap.<sup>1</sup>

### Recommended CCOE Composition

| **Role / Domain** | **Why They’re at the Table** |
| --- | --- |
| **Network Security** | Owns TLS termination, IPsec VPNs, load balancer configurations, and the infrastructure where most visible PQC changes happen first. |
| **Application Security** | Understands how applications use cryptographic libraries, API authentication, and session management. Identifies application-layer migration dependencies. |
| **Identity & Access Management** | Owns PKI, certificate lifecycle, smart card / CAC/PIV authentication, and federation protocols (SAML, OIDC) that depend on digital signatures. |
| **Infrastructure / Endpoint Security** | Manages OS-level crypto (disk encryption, code signing verification, secure boot), endpoint configurations, and patch management. |
| **Development / DevSecOps** | Controls CI/CD pipelines, application code, cryptographic library selection, and the speed at which software can be updated for new algorithms. |
| **Cryptography SME** | Provides algorithm expertise, evaluates implementation correctness, and advises on parameter set selection. May be internal or external consultant. |
| **Risk & Compliance** | Maps PQC requirements to regulatory frameworks (FISMA, CMMC, FedRAMP, HIPAA, PCI-DSS). Tracks compliance posture and reports to leadership. |
| **Procurement / Budget** | Ensures PQC readiness criteria are embedded in vendor evaluations and acquisition processes. Manages the funding lifecycle for the migration program. |

The CCOE should be small (8–12 people), empowered to set cryptographic policy, and have a direct reporting line to the CISO or CTO. Its mandate: ensure consistent, strategic, and measurable PQC migration across the organization.

> **PLAIN-LANGUAGE SIDEBAR**
> If your organization doesn’t have the internal expertise to staff a cryptography SME role, that’s normal. Most don’t. The CCOE can work with external consultants, your security vendor’s engineering team, or industry bodies like the PKI Consortium for specialized guidance. The important thing is that the cross-functional structure exists. The expertise can be sourced.

## Step 2: Design for Crypto-Agility

Before you start replacing algorithms, establish a design principle that will save you from doing this again in a decade: **crypto-agility.**

NIST defines crypto-agility as “the capabilities needed to replace and adapt cryptographic algorithms in protocols, applications, software, hardware, and infrastructures without interrupting the flow of a running system.”<sup>2</sup> In December 2025, NIST published CSWP 39 (“Considerations for Achieving Crypto Agility: Strategies and Practices”), elevating crypto-agility from a nice-to-have to a formal strategic framework.

The core idea: **never hard-code cryptographic choices again.** The PQC migration should be the last time your organization does a panic-driven, multi-year cryptographic overhaul. After this transition, your architecture should support algorithm swaps as routine maintenance, not emergency projects.

### Four Pillars of Crypto-Agility

- **Modularity:** Separate cryptographic algorithms from application logic. Use cryptographic APIs that abstract the algorithm choice, so the same API call can invoke classical or PQC algorithms without application changes.

- **Policy-driven configuration:** Cryptographic choices should be set by external policy (machine-readable configuration profiles), not compiled into software. When an algorithm is deprecated, an administrator updates a policy; developers don’t rewrite code.<sup>3</sup>

- **Inventory and monitoring:** You can’t be agile about what you can’t see. The CBOM from Chapter 5 isn’t a one-time deliverable: it’s a living system that continuously tracks what cryptography is deployed where.

- **Testing and validation:** Build automated tests that verify cryptographic configurations against policy. When a new algorithm is approved or an old one deprecated, the test suite catches drift before auditors do.

CSWP 39 introduces a maturity model for crypto-agility, ranging from unstructured and reactive practices at the low end to fully adaptive programs integrated into enterprise risk management.<sup>2</sup> The PQC migration is your opportunity to climb that maturity curve. Don’t just solve the quantum problem. Build the capability to solve the next cryptographic problem, whatever it is.

### Crypto-Agility in Five Layers

The four pillars above describe what crypto-agility looks like as a design discipline. But ”be crypto-agile” is the kind of advice that’s easy to nod at and hard to operationalize. What does it actually mean to build agility into an organization’s cryptographic stack?

Gartner’s PQC journey guide offers one of the cleanest decompositions we’ve found: crypto-agility shows up at five distinct layers, and each requires its own decisions, its own tools, and its own owners. Treating agility as a single objective tends to make it everyone’s job and therefore nobody’s. Treating it as five layers, each with concrete deliverables, makes it tractable.<sup>7</sup>

![figure](/book-media/img-07.png)

*Figure 6.2 — The Five Layers of Crypto-Agility*

**Vendor layer.** The vendor layer is about the products and platforms an organization brings in to host its cryptography. Agility here means buying from vendors who follow open standards rather than proprietary protocols. A standards-based product can interoperate with the rest of the ecosystem and can adopt new IETF or NIST algorithms as they ship; a proprietary one becomes a hostage. For PQC specifically, the minimum bar is FIPS-approved algorithms (ML-KEM, ML-DSA, SLH-DSA) and IETF-defined protocol profiles for TLS 1.3, IKEv2, and X.509. Any vendor selling "quantum-safe" cryptography that doesn’t land cleanly in one of those buckets deserves a hard second look.

**Feature layer.** The feature layer is about whether the products already in production can be upgraded without being ripped out and replaced. Field-upgradable hardware and software is the difference between a cipher migration that takes a configuration change and one that takes a procurement cycle. Ask every cryptographic-touching vendor what their PQC delivery mechanism looks like, and treat "wait for the next major version" as a yellow flag.

**Data layer.** The data layer is where things get unglamorous and important. Larger keys and ciphertexts mean larger fields in databases, longer columns in audit logs, larger signed envelopes in document formats, and bigger entries in directory schemas. If those schemas weren’t sized for it, PQC migration breaks them in subtle ways: truncated signatures that validate locally and fail downstream, or queries that silently drop rows when the certificate field overflows. Building data-layer agility means auditing every place a cryptographic artifact is stored or transmitted and making sure it can carry, at minimum, an ML-DSA-87 signature (approximately 4,627 bytes) or an ML-KEM-1024 ciphertext (approximately 1,568 bytes) with headroom for future algorithm growth.

**Algorithm layer.** The algorithm layer is the cleanest agility win and the easiest one to design in. The principle is straightforward: algorithm selection should be a runtime policy decision, not a compiled-in constant. A TLS terminator should accept a cipher group as configuration. A signing service should accept an algorithm identifier as a parameter. A KMS should let policy decide whether new keys are ML-DSA-65 or ML-DSA-87. When agility is configured rather than coded, swapping algorithms in response to a new cryptanalytic advisory becomes a change ticket, not a software release. NIST CSWP 39 formalizes this as "modularity," and it is the single most important agility property a system can have.

**Key layer.** The key layer is about the operational machinery that issues, rotates, and retires keys and certificates. None of the layers above matter if cert rotation takes three weeks and a change-advisory-board approval. Agility at this layer is automation: ACME for certificate lifecycle, KMS-managed key rotation policies, HSM-backed signing operations that don’t require staring at a terminal. The CA/Browser Forum 47-day maximum certificate validity in March 2029 alone makes automated certificate lifecycle management non-optional; organizations that haven’t automated certificate operations by the end of 2027 will be trying to do that and PQC algorithm change at the same time.

Strong crypto-agility is the product of all five layers, not any one of them. A standards-based vendor running upgradable platforms that handle larger artifacts via policy-driven algorithm selection and automated certificate operations: that’s an organization that can absorb its next algorithm migration as routine work, not crisis response. The PQC migration is the first test of these layers for most organizations. It will not be the last.

> **F5 PERSPECTIVE**
> **BIG-IP Maps to All Five Layers**
> The five layers map cleanly onto how the BIG-IP platform is architected.
> **Vendor layer.** ML-KEM and ML-DSA arrive through FIPS-validated OpenSSL modules and IETF-defined TLS 1.3 profiles: no proprietary cipher extensions, no parallel "F5-flavored" PQC. What you negotiate on the wire is what the standards bodies published.
> **Feature layer.** Customers move from classical to hybrid PQC via firmware upgrade. v17.5.1 introduced X25519MLKEM768 hybrid key exchange; v21.1 expanded the supported PQC cipher set. No platform refresh, no new licensing, no procurement cycle.
> **Data layer.** The certificate chain math in Chapter 8 (ML-DSA-65 chains running 15–20 KB on the wire) translates into concrete BIG-IP capacity planning. Memory per connection scales, SSL profile sizing matters more than it did with ECDSA, and TLS Certificate Compression (RFC 8879) becomes a profile setting worth turning on by default.
> **Algorithm layer.** The SSL cipher group is a configuration object, not a code path. Fleet-wide algorithm changes ship via iControl REST, AS3 declarations, or BIG-IQ. An algorithm rollback in response to a future cryptanalytic advisory is a config push, not a software release.
> **Key layer.** BIG-IP v21.1 added native ACME v2 client support on the TLS terminator, eliminating the need for external Certificate Lifecycle Management glue for automated renewal. Combined with the CA/Browser Forum 47-day validity deadline in March 2029, this is the layer where v21.1 carries the most operational weight.

> **⚠  MANDATE ALERT**
> **Eight Things Your Crypto Policy Must Now Address**
> Updating internal cryptographic policy is one of the cheapest deliverables of a postquantum program, and one of the highest-leverage. Every architecture decision, vendor procurement, and engineering pattern that follows will reference the policy. At minimum, it should address:
> **Deprecation timelines** for RSA, DH, ECC, and other quantum-vulnerable algorithms, aligned to NIST IR 8547 (deprecated after 2030, disallowed after 2035) unless sector mandates pull dates earlier.
> **PQC adoption timelines and conditions,** including which algorithms are approved, at which parameter sets, and whether hybrid deployment is required during the transition window.
> **Minimum parameter sets per security category:** FIPS Category 3 (ML-KEM-768 / ML-DSA-65) as the default; Category 5 (ML-KEM-1024 / ML-DSA-87) for long-lived signing keys and 25-plus-year data.
> **Hybrid versus pure PQC strategy:** where each pattern applies, and when the transition from hybrid to pure PQC is scheduled.
> **Position on QKD and adjacent techniques** (photonic-layer protection, fully homomorphic encryption, multiparty computation). The defensible default: not for general-purpose cryptography; revisit if NSA/NIST guidance changes.
> **Vendor readiness deadlines** with explicit consequences for vendors that miss them (re-procurement, exception process, contract triggers).
> **Cryptographic inventory mandate:** new systems register their cryptographic dependencies in the CBOM at deployment, not after.
> **Crypto-agility requirements:** algorithm selection as configuration, not hard-coded constants. NIST CSWP 39 supplies the reference framework.

## Step 3: Prioritize Based on Risk, Not Compliance Dates

With your CBOM in hand and your CCOE assembled, the next question is: what do we migrate first?

The temptation is to prioritize by compliance deadline: “CNSA 2.0 says networking by 2026, so we start there.” That’s not wrong, but it’s incomplete. The better framework prioritizes by **risk exposure**, which accounts for both compliance and the actual damage a quantum adversary could inflict:

| **Priority** | **Criteria** | **Examples** | **Action** |
| --- | --- | --- | --- |
| **P0** | HNDL-exposed + long-lived data + internet-facing | TLS key exchange on internet-facing services protecting classified, financial, or medical data | **Migrate now. Deploy hybrid key exchange immediately.** |
| **P1** | HNDL-exposed + moderate data lifetime + internet-facing | General web TLS, VPN tunnels, partner-to-partner links, email encryption | Begin migration within 6 months. Hybrid mode. |
| **P2** | Authentication and signatures on long-lived artifacts | Code signing, firmware signing, CA certificates, legal/compliance evidence | Plan migration within 12 months. CNSA 2.0 firmware signing is urgent. |
| **P3** | Internal infrastructure + moderate data sensitivity | Internal TLS between microservices, east-west traffic, internal PKI, SSH keys | Migrate within NIST timeline. Plan for 2028–2032 execution. |
| **P4** | Low-sensitivity + short-lived data + low interception risk | Ephemeral session tokens, internal API keys, transient development environments | Upgrade during normal refresh cycles. Low urgency. |

Notice that key exchange (confidentiality) consistently outranks signatures (authentication) in priority. That’s because the HNDL threat applies to key exchange today: captured traffic can be decrypted retroactively. Signatures, by contrast, only need to be quantum-resistant at the time they’re verified. This is why Chrome, NIST, and most migration frameworks recommend **key exchange first, signatures second.**<sup>4</sup>

## Step 4: Assess HSM and Infrastructure Readiness

Before you can execute the migration, you need to know whether your infrastructure can actually support the new algorithms. The most common blocker is **HSM readiness.** Hardware Security Modules sit at the root of trust for most certificate and signing operations, and if your HSM can’t handle PQC algorithms, your PKI migration stalls before it starts.<sup>5</sup>

### Five HSM Planning Questions

- **Algorithm support:** Does the HSM firmware expose the PQC algorithms you need (ML-KEM, ML-DSA, LMS/XMSS)? Which parameter sets are available?

- **API and connector mapping:** How do PQC key types map into PKCS#11, vendor APIs, and the application connectors your CA, signing platform, and identity systems use?

- **Backup and HA semantics:** Do new PQC key types change how cloning, backup, restore, or active-active designs behave? Stateful hash-based signatures (LMS/XMSS) have unique state management requirements.

- **Performance and object size:** Larger PQC keys and signatures change throughput, storage, CSR processing, and certificate issuance rates. Benchmark before committing to a production timeline.

- **Validation and compliance timing:** Algorithm availability in a product is not the same as FIPS 140-3 validation. Verify the exact firmware version, validation state, and expected certification timeline for your environment.

HSM vendor readiness is improving rapidly but unevenly. Thales Luna HSMs support ML-DSA through firmware 7.9.0+. Entrust nShield 5 has NIST CAVP-validated support for ML-DSA, ML-KEM, and SLH-DSA with FIPS 140-3 certification work following.<sup>6</sup> The planning lesson: verify the exact firmware, SDK, connector, and validation path before committing a PKI or signing architecture to a date.

## Step 5: Execute in Phases

![figure](/book-media/img-08.png)

*Figure 6.1 — PQC Migration Roadmap: Five Phases (2026–2035)*

The most credible migration plan is phased: edge first, origins next, trust infrastructure after that, and supply chain signing alongside. Here’s the template:

| **Phase** | **Timeline** | **Key Actions** |
| --- | --- | --- |
| **Phase 0: Organize** | Months 1–3 | Establish CCOE. Complete CBOM for P0 systems. Assess HSM readiness. Define crypto-agility policy. Set budget and executive sponsorship. |
| **Phase 1: Edge First** | Months 3–9 | Deploy hybrid key exchange (ML-KEM + X25519) on internet-facing TLS termination points. Pilot 2–3 services. Measure client compatibility, performance, and operational impact. Expand to all P0 and P1 services. |
| **Phase 2: Trust Infrastructure** | Months 6–18 | Migrate code signing and firmware signing to PQC (CNSA 2.0 priority). Begin PKI migration: issue PQC certificates from internal CAs. Update HSMs. Test hybrid certificate chains. Migrate VPN/IPsec key exchange. |
| **Phase 3: Broaden** | Months 12–30 | Migrate P2 and P3 systems. Expand PQC to internal TLS, SSH, email encryption, and database encryption. Replace quantum-vulnerable certificates across the enterprise. Address partner and supply chain dependencies. |
| **Phase 4: Complete and Sustain** | Months 24–36+ | Retire all quantum-vulnerable algorithms. Transition from hybrid to pure PQC where appropriate. Embed crypto-agility into ongoing operations (Chapter 9). Decommission legacy cryptographic configurations. Validate compliance posture against NIST 2035 deadline. |

> **⚠  MANDATE ALERT**
> These timelines are templates, not mandates. Your actual pace depends on your regulatory environment, infrastructure complexity, and risk tolerance. For CNSA 2.0 organizations, Phase 1 should already be in progress. For commercial organizations following the NIST timeline, the UK NCSC’s Phase 1 target (crypto inventory and plan complete by 2028) is a reasonable benchmark.

> **F5 PERSPECTIVE**
> **Edge-First Migration with F5 BIG-IP**
> Phase 1 of the migration roadmap (hardening internet-facing TLS key exchange) maps directly to F5’s deployment model. BIG-IP already sits at the TLS offload point for most F5 customers, making it the fastest place to prove PQC progress.
> The operational pattern: enable hybrid TLS 1.3 (X25519MLKEM768) on the browser-facing side of BIG-IP while preserving classical TLS on the backend origin connections. This hardens the internet-exposed leg against HNDL risk immediately, without requiring every origin server, application framework, or backend library to be upgraded first.
> This “bridge architecture” is often the right operational choice, but it should be described honestly: it improves the front door first. It does not make the full application path post-quantum safe if the backend is still classical. The program still has to expand into PKI, certificates, HSMs, code signing, device identity, and supply chain trust. BIG-IP is the starting point, not the whole program.
> Chapter 7 covers the hybrid deployment patterns in detail.

## Selling the Roadmap: Budget and Executive Sponsorship

A migration roadmap without budget is a wish list. Here’s how to frame the investment for leadership:

- **Frame it as risk reduction, not compliance:** “We’re reducing the window during which captured data can be retroactively decrypted” is a more compelling message than “NIST says we have to.”

- **Quantify the crypto debt cleanup:** Your discovery pilot (Chapter 5) found SHA-1 in production, expired certificates, and TLS 1.0 connections. Those are security risks today, not just quantum risks. The PQC budget fixes both.

- **Use the SHA-1 precedent:** The SHA-1 to SHA-2 migration took 12+ years and cost organizations billions in aggregate. The PQC migration is larger and more complex. Early investment reduces total cost.

- **Show the regulatory trajectory:** The Master Timeline from Chapter 4 demonstrates that deadlines are converging across NIST, CNSA 2.0, UK NCSC, and EU NIS2. This isn’t one agency’s opinion. It’s global consensus.

- **Start small, prove value:** Phase 0 and the early Phase 1 pilot can be funded from existing security budgets. The pilot results (discovery findings + performance benchmarks + client compatibility data) justify the larger Phase 2–4 investment.

> **PLAIN-LANGUAGE SIDEBAR**
> **What Does PQC Migration Actually Cost?**
> The U.S. federal government estimated total government-wide PQC migration costs at $7.1 billion between 2025 and 2035, and requires agencies to update cost estimates annually. While your organization won’t spend billions, the cost categories are the same:
> **Personnel and expertise:** staff time for discovery, planning, testing, and execution. This is typically the largest cost. Expect 2–5 FTEs dedicated to the CCOE for 3–5 years in a mid-size enterprise.
> **Hardware replacement:** HSMs, network appliances, and embedded devices that cannot be firmware-upgraded to support PQC may need replacement. This is the wild card; cost varies dramatically by environment.
> **Software and tooling:** crypto discovery tools, certificate lifecycle management platforms, testing infrastructure, and vendor upgrades.
> **Potential downtime and rollback:** budget for complications. The AIVD/TNO PQC Migration Handbook emphasizes that unforeseen issues during execution are common and a robust rollback procedure is essential.
> The PQC migration is also an opportunity: the crypto debt cleanup (finding SHA-1, expired certs, TLS 1.0) delivers security value today, not just in a post-quantum future. Frame the investment as infrastructure modernization, not just compliance.

## Building the Financial Case

The arguments above frame the pitch. Securing the actual funding is a separate exercise, one that depends less on the strength of the pitch and more on how the program integrates with the organization’s financial planning cycle. Funding for a multi-year cryptographic program is not a line item your finance team has seen before; the financial pattern has to be built from scratch.<sup>7</sup>

A useful working frame: the postquantum program is a multi-year capital and operating investment that competes with every other multi-year initiative in the organization. Treat finance as a partner, not a gatekeeper. The earlier they understand the cryptographic risk and the migration shape, the more likely they are to defend the budget when other priorities crowd it.

### Partner with finance early

Bring the CFO’s office into the conversation during the planning phase, not at the budget-cycle deadline. Walk them through the HNDL risk in plain language. Walk them through the multi-year deliverable structure. Walk them through the cost of doing nothing, not as a scare tactic, but as the alternative scenario any sound investment decision has to compare against. The goal is shared ownership of the program’s financial trajectory, not a one-shot funding ask.

### Plan for reforecasting, not a single budget request

Multi-year cryptographic migrations rarely land on their first estimate. New NIST guidance, vendor delivery slips, discovered scope, and cryptanalytic news will all shift the plan. The financial model should be built to accommodate quarterly or semi-annual reforecasts, with the program lead and a finance partner running the cycle jointly. Organizations that pitch one large number up front and then return for ”additional” funding when the scope shifts erode credibility fast. Organizations that pitch a phased model with explicit reforecast checkpoints build it.

### Frame costs in both tangible and intangible categories

Tangible costs are the easy ones: staff time, tooling licenses, professional services, HSM upgrades, lab and test infrastructure, ongoing certificate operations. These are the line items finance will recognize. Intangible costs need surfacing too: migration-related downtime, opportunity cost of engineering attention pulled from other work, the regression risk of running classical and hybrid in parallel for months. Counting only the tangible costs produces a number that’s too low, and the program runs out of runway in year two.

### Mirror the budget to the roadmap

The first funded deliverable should be a scoping exercise (discovery pilot, vendor assessment, initial CBOM) that produces the data needed to size the rest. This is also the easiest funding ask, because the deliverable is small, the timeline is short, and the output is a defensible plan. Subsequent phases (edge hybrid deployment, internal mTLS, signing infrastructure, legacy bridge architecture) each carry their own scope and cost estimate. The roadmap and the budget become the same document.

### Invest in the right mix of platform and custom tooling

A budget that funds only commercial CLM, discovery, and TLS platforms misses the integration work that holds them together. A budget that funds only custom-built tooling misses the maturity and support of vendor platforms. The right ratio depends on the organization’s engineering capacity and risk tolerance, but the question itself deserves explicit attention in the financial model. ”Buy what’s mature; build what’s specific” is a defensible starting principle.

### Tie metrics to dollars where possible

Finance partners respond to numbers. Where the program can quantify progress (percent of internet-facing endpoints on hybrid TLS, percent of P0 systems migrated, mean time to deploy a new cipher policy), those numbers should feed the financial reporting. They demonstrate execution, justify continued funding, and give finance a defensible answer when other budget owners ask why cryptographic migration is consuming this much capital this many years in a row.

## What’s Next

You have the team (CCOE), the design principle (crypto-agility), the priority matrix (risk-based), the infrastructure assessment (HSM readiness), and the phased plan (edge first). The next chapter dives into the specific technical pattern that dominates Phase 1: hybrid mode, running classical and post-quantum cryptography side by side during the transition. Chapter 7 covers hybrid TLS, hybrid certificates, and the bridge architecture in detail.

## Notes

The following sources support specific claims made in Chapter 6. Full bibliographic entries appear in the Bibliography.

**1.**  The Cryptographic Center of Excellence (CCOE) concept aligns with Gartner’s 2026 PQC guidance, which recommends creating a “cross-functional cryptographic center of excellence with clear mandates to ensure consistent and strategic quantum threat remediation across the organization.” The recommended composition draws from Gartner’s suggested domains: data security, network security, infrastructure, endpoint, application security, development, IAM, cryptography, risk/compliance, procurement, and budgeting.

**2.**  NIST CSWP 39 (Final), “Considerations for Achieving Crypto Agility: Strategies and Practices.” Published December 2025. Defines crypto-agility, proposes a maturity model, and describes technical levers including modularity, policy-mechanism separation, inventory, and testing.

**3.**  CSWP 39 describes “technology-specific, machine-consumable configuration profiles” as a mechanism for enforcing cryptographic policy across systems without hard-coding algorithm choices into software.

**4.**  Chrome’s PQC strategy explicitly prioritizes key exchange over authentication due to the HNDL risk asymmetry. See: Chromium Blog, “Advancing Our Amazing Bet on Asymmetric Cryptography,” May 2024. NIST IR 8547 similarly notes that application-specific guidance may require earlier migration for key establishment to mitigate HNDL.

**5.**  HSM readiness planning framework adapted from F5, Inc. internal PQC field guidance (2025). The five planning questions address the operational dimensions most frequently encountered in customer PQC migration discussions.

**6.**  Thales documents ML-DSA support through Luna HSM Firmware 7.9.0+, with operational caveats for stateful hash-based signatures (LMS-HSS) including backup and HA limitations. Entrust announced NIST CAVP-validated support for ML-DSA, ML-KEM, and SLH-DSA in nShield 5 firmware in 2025, with FIPS 140-3 certification work following. Source: vendor product documentation.

**7.**  Sarah Almond and Mark Horvath, ”A Journey Guide to Postquantum Readiness,” Gartner Research G00843746, 13 March 2026. The five-layer crypto-agility decomposition (vendor, feature, data, algorithm, key) in Step 2 is paraphrased from this source, as is the financial planning guidance in ”Building the Financial Case.” The Mandate Alert’s eight policy requirements also draw on this source.

Next: Chapter 7 — Hybrid Mode: Bridging Classical and Quantum-Safe
