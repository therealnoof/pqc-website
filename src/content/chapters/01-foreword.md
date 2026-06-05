---
title: "Foreword"
displayTitle: "Foreword"
section: "Front Matter"
chapter: null
order: 1
words: 1586
readingMinutes: 7
excerpt: "A few years ago, I came across a TED talk presented by Quantum Physicist, Dr. Shohini Ghose. It had been many years since I last attended an academic course on anything physics much less quantum. During her talk she expl"
---

A few years ago, I came across a TED talk presented by Quantum Physicist, Dr. Shohini Ghose.<sup>1</sup> It had been many years since I last attended an academic course on anything physics much less quantum. During her talk she explained the concept of superposition and entanglement amongst other topics related to quantum mechanics. I had heard of these concepts in previous readings and academic studies, but I took notice considering the recent grumblings about a future world where quantum computers will break modern encryption.

Quantum physics is a weird spooky world. Particles and atoms behave differently in their sub-atomic world versus our classical macro world. Qubits, which are the unit of measure in quantum can exist in multiple states, and they can even share information with each other over vast distances.

It is these attributes that make Quantum so powerful. It has the power to transform medicine and find cures for diseases like Parkinson’s. It will impact energy and how we use power harvesting technology like batteries. It could even unlock new information about how the universe works and how humans form consciousness.

But what does all this quantum mechanics stuff have to do with cryptography and our networks? What is Q-day and why should we care?

My recent conversations with customers and colleagues around post quantum cryptography have led to this book. We hope to shed some light on the weird world of quantum and more importantly we hope to guide you on your post-quantum cryptography journey.

If you are curious about Quantum and need to know how to prepare for Q-day then this book is for you.

## The Clock We Can’t See

Somewhere in the world, there’s an adversary capturing your organization’s encrypted traffic right now. This information can’t be read today—that’s not currently possible. But they’re relying on the idea that within the next decade or so, a sufficiently powerful quantum computer will let them decrypt everything they’ve been patiently collecting. The security community calls this **Harvest Now, Decrypt Later (HNDL)**,<sup>2</sup> and it means the quantum threat isn’t a future problem. It’s a here today data exfiltration campaign with a delayed payoff.

The day a cryptographically relevant quantum computer (CRQC) becomes operational—also known as **“Q-Day”**—isn’t something we’ll see coming with a press release. It may happen in a university lab or maybe in a classified nation state bunker. It may be announced months or years after it becomes operational. The point is: we won’t know the day it happens. All we can do now is prepare our networks for a future with Quantum.

## The Mandates Are Already Here

If the HNDL argument feels too abstract, here’s the concrete version: the compliance clock is already ticking. NIST published the first three finalized post-quantum cryptography (PQC) standards in August 2024.<sup>3</sup> The NSA’s CNSA 2.0 requires all new National Security Systems acquisitions to support quantum-resistant algorithms by January 2027.<sup>4</sup> Federal agencies must submit PQC transition plans by April 2026.<sup>5</sup> The Quantum Computing Cybersecurity Preparedness Act—that’s federal law, not an executive order that can be rescinded—mandates ongoing cryptographic inventories and migration planning.<sup>6</sup>

This isn’t a “maybe someday” situation. If you sell to, partner with, or operate within the federal ecosystem, post-quantum cryptography is now a procurement, compliance, and architectural requirement. And the private sector won’t be far behind—the EU has already published its own PQC migration roadmap targeting critical infrastructure by 2030.<sup>7</sup>

## Why We Wrote This

We’ve spent years working with public sector customers—DoD, federal civilian, intelligence community, and state and local agencies—helping them architect, deploy, and secure some of the most complex network environments in the world. What we’ve learned is that the hardest part of any major technology transition isn’t the technology itself. It’s the gap between knowing something and then knowing how to act on it.

That gap is enormous in post-quantum cryptography right now. There’s no shortage of whitepapers explaining Shor’s algorithm or listing NIST’s new standards. What’s missing is a practical, pragmatic guide that answers the questions we hear in every customer conversation:

- “Okay, but where do I start?”

- “How do I even find all the cryptography in my environment?”

- “What breaks when I start changing things?”

- “How do I explain this to my leadership without losing them in the math?”

- “What’s required vs. what’s recommended vs. what’s actually possible right now?”

This field guide is our attempt to close that gap. We’ve pulled together the regulatory mandates, the technical details, the migration frameworks, and the operational reality into something you can hold in one hand and actually use.

