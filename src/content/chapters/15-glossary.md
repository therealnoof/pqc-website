---
title: "Glossary"
displayTitle: "Glossary"
section: "Appendices & Reference"
chapter: null
order: 15
words: 1542
readingMinutes: 7
excerpt: "Quick-reference definitions for terms used throughout this book. Terms are listed alphabetically."
---

Quick-reference definitions for terms used throughout this book. Terms are listed alphabetically.

**AES (Advanced Encryption Standard)**  Symmetric block cipher standardized by NIST. AES-128/192/256 refers to the key length in bits. Considered quantum-safe at 256-bit key lengths.

**Algorithm Weakness Score**  A 0–3 rating of how vulnerable a cryptographic algorithm is to quantum attack (Appendix D).

**AMS (Acquisition Management System)**  FAA lifecycle framework for planning, analyzing, acquiring, deploying, and sustaining systems. Six phases per FAA FAST policy: Service Analysis & Strategic Planning, Concept & Requirements Definition, Initial Investment Analysis, Final Investment Analysis, Solution Implementation, and In-Service Management. Disposal and service life extension are managed within In-Service Management rather than as a distinct phase. See Appendix G for PQC migration crosswalk.

**ATO (Authorization to Operate)**  Formal management decision authorizing an information system to operate at an acceptable level of residual risk (NIST SP 800-37 Rev 2). Typically three-year validity for federal systems, with continuous authorization models increasingly encouraged.

**Bridge Architecture**  Deployment pattern where the TLS termination point (e.g., BIG-IP) negotiates hybrid PQC on the front side and classical TLS to backends. Hardens the internet-facing leg first.

**CA/Browser Forum**  Industry consortium that sets baseline requirements for publicly trusted TLS certificates. Ballot SC-081v3 sets certificate validity shrinking to 47 days by 2029.

**CBOM (Cryptographic Bill of Materials)**  A structured inventory documenting every cryptographic algorithm, key, certificate, and protocol in use across an organization’s systems.

**CCOE (Cryptographic Center of Excellence)**  A cross-functional team (Chapter 6) responsible for steering the PQC migration across network, PKI, application, and governance domains.

**CNSA 2.0 (Commercial National Security Algorithm Suite 2.0)**  NSA’s updated algorithm guidance for National Security Systems. Specifies ML-KEM-1024 and ML-DSA-87. Full compliance required by 2030–2035.

**CNSSI 4009**  Committee on National Security Systems Instruction 4009, the CNSS Glossary. Authoritative source for federal information security terminology across U.S. National Security Systems.

**CRQC (Cryptographically Relevant Quantum Computer)**  A quantum computer powerful enough to run Shor’s algorithm against deployed cryptographic key sizes. Does not yet exist; timeline estimates range from 10–20+ years.

**CSfC (Commercial Solutions for Classified)**  NSA program that lets layered, properly configured commercial products protect classified data, as an alternative to NSA-developed Type 1 equipment. In the DoW PQC Strategy, CSfC is a primary path for fielding PQC commodity IT.

**Crypto-Agility**  The architectural capability to swap, update, or replace cryptographic algorithms without redesigning applications or protocols. A core design principle for PQC migration.

**Cryptographic Proxy Layer**  Structural term for the Bridge Architecture (Chapter 7): a dedicated enforcement point (TLS terminator, ADC, reverse proxy) that performs cryptographic upgrade on behalf of downstream systems that are not yet PQC-capable. Commonly used in federal and enterprise architecture documentation as a synonym for “bridge architecture.”

**DoW CIO PQC Directorate**  Department of War organization established by the November 18, 2025 DoW CIO memorandum *Preparing for Migration to Post Quantum Cryptography*. Issues two new authorizations every DoW Component must obtain before any PQC engagement: **cryptographic intake approval** (before testing, evaluating, piloting, investing in, or acquiring any PQC-enabling or PQC-related technology) and **cryptographic deployment approval** (before deployment, informed by NIST, NSA, and IC certification outcomes). These approvals layer on top of, not replace, FIPS 140-3, NIAP Common Criteria, and NSA CSfC. Led by Dr. Britta Hale. Chapter 4.

**DoW PQC Strategy**  Department of War *Post Quantum Cryptography Strategy*, signed April 1, 2026. Master execution document for the DoW transition. Sets five Lines of Effort and two acquisition tracks (High Assurance ECU and Commercial Solutions), and the department-wide deadlines: support PQC by December 31, 2030; use PQC by December 31, 2031; NSS support CNSA 2.0. Chapter 4.

**DoWIN (Department of War Information Network)**  The DoW’s enterprise network of IT systems, infrastructure, and services. Formerly the DoDIN. PQC migration of the DoWIN spans commodity IT, weapon systems, and edge devices.

**ECU (End Cryptographic Unit) / HA-ECU**  A device that performs the actual encryption or decryption at the end of a secure communications path. High Assurance ECUs (HA-ECUs) are NSA-certified and depend on the NSA Key Management Infrastructure (KMI); they form one of the two acquisition tracks in the DoW PQC Strategy.

**EO 14144 / EO 14306 / EO 14409**  U.S. Executive Orders shaping federal PQC policy. EO 14144 (Jan 2025) and EO 14306 (June 2025) direct agencies to inventory quantum-vulnerable systems and migrate; EO 14306 rescinded several prior orders but preserved PQC mandates. EO 14409 (June 2026, “Securing the Nation Against Advanced Cryptographic Attacks”) re-imposes hard deadlines: high-value assets use PQC for key establishment by 2030 and digital signatures by 2031, with a FAR rule requiring contractor FIPS/PQC compliance by 2030.

**FIPS 203 (ML-KEM)**  NIST standard for Module-Lattice-Based Key Encapsulation Mechanism. Replaces ECDH/DH for key exchange. Three parameter sets: ML-KEM-512/768/1024.

**FIPS 204 (ML-DSA)**  NIST standard for Module-Lattice-Based Digital Signature Algorithm. Replaces RSA/ECDSA for signatures. Three parameter sets: ML-DSA-44/65/87.

**FIPS 205 (SLH-DSA)**  NIST standard for Stateless Hash-Based Digital Signature Algorithm (formerly SPHINCS+). Conservative backup to ML-DSA, using only hash functions. Larger signatures.

**FIPS 206 (FN-DSA)**  NIST draft standard for FFT-over-NTRU-Lattice Digital Signature Algorithm (formerly Falcon). Compact 666-byte signatures at Level 1; complex floating-point implementation.

**FISMA (Federal Information Security Modernization Act)**  2014 law updating the 2002 Federal Information Security Management Act. Requires federal agencies to implement information security programs; mandates RMF compliance through OMB oversight.

**Grover’s Algorithm**  Quantum search algorithm that provides quadratic speedup against symmetric cryptography. Halves effective key strength: AES-128 → 64-bit equivalent. AES-256 remains safe.

**Harvest-Now, Decrypt-Later (HNDL)**  Attack strategy where adversaries capture encrypted traffic today for decryption by a future quantum computer. The primary driver of urgency for PQC key exchange migration.

**HQC (Hamming Quasi-Cyclic)**  Code-based backup KEM selected by NIST in March 2025. Provides algorithmic diversity from lattice-based ML-KEM. Standard expected ~2027.

**HSM (Hardware Security Module)**  Dedicated hardware device for secure key generation, storage, and cryptographic operations. PQC migration requires HSM firmware/hardware supporting ML-KEM/ML-DSA.

**Hybrid Mode**  Running a classical algorithm alongside a PQC algorithm so that the system is secure as long as at least one holds. Example: X25519MLKEM768 for TLS key exchange.

**IW10 / IW20**  TCP initial congestion window set to 10 or 20 segments. IW10 (≈14.6 KB) is the default; IW20 (≈29 KB) accommodates most PQC certificate chains in a single flight.

**KMI (Key Management Infrastructure)**  NSA system for generating, distributing, and managing keying material for High Assurance devices. The DoW PQC Strategy tasks NSA with adapting the KMI for PQC algorithms while scaling key production to Component needs.

**Merkle Tree Certificates (MTCs)**  Google/Cloudflare initiative replacing per-certificate PQC signatures with compact Merkle inclusion proofs. Reduces TLS authentication data from ~15 KB to ~736 bytes.

**ML-DSA (Module-Lattice Digital Signature Algorithm)**  See FIPS 204. The primary PQC signature algorithm. ML-DSA-65 is the general-purpose recommendation.

**ML-KEM (Module-Lattice Key Encapsulation Mechanism)**  See FIPS 203. The primary PQC key exchange algorithm. ML-KEM-768 is the general-purpose recommendation.

**mTLS (Mutual TLS)**  TLS configuration where both client and server authenticate with certificates. PQC doubles the certificate size overhead (both directions send PQC chains).

**NIST IR 8547**  NIST guidance on transitioning to PQC. Deprecates 112-bit classical algorithms after 2030; disallows all quantum-vulnerable public-key algorithms after 2035.

**NSM-10 (National Security Memorandum 10)**  2022 White House directive requiring federal agencies to migrate to PQC “as much as is feasible by 2035.”

**POA&M (Plan of Action and Milestones)**  Document identifying tasks needed to remediate known security weaknesses, milestones for completion, and resource requirements. Core output of the RMF Monitor step (NIST SP 800-37 Rev 2).

**PPK (Post-Quantum Pre-Shared Key)**  RFC 8784 mechanism for layering a quantum-resistant symmetric secret onto IKEv2 IPsec key derivation as an interim PQC measure.

**Q-Day**  The hypothetical date when a CRQC first breaks deployed public-key cryptography. Not a single event. Different algorithms may fall at different times.

**QKD (Quantum Key Distribution)**  Hardware-based key distribution using quantum physics. NSA, NCSC, ANSSI, and BSI recommend PQC over QKD for most use cases due to cost, range, and scalability limitations.

**RMF (Risk Management Framework)**  NIST SP 800-37 Rev 2 seven-step process (Prepare, Categorize, Select, Implement, Assess, Authorize, and Monitor) for managing security and privacy risk across federal information systems.

**SCRM (Supply Chain Risk Management)**  Discipline for identifying and mitigating risks introduced by suppliers, subcontractors, and third-party components (NIST SP 800-161 Rev 1). Extended in Chapter 9 to address PQC vendor readiness.

**Shor’s Algorithm**  Quantum algorithm that efficiently factors large integers and computes discrete logarithms, breaking RSA, ECDSA, ECDH, DH, and DSA.

**SSP (System Security Plan)**  Document describing how required security controls are implemented or planned for an information system (NIST SP 800-18, SP 800-37 Rev 2). Core component of the authorization package submitted for ATO.

**X25519MLKEM768**  The dominant hybrid TLS key exchange combining classical X25519 with ML-KEM-768. Client key share: 1,216 bytes. Specified in IETF draft-ietf-tls-ecdhe-mlkem.

### Appendix B