> **A QUICK DISCLAIMER**
> Let’s address the elephant in the room. The primary author’s of this guide work for F5, Inc. F5 makes products that live in the middle of network traffic—load balancers, SSL/TLS terminators, application delivery controllers, API gateways—and some of those products are directly relevant to a PQC migration.
> We’re not going to pretend otherwise. But we made a deliberate choice when writing this book: **every chapter presents vendor-neutral guidance first.** Where F5 capabilities are relevant to a specific migration challenge, we’ll call them out—clearly labeled, never disguised as generic advice. If you work with a different vendor stack, this book should still be one of the most useful things on your desk. If you happen to use F5, you’ll get some bonus context on where those tools fit.
> Our credibility depends on your trust, and we’d rather you find this guide genuinely useful than feel like you got handed a sales pitch.

## What This Book Is (and Isn’t)

**This is** a practitioner’s field guide—concise, opinionated, and focused on getting you from “aware” to “acting.” It’s designed to be carried to meetings, marked up with sticky notes, and dog-eared at the chapters that matter to your role.

**This is not** a cryptography textbook. We’ll explain the algorithms and the math when it’s necessary to understand why something matters, but we won’t bury you in lattice theory. If you want a deep academic treatment, we’ll point you to excellent resources. Our job is to help you build a plan, make decisions, and start moving.

**This is not** an academic course on Quantum Mechanics. However, we will cover the basics because a firm understanding of why we are here is critical. We will cover core topics like Superposition and Entanglement. These topics will give you a firm understanding of what makes quantum so powerful and how it applies to cryptography.

Everything in this guide is grounded in primary sources: NIST standards, NSA guidance, CISA publications, IETF RFCs, and executive-level mandates. Every factual claim is cited. Where the landscape is uncertain or actively changing—and there’s a lot of that right now—we’ll tell you so.

## Notes

The following sources support specific claims made in the Foreword. Full bibliographic entries for all sources referenced throughout the book appear in the Bibliography at the end of this guide.

**1.**  Ghose, Shohini. “Quantum Computing Explained in 10 Minutes.” TED Talk. TED Conferences, 2018. Available at: https://www.ted.com/talks/shohini_ghose_a_beginner_s_guide_to_quantum_computing

**2.**  NSA Cybersecurity Advisory. “Quantum Computing and Post-Quantum Cryptography.” The “Harvest Now, Decrypt Later” threat model is widely referenced across NSA, CISA, and NIST guidance as a primary motivation for urgent PQC adoption. See also: CISA, “Post-Quantum Cryptography Initiative,” https://www.cisa.gov/quantum

**3.**  National Institute of Standards and Technology. FIPS 203: Module-Lattice-Based Key-Encapsulation Mechanism Standard; FIPS 204: Module-Lattice-Based Digital Signature Standard; FIPS 205: Stateless Hash-Based Digital Signature Standard. Published August 13, 2024. https://csrc.nist.gov/news/2024/postquantum-cryptography-fips-approved

**4.**  National Security Agency. “Commercial National Security Algorithm Suite 2.0 (CNSA 2.0) Algorithms.” PP-22-1338, Ver. 1.0, September 2022; updated FAQ Ver. 2.1, December 2024. CNSA 2.0 requires that all new NSS acquisitions support CNSA 2.0 algorithms by January 1, 2027. https://media.defense.gov/2025/May/30/2003728741/-1/-1/0/CSA_CNSA_2.0_ALGORITHMS.PDF

**5.**  The White House. National Security Memorandum on Promoting United States Leadership in Quantum Computing While Mitigating Risks to Vulnerable Cryptographic Systems (NSM-10), May 4, 2022. Office of Management and Budget Memorandum M-23-02, November 18, 2022, requires FCEB agencies to submit cryptographic system inventories and migration plans. The April 2026 milestone for transition plan submissions is derived from NSM-10 agency timelines.

**6.**  Quantum Computing Cybersecurity Preparedness Act, Pub. L. No. 117-349, signed December 21, 2022. Requires OMB to issue guidance on PQC migration, mandates agency cryptographic inventories, and requires annual progress reports to Congress. As federal statute, its requirements cannot be rescinded by executive order.

**7.**  NIS Cooperation Group. “Coordinated Implementation Roadmap for the Transition to Post-Quantum Cryptography.” Published early 2025. Recommends EU member states initiate national PQC transition strategies by end of 2026, transition critical infrastructure by 2030, and complete migration by 2035. In January 2026, the European Commission published a proposed directive amending NIS2 to include explicit PQC requirements.

Let’s get started. The quantum clock doesn’t pause for planning meetings.
