---
title: "The Quantum Threat: Why This Matters Now"
displayTitle: "Chapter 1: The Quantum Threat: Why This Matters Now"
section: "Chapters"
chapter: 1
order: 4
words: 7125
readingMinutes: 32
excerpt: "Before we can understand why post-quantum cryptography matters, we need to understand the strange and beautiful science that makes it necessary. This chapter is a guided tour—from the birth of quantum mechanics over a ce"
---

Before we can understand why post-quantum cryptography matters, we need to understand the strange and beautiful science that makes it necessary. This chapter is a guided tour—from the birth of quantum mechanics over a century ago, through the core concepts that make quantum computing so powerful, to the specific moment where that power threatens every encrypted system on the planet.

We promise to keep the math and complexity to a minimum. But some of these ideas are genuinely weird and understanding why they’re weird is essential to understanding what we’re up against. So, hang in there it’s about to get a little nerdy. Grab a cup of coffee and let’s go.

## A Brief History of Quantum Mechanics

The story of quantum mechanics begins, like many great scientific stories, with a problem nobody could solve.

In 1900, German physicist Max Planck was wrestling with a puzzle called the “blackbody radiation problem”—the question of why hot objects glow certain colors at certain temperatures. Classical physics predicted that a hot object should radiate infinite energy at short wavelengths, which clearly didn’t match reality. In what he later described as “an act of desperation,” Planck proposed a radical idea: energy isn’t emitted in a continuous stream. Instead, it comes in discrete packets—tiny, indivisible bundles that he called quanta.<sup>1</sup>

Planck didn’t fully appreciate what he’d done. It fell to a 26-year-old patent clerk named Albert Einstein to take the next leap. In 1905—the same year he published the theory of special relativity—Einstein proposed that light itself exists as particles (later called photons), not just waves. This was heresy. Maxwell’s equations had convinced the physics world that light was a wave phenomenon. Einstein was saying it was both.<sup>2</sup>

In 1913, the Danish physicist Niels Bohr took quantum ideas and applied them to the atom. His model proposed that electrons orbit the nucleus in fixed, quantized energy levels—and that they can “jump” between these levels by absorbing or emitting photons. Bohr’s model accurately predicted the spectral lines of hydrogen, lending real credibility to quantum ideas.<sup>3</sup>

Then, in 1924, French physicist Louis de Broglie proposed something even stranger: if light (a wave) can behave like a particle, then particles—like electrons—should also behave like waves.<sup>4</sup> This idea of wave-particle duality was confirmed experimentally and opened the door to the modern quantum revolution.

The floodgates opened in 1925–1927. Werner Heisenberg developed matrix mechanics, Erwin Schrödinger developed wave mechanics (and the famous equation bearing his name), and Max Born provided the probabilistic interpretation of the wave function—the idea that quantum mechanics doesn’t tell us where a particle is, but rather the probability of finding it in any given place.<sup>5</sup>

In 1927, Heisenberg published his uncertainty principle: you cannot simultaneously know both the exact position and the exact momentum of a particle. This isn’t a measurement limitation—it’s a fundamental property of nature.<sup>6</sup>

These discoveries shook the foundations of physics. Einstein himself was deeply uncomfortable with the probabilistic nature of quantum mechanics, famously objecting: “God does not play dice with the universe.” But experiment after experiment confirmed that at the subatomic level, the universe does exactly that.<sup>7</sup>

> **PLAIN-LANGUAGE SIDEBAR**
> Think of quantum mechanics as the operating system of reality at the smallest scales. Just as your computer’s behavior is governed by code you never see, every atom in the universe follows quantum rules—rules that are fundamentally different from the physics we experience in everyday life. The key insight: at the quantum level, things aren’t certain. They’re probabilistic.

## Superposition: Being Everything at Once

Of all the strange concepts in quantum mechanics, **superposition** is the one that most directly enables quantum computing—and most directly threatens our cryptographic systems.

In our classical, everyday world, things have definite states. A light switch is either on or off. A coin on a table is either heads or tails. But in the quantum world, a particle can exist in multiple states simultaneously until it is measured. An electron doesn’t have to spin “up” or “down”—it can be in a superposition of both at the same time.

This isn’t a metaphor. It’s not that we don’t know the state and it could be either one. The particle genuinely exists in both states at once, described by a mathematical wave function that encodes the probability of each possible outcome. Only when we measure the particle does this superposition “collapse” into a definite result. More on the “measure” in a moment.

![figure](/book-media/img-01.png)

*Figure 1.1 — Classical Bit vs. Quantum Bit (Qubit)*

### Schrödinger’s Cat: A Thought Experiment

In 1935, Erwin Schrödinger devised a famous thought experiment to illustrate just how strange superposition is when scaled up.<sup>8</sup> Imagine a cat sealed in a box with a vial of poison, a radioactive atom, and a Geiger counter. If the atom decays (a quantum event), the Geiger counter triggers, breaks the vial, and the cat dies. If the atom doesn’t decay, the cat lives.

According to quantum mechanics, until someone opens the box and observes the result, the radioactive atom is in a superposition of “decayed” and “not decayed.” And since the cat’s fate is tied to that atom, the cat is—in a quantum mechanical sense—both alive and dead simultaneously.

Schrödinger intended this as a reductio ad absurdum—a way to show how absurd quantum mechanics becomes at macroscopic scales. But the math works. The cat’s superposition is real within the formalism, even if we never observe it in practice because large objects interact with their environment and “decohere” almost instantly. Think about this for a moment. We have all heard the phrase “if a tree falls in a forest and no one is there to see it, did it really fall?” In our classical world, our logical thinking says yes, the tree fell, just because no one was there to “measure or observe” it falling doesn’t mean it didn’t happen. Well in the quantum world this is not the case. The tree exists in both states until measured. Seems ridiculous I know, but this is how things work in the quantum world. More on measure or observer effect in a bit.

For quantum computing, superposition is not a paradox—it’s a feature. A quantum bit (qubit) in superposition can represent 0 and 1 at the same time, combine this with entanglement and you suddenly reach exponential compute. This is what gives quantum computers their extraordinary potential power.

## Entanglement: Spooky Action at a Distance

If superposition is strange, **entanglement** is downright out of science fiction.

In 1935, Einstein, Boris Podolsky, and Nathan Rosen published a paper (known as the EPR paradox) arguing that quantum mechanics must be incomplete.<sup>9</sup> Their thought experiment showed that two particles could be prepared in a way that measuring one would instantly determine the state of the other—no matter how far apart they were. Einstein called this “spukhafte Fernwirkung”: spooky action at a distance.

Here’s how it works: two particles interact and become “entangled.” Their quantum states are now correlated. Separate them by inches or by light-years—it doesn’t matter. Measure the spin of particle A and you will instantly know the spin of particle B, because their states are linked. Distance has no bearing on the relationship…spooky…indeed.

![figure](/book-media/img-02.png)

*Figure 1.2 — Quantum Entanglement*

This doesn’t violate Einstein’s speed-of-light limit (you can’t use it to send information faster than light), but it reveals that entangled particles share information in a way that has no classical analogue. When Irish physicist John Bell proposed a test in 1964—and experiments by Alain Aspect and others confirmed it in the 1980s—the physics community had to accept that entanglement is real.<sup>10</sup>

For quantum computing, entanglement is the secret sauce. It allows qubits to be correlated in ways that classical bits cannot, enabling quantum algorithms to explore vast solution spaces simultaneously. Combined with superposition, entanglement is what makes a quantum computer fundamentally more powerful than a classical one for certain problems.

## The Observer Effect: Measurement Changes Reality

One of the most counterintuitive aspects of quantum mechanics is the role of observation itself.

In the classical world, you can measure something without changing it. You can look at a thermometer or read a speedometer and the thing being measured doesn’t care. But in the quantum world, the act of measurement **fundamentally alters the system being observed**.

When a particle is in superposition and you measure it, the wave function “collapses”—the particle snaps into one definite state. Before measurement: all possibilities exist. After measurement: only one reality remains. This is sometimes called the observer effect or the “measurement problem,” and it sits at the heart of every interpretation of quantum mechanics.

The most dramatic demonstration is the now famous **double-slit experiment**. Fire electrons one at a time at a barrier with two slits and a detector screen behind it. Without observation, the electrons produce an interference pattern—as if each electron passed through both slits simultaneously as a wave. But place a detector at the slits to observe which path the electron takes, and the interference pattern vanishes. The electron behaves like a particle going through one slit or the other.<sup>11</sup> It’s as if the particles “know” they are being watched!

The mere act of looking changes the outcome. For our purposes, this has a practical implication: quantum states are fragile. This fragility is both a challenge for building quantum computers (qubits are notoriously difficult to keep stable) and a feature of quantum cryptography (any attempt to eavesdrop on a quantum communication channel disturbs the signal and is detectable).

## Quantum in the Wild: Nature Got There First

You might think quantum effects are limited to laboratory conditions near absolute zero. Nature disagrees.

One of the most fascinating discoveries of the past two decades is that **photosynthesis**—the process by which plants convert sunlight into chemical energy—may exploit quantum mechanics to achieve its remarkable efficiency.<sup>12</sup>

Here’s the puzzle: when a photon of sunlight hits a chlorophyll molecule in a plant leaf, it dislodges an electron, creating an “exciton” (a paired electron-hole that acts like a tiny battery). This exciton must travel through a maze of molecular structures to reach the reaction center where photosynthesis actually happens. Classical physics would predict a random walk—the exciton bouncing from molecule to molecule like a pinball until it stumbles upon the right destination. That random process would be slow and inefficient, most of the energy would be lossed.

But photosynthesis operates at near-perfect quantum efficiency—virtually every photon captured is converted to usable energy. In 2007, researchers at UC Berkeley led by Graham Fleming observed something remarkable in the Fenna-Matthews-Olson (FMO) photosynthetic complex of green sulfur bacteria: the exciton wasn’t hopping randomly. It was moving as a quantum wave, exploring multiple pathways simultaneously through quantum coherence—then collapsing along the most efficient route.<sup>13</sup>

> **PLAIN-LANGUAGE SIDEBAR**
> Think of it this way: a classical exciton is like a lost tourist wandering city streets, trying random turns until they find their hotel. A quantum exciton is like that same tourist existing on every street at once, then instantly appearing at the hotel via the shortest path. Nature figured out quantum computing long before we did.

The scientific community continues to debate the exact role of quantum effects in photosynthesis—some recent studies suggest that molecular vibrations, rather than purely electronic quantum coherence, may explain the observed efficiency.<sup>14</sup> But the broader point stands: quantum phenomena operate in warm, wet, noisy biological systems, not just in pristine laboratory conditions. Researchers have also found evidence of quantum effects in bird navigation (the “quantum compass” used by European robins), enzyme catalysis, and even the human sense of smell.<sup>15</sup>

Why does this matter for a book about cryptography? Because it demonstrates that quantum mechanics isn’t abstract theory trapped in a physics journal. It’s an operational reality—one that engineers are learning to harness for computing, and one that will inevitably transform the security landscape.

## From Physics to Computing: The Qubit

A classical computer stores information in **bits**—binary digits that are either 0 or 1. Every computation, from loading a webpage to encrypting a file, is ultimately a sequence of operations on billions of these binary values.

A quantum computer replaces bits with **qubits** (quantum bits). Thanks to superposition, a single qubit can represent 0, 1, or both simultaneously. And when you entangle multiple qubits, their combined state space grows exponentially. Two entangled qubits can represent 4 states simultaneously (2<sup>2</sup>). Three qubits: 8 states (2<sup>3</sup>). Ten qubits: 1,024 states. Three hundred qubits can represent more states than there are atoms in the observable universe (2<sup>300</sup>).<sup>16</sup> That’s right…more atoms than the observable universe contains.

This isn’t just more computing power—it’s a fundamentally different kind of computing power. A quantum computer doesn’t just try answers faster. It can explore an enormous number of possibilities at once, using interference to amplify correct answers and cancel out wrong ones. For certain types of problems, this approach is exponentially more efficient than anything a classical computer can do.

The key phrase is “certain types of problems.” Quantum computers won’t replace your laptop. They’re not faster at Excel or email. But for specific mathematical problems—including the ones that underpin modern encryption—they are supremely effective.

![figure](/book-media/img-03.png)

*Figure 1.3 — How Shor’s Algorithm Breaks RSA*

### The Qubit Reality Check: Physical vs. Logical

Before we go further, we need to address an important distinction that trips up even experienced technologists: not all qubits are created equal.

The qubits we’ve been describing—the ones that can exist in superposition and become entangled—are **physical qubits**. These are the actual hardware: superconducting circuits cooled to near absolute zero, trapped ions held in electromagnetic fields, photons routed through optical networks, or any of the other physical systems being explored today. The problem with physical qubits is that they are extraordinarily fragile. They are susceptible to environmental noise, thermal fluctuations, and electromagnetic interference. A stray vibration or a slight temperature change can cause a qubit to lose its quantum state—a phenomenon called decoherence. And when a qubit decoheres, it introduces errors into the computation.

This is where **logical qubits** come in. A logical qubit is an error-corrected qubit—a single, reliable computational unit built from many physical qubits working together. The additional physical qubits act as a safety net, continuously detecting and correcting errors in real time through a process called **quantum error correction (QEC)**. Think of it like RAID in storage: you use redundancy to protect against failure.<sup>16</sup>

The overhead is staggering. Depending on the error rate of the underlying hardware and the error correction scheme used (the most common today is the surface code), you might need **1,000 to 10,000 physical qubits to create a single reliable logical qubit.** This is why quantum computing resource estimates are often expressed in physical qubit counts—they represent the total hardware required, including all the error correction overhead.

> **PLAIN-LANGUAGE SIDEBAR**
> When a vendor announces a “1,000-qubit processor,” they’re talking about physical qubits—the raw hardware. After error correction, that 1,000-qubit chip might yield just one or two usable logical qubits. It’s the logical qubits that perform the meaningful computation. Shor’s algorithm needs roughly 4,000–6,000 logical qubits to factor RSA-2048. When researchers say you need “20 million physical qubits” for that job, the vast majority of those qubits are dedicated to error correction—keeping those few thousand logical qubits stable long enough to finish the calculation.

This is both good news and bad news. The good news: we’re a long way from having enough stable logical qubits to threaten real-world encryption. The bad news: error correction techniques are improving rapidly, physical qubit quality is increasing, and alternative error correction codes (such as quantum LDPC codes) promise to dramatically reduce the overhead ratio.<sup>16</sup> The distance between where we are and where an adversary needs to be is shrinking from both directions—better hardware and better algorithms.

## How Modern Encryption Actually Works

Before we can understand what quantum computing breaks, we need to understand what it’s breaking. Let’s talk about the mathematical trick that secures nearly everything on the internet.

### The Trapdoor: Easy One Way, Impossible the Other

Modern public-key cryptography is built on a concept mathematicians call a **trapdoor function**—a mathematical operation that is easy to perform in one direction but practically impossible to reverse without a secret key.<sup>17</sup>

Here’s the simplest example. Take two large prime numbers—let’s call them p and q—and multiply them together to get a product N. A fourth grader can multiply two numbers together, and a computer can do it in microseconds, even when those primes are hundreds of digits long. But now try going backward: given only N (the product), figure out which two primes were multiplied to create it. That’s the trapdoor. Multiplication is easy. Factoring is extraordinarily hard.

> **PLAIN-LANGUAGE SIDEBAR**
> Think of it like mixing paint. If someone hands you a can of yellow paint and a can of blue paint, you can mix them into green in seconds. But if someone hands you a can of green paint and says “tell me the exact shades of yellow and blue that were mixed to make this,” you’re in trouble. That’s the trapdoor: easy to combine, practically impossible to decompose.

RSA, the most widely deployed public-key algorithm in history, depends on exactly this asymmetry.<sup>18</sup> When you generate an RSA key pair, you pick two huge random prime numbers (each typically 1,024 bits long—roughly 300 digits), multiply them together, and publish the result as your **public key**. Anyone can use that public key to encrypt a message to you. But only someone who knows the original two primes—your **private key**—can decrypt it.

Elliptic Curve Cryptography (ECC) and Diffie-Hellman key exchange work on different mathematical structures (elliptic curves and discrete logarithms, respectively), but they share the same fundamental design principle: there’s a mathematical operation that’s trivially easy in one direction and computationally infeasible to reverse.

### Why Classical Computers Can’t Break the Lock

To factor a 2048-bit RSA key, a classical computer would need to find the two prime factors of a number that is 617 digits long. The best known classical factoring algorithm (the General Number Field Sieve) would require approximately 2<sup>112</sup> operations for this key size.<sup>19</sup> To put that in perspective: if you harnessed every classical computer on Earth and ran them until the sun burned out, you still wouldn’t come close.

This isn’t a guess or an approximation—it’s a mathematical wall. Classical computers can only test potential factors one at a time (or a few at a time with parallelism), and the number of possibilities grows exponentially with key size. The entire security model of the modern internet rests on this simple bet: **no classical computer will ever be powerful enough to reverse the trapdoor.**

For over 40 years, that bet has held. RSA was published in 1977. The largest RSA key ever factored by a classical computer is RSA-250 (829 bits), and it took a distributed computing effort spanning years. RSA-2048 is in an entirely different league.

## The Algorithms That Break Our Locks

### Shor’s Algorithm: The Lock Pick That Changes Everything

In 1994, mathematician Peter Shor published a paper that fundamentally changed the security landscape—even though the hardware to execute his idea didn’t exist yet.<sup>20</sup> He proved that a quantum computer, using the unique properties of superposition and entanglement, could factor large numbers exponentially faster than any known classical algorithm. The trapdoor—the one-way function that the entire internet depends on—suddenly had a back door.

Here’s how it works, in plain language:

Remember that a classical computer trying to factor a large number is essentially guessing and checking—trying one potential factor after another, sequentially. A 2048-bit RSA key has a solution space so vast that a classical machine could search it for billions of years without success.

Shor’s algorithm takes a completely different approach. Rather than trying to find the factors directly, it converts the factoring problem into a **period-finding problem**—a question about repeating patterns in a mathematical function. This is the key insight: finding the period (the repeating cycle) of a specific modular arithmetic function reveals information that can be used to calculate the prime factors.<sup>21</sup>

Why does this matter? Because **quantum computers are exceptionally good at finding periods.** This is where superposition becomes a weapon. A quantum computer can prepare a massive superposition of all possible inputs simultaneously—not testing them one by one, but evaluating them all at once. Through a process called the Quantum Fourier Transform, the computer then uses interference to amplify the periodic patterns and suppress everything else. The correct period rises to the surface like a signal emerging from noise.

Once you have the period, extracting the prime factors is straightforward classical math—a few lines of algebra. The quantum computer doesn’t do the factoring. It finds the hidden pattern that makes factoring trivially easy.

> **PLAIN-LANGUAGE SIDEBAR**
> Imagine you’re trying to crack a combination lock with a billion possible combinations. A classical computer tries them one at a time: 000-000-001, 000-000-002, and so on. It’ll be at this for a while.
> A quantum computer doesn’t try combinations at all. Instead, it does something like shaking the lock in a very specific way and listening for resonance. The quantum properties of superposition let it test all billion combinations simultaneously, and interference makes the correct answer ring louder than the wrong ones. It’s not brute force. It’s a fundamentally different strategy that only works because of quantum mechanics.

Shor’s algorithm doesn’t just work on RSA. It also solves the **discrete logarithm problem** and the **elliptic curve discrete logarithm problem**—the mathematical foundations of Diffie-Hellman key exchange, DSA, ECDSA, and ECDH. Every major public-key algorithm deployed today relies on a trapdoor that Shor’s algorithm can reverse. When a sufficiently powerful quantum computer runs Shor’s algorithm, the entire public-key infrastructure collapses simultaneously.

### How Close Are We? The Numbers Keep Dropping

Shor’s algorithm itself needs only a few thousand logical qubits to factor RSA-2048—roughly 4,000 to 6,000, depending on the implementation.<sup>22</sup> But as we discussed earlier, each logical qubit requires thousands of physical qubits for error correction. That’s why the total hardware estimates are so large.

In 2021, researchers Craig Gidney and Martin Ekerå estimated that breaking RSA-2048 would require approximately **20 million physical qubits** (supporting roughly 6,150 logical qubits with surface code error correction) operating for about 8 hours.<sup>23</sup> In 2025, Gidney published a further optimization—leveraging innovations in approximate arithmetic, more efficient qubit storage, and a technique called magic state cultivation—that reduced the estimate to **fewer than 1 million physical qubits** over roughly one week.<sup>24</sup> That’s a 20x reduction in hardware requirements in just four years, using the same underlying hardware assumptions.

These numbers matter because they define the finish line for adversaries. While no quantum computer exists today with this capacity, the trajectory is clear: multiple hardware vendors have published roadmaps targeting millions of physical qubits by the early 2030s. And as we’ve seen, progress comes from two fronts simultaneously—better physical hardware and smarter algorithms that reduce how many qubits you need in the first place.

> **⚠  MANDATE ALERT**
> Shor’s algorithm doesn’t just threaten RSA. It breaks every public-key cryptosystem based on integer factorization, discrete logarithms, or elliptic curve discrete logarithms. This includes RSA, DSA, ECDSA, ECDH, and DH—the foundational algorithms of TLS, IPsec, SSH, S/MIME, code signing, and certificate-based authentication. When a CRQC arrives, all of these are compromised simultaneously.

### The Solution Is Changing the Math

Here’s the critical insight that sets up the rest of this book: **the problem isn’t with encryption itself. The problem is with the specific mathematical problems we chose as our trapdoors.**

Factoring large numbers and computing discrete logarithms happen to be problems that quantum computers solve efficiently. But there are other mathematical problems—problems based on lattice geometry, error-correcting codes, hash functions, and other structures—that we have no reason to believe quantum computers can solve any faster than classical ones.

That’s what post-quantum cryptography (PQC) is: replacing the math. We keep the concept of public-key encryption—the idea of trapdoor functions, key pairs, digital signatures—but we swap the underlying mathematical problem for one that resists both classical and quantum attack. The new NIST standards (ML-KEM, ML-DSA, SLH-DSA, which we’ll cover in Chapter 3) are built on exactly these quantum-resistant mathematical foundations.

The protocols stay the same. TLS still does a handshake. IPsec still builds a tunnel. SSH still authenticates. But inside those protocols, the algorithms that generate keys, exchange secrets, and sign data are being swapped for new ones—ones where the trapdoor holds even against a quantum adversary. That migration—changing the math inside the protocols you already run—is the operational challenge this book is designed to help you navigate.

### Grover’s Algorithm: The Other Half of the Equation

Shor’s algorithm targets public-key (asymmetric) cryptography—the trapdoor math that protects key exchange and digital signatures. But asymmetric crypto is only half the story. To understand the second quantum threat, we need to understand how asymmetric and **symmetric** encryption work together—because in practice, they’re inseparable.

### Why Symmetric Encryption Matters: The Workhorse You Don’t See

Here’s something that surprises many people: **public-key encryption doesn’t actually protect your data.** Not directly. It’s too slow for that. Encrypting a large file or a video stream with RSA would be orders of magnitude slower than using a symmetric algorithm like AES. Public-key crypto exists to solve one specific problem: how do two parties who’ve never met securely agree on a shared secret key?

Once that shared secret is established, **symmetric encryption** takes over and does the actual work. Symmetric algorithms like AES (Advanced Encryption Standard) use the same key for both encryption and decryption. They’re fast, efficient, and handle the bulk encryption of every email, file transfer, web session, VPN tunnel, and database connection on the planet.

The relationship between asymmetric and symmetric encryption is like a diplomatic courier and a secure phone line. The courier (asymmetric crypto) makes a dangerous trip across enemy territory to deliver a codebook. Once the codebook is delivered, the two parties use it to have fast, secure conversations over the phone (symmetric crypto). The courier’s job is brief but critical; the phone line does the heavy lifting.

### How This Plays Out in TLS: A Session in Two Acts

Let’s walk through what actually happens when your browser connects to a website over HTTPS, because this is where both types of cryptography meet—and where both quantum threats apply.

**Act 1: The Handshake (Asymmetric).** When a TLS session begins, the client and server perform a handshake. In modern TLS 1.3, this uses an algorithm like **ECDHE** (Elliptic Curve Diffie-Hellman Ephemeral) to agree on a shared secret. The server also presents a digital certificate signed with an algorithm like **ECDSA** or **RSA** so the client can verify it’s talking to the right server and not an impostor. This handshake phase is where Shor’s algorithm strikes—it can break ECDHE, ECDSA, and RSA, allowing an attacker to either impersonate the server or recover the shared secret.

**Act 2: Bulk Encryption (Symmetric).** Once the handshake is complete and both sides have the shared secret, they derive symmetric session keys and switch to **AES-256-GCM** (or a similar symmetric cipher) for all subsequent data transfer. Every byte of actual content—HTML pages, API responses, file uploads, credentials—is encrypted with AES using the session keys from Act 1. This is the workhorse phase, and it’s where Grover’s algorithm applies.

> **PLAIN-LANGUAGE SIDEBAR**
> Think of a TLS session as a two-step process:
> Step 1 (the handshake): Public-key crypto securely delivers the key. This is the part Shor’s breaks.
> Step 2 (the data transfer): Symmetric crypto uses that key to encrypt everything. This is the part Grover’s weakens.
> If an attacker breaks Step 1, they get the key—and Step 2 is useless because the attacker can now decrypt everything with the stolen key. This is why Shor’s is the existential threat. But even if Step 1 is quantum-safe, Step 2 needs to be strong enough to resist Grover’s on its own. Both halves matter.

### What Grover’s Algorithm Actually Does

In 1996, Lov Grover published an algorithm for searching unsorted databases quadratically faster than any classical approach.<sup>25</sup> While this doesn’t sound as dramatic as Shor’s exponential speedup, the impact on symmetric cryptography is straightforward and significant.

Classically, if you want to brute-force an AES-256 key, you need to try up to 2<sup>256</sup> possible keys—a number so large it would take every computer on Earth longer than the age of the universe. Grover’s algorithm lets a quantum computer search that same key space in only the square root of the number of attempts. That means AES-256’s effective security strength drops from 2<sup>256</sup> to 2<sup>128</sup> operations. AES-128 drops to 2<sup>64</sup>—which begins to enter the range of a feasible attack.

Grover’s also impacts **hash functions**—the algorithms (like SHA-256) used for digital fingerprinting, certificate validation, password storage, and blockchain integrity. A hash function’s security against collision and preimage attacks is similarly halved by Grover’s. SHA-256 drops from 256-bit security to 128-bit equivalent.

### The Practical Takeaway: Upgrade, Don’t Panic

Unlike Shor’s algorithm, which completely obliterates public-key crypto, Grover’s merely weakens symmetric crypto—and the fix is simple: **double the key size.**

- **AES-256 → drops to 128-bit effective security.** Still computationally infeasible to break. AES-256 remains quantum-safe for any foreseeable future.

- **AES-128 → drops to 64-bit effective security.** Potentially vulnerable. Should be upgraded to AES-256.

- **SHA-256 → drops to 128-bit collision resistance.** Still practically secure for most applications.

- **3DES, Blowfish, and other legacy symmetric ciphers** with key sizes under 128 bits become unacceptable.

The message is reassuring but clear: Shor’s algorithm is the existential crisis. Grover’s algorithm is a maintenance upgrade. But that maintenance upgrade needs to happen—and for organizations still running AES-128 or SHA-1 in production environments (and you’d be surprised how many are), Grover’s adds genuine urgency to a cleanup that should have happened years ago.

## Q-Day: When Theory Becomes Threat

The security community uses the term **“Q-Day”** to describe the moment a cryptographically relevant quantum computer (CRQC) becomes operational—a machine powerful enough to run Shor’s algorithm against real-world encryption keys.

When will Q-Day arrive? Honest answer: nobody knows for certain. Here’s what we do know:

- As of early 2026, the largest quantum processors have roughly 1,000–1,200 physical qubits (e.g., IBM’s Condor at 1,121 qubits, Google’s Willow at 105 high-quality logical qubits). Breaking RSA-2048 requires roughly 1 million to 20 million physical qubits or roughly 4000-6000 logical qubits, depending on architecture.

- Multiple vendors—IBM, Google, Quantinuum, PsiQuantum, Microsoft—have published roadmaps targeting systems with hundreds of thousands to millions of qubits by the early 2030s.

- Algorithmic improvements continue to reduce the hardware threshold. Gidney’s 2025 paper cut the required qubits by 20x compared to the 2021 estimate.<sup>24</sup>

- Error correction remains the critical bottleneck. Today’s qubits are noisy; thousands of physical qubits are needed to create one reliable logical qubit.

Most expert assessments place Q-Day somewhere between 2030 and 2045, with significant uncertainty.<sup>26</sup> But the exact date is less important than a simple fact: **cryptographic migration takes 10–15 years for large organizations.** If Q-Day arrives in 2035 and you haven’t started migrating, you’re already too late.

> **⚠  MANDATE ALERT**
> Industry Q-Day estimates have shortened materially since this book was first drafted. On March 25, 2026, Google’s VP of Security Engineering announced an internal target to migrate all Google infrastructure to PQC by **2029**, citing faster-than-expected progress on quantum hardware, error correction, and factoring resource estimates. Cloudflare followed within days with a matching 2029 timeline. Scott Aaronson—historically the field’s most prominent skeptic of overheated quantum claims—wrote in May 2026 that quantum-hardware and error-correction researchers he trusts now believe a fault-tolerant machine capable of breaking deployed cryptography “ought to be possible by around 2029.” None of these are formal Q-Day announcements, but when the most cautious voices and the largest internet-scale infrastructure providers converge on a single year, the planning assumption shifts. Don’t anchor your migration on 2035.<sup>28</sup>

## Harvest Now, Decrypt Later: A Present-Tense Threat

There’s a reason this chapter is called “The Quantum Threat” and not “The Quantum Future.” The threat is already here.

The strategy is called **Harvest Now, Decrypt Later (HNDL)**, and it works like this: an adversary captures encrypted data today—intercepting TLS sessions, VPN tunnels, classified communications, financial transactions, healthcare records—and stores it. The adversary can’t read the data now. But when a CRQC becomes available, they can retroactively decrypt everything they’ve collected.<sup>27</sup>

For data with a long sensitivity lifetime—classified intelligence, trade secrets, medical records, attorney-client communications, strategic military plans—HNDL means the clock started ticking the moment the data was transmitted. If your organization sent encrypted data over the wire in 2020 and a CRQC appears in 2035, that 2020 data is compromised.

HNDL transforms the quantum threat from a speculative future risk into a present-day data exfiltration campaign with a delayed decryption payoff. It’s the reason NSA, CISA, and NIST have all emphasized that migration to post-quantum cryptography must begin now—not when Q-Day arrives, but years before it.

## What’s Next

Now that we understand the quantum mechanics, the computing power, and the specific threat algorithms, a natural question emerges: what exactly is at risk?

In Chapter 2, we’ll map out precisely which cryptographic algorithms are vulnerable to quantum attack, which ones are safe, and how to classify your organization’s data and systems by quantum risk level. That inventory is the foundation of everything that follows.

## Notes

The following sources support specific claims made in Chapter 1. Full bibliographic entries appear in the Bibliography.

**1.**  Planck, Max. “Über das Gesetz der Energieverteilung im Normalspektrum.” Annalen der Physik 309 (1901): 553–563. Planck introduced the concept of energy quanta to resolve the blackbody radiation problem.

**2.**  Einstein, Albert. “Über einen die Erzeugung und Verwandlung des Lichtes betreffenden heuristischen Gesichtspunkt.” Annalen der Physik 322, no. 6 (1905): 132–148. This paper proposed the photon hypothesis and is one of Einstein’s three revolutionary 1905 papers.

**3.**  Bohr, Niels. “On the Constitution of Atoms and Molecules.” Philosophical Magazine 26 (1913): 1–25. Bohr’s atomic model introduced quantized electron orbits.

**4.**  de Broglie, Louis. “Recherches sur la théorie des quanta.” PhD thesis, University of Paris, 1924. Proposed wave-particle duality for matter.

**5.**  For the development of matrix mechanics: Heisenberg, W. “Über quantentheoretische Umdeutung kinematischer und mechanischer Beziehungen.” Zeitschrift für Physik 33 (1925): 879–893. For wave mechanics: Schrödinger, E. “Quantisierung als Eigenwertproblem.” Annalen der Physik (1926). For the probabilistic interpretation: Born, M. “Zur Quantenmechanik der Stoßvorgänge.” Zeitschrift für Physik 37 (1926): 863–867.

**6.**  Heisenberg, Werner. “Über den anschaulichen Inhalt der quantentheoretischen Kinematik und Mechanik.” Zeitschrift für Physik 43 (1927): 172–198. Introduces the uncertainty principle.

**7.**  Pais, Abraham. “Suttle is the Lord: The Science and the Life of Albert Einstein.” Oxford University Press, 1982. Documents Einstein’s philosophical objections to quantum mechanics.

**8.**  Schrödinger, Erwin. “Die gegenwärtige Situation in der Quantenmechanik.” Naturwissenschaften 23 (1935): 807–812, 823–828, 844–849. Introduces the cat thought experiment.

**9.**  Einstein, A., Podolsky, B., and Rosen, N. “Can Quantum-Mechanical Description of Physical Reality Be Considered Complete?” Physical Review 47, no. 10 (1935): 777–780. The EPR paradox paper.

**10.**  Bell, J.S. “On the Einstein Podolsky Rosen Paradox.” Physics 1, no. 3 (1964): 195–200. Aspect, A., Dalibard, J., and Roger, G. “Experimental Realization of Einstein-Podolsky-Rosen-Bohm Gedankenexperiment: A New Violation of Bell’s Inequalities.” Physical Review Letters 49 (1982): 1804–1807. Confirmed entanglement experimentally.

**11.**  The double-slit experiment has been demonstrated many times since Thomas Young’s original 1801 light experiment. A landmark electron version: Tonomura, A., et al. “Demonstration of single-electron buildup of an interference pattern.” American Journal of Physics 57 (1989): 117–120.

**12.**  Engel, G.S., et al. “Evidence for wavelike energy transfer through quantum coherence in photosynthetic systems.” Nature 446 (2007): 782–786. The landmark paper reporting quantum coherence in photosynthesis.

**13.**  Panitchayangkoon, G., et al. “Long-lived quantum coherence in photosynthetic complexes at physiological temperature.” Proceedings of the National Academy of Sciences 107, no. 29 (2010): 12766–12770.

**14.**  Cao, J., et al. “Quantum biology revisited.” Science Advances 6, no. 14 (2020). This review argues that while quantum effects are present in photosynthesis, long-lived interexciton coherences may not be functionally significant; molecular vibrations and environment-assisted transport may better explain efficiency.

**15.**  Lambert, N., et al. “Quantum biology.” Nature Physics 9 (2013): 10–18. Reviews quantum effects in photosynthesis, avian magnetoreception, enzyme catalysis, and olfaction.

**16.**  Nielsen, Michael A. and Chuang, Isaac L. “Quantum Computation and Quantum Information.” Cambridge University Press, 10th Anniversary Edition (2010). The standard reference for quantum computing fundamentals.

**17.**  Trapdoor functions are formally defined in: Diffie, Whitfield and Hellman, Martin. “New Directions in Cryptography.” IEEE Transactions on Information Theory 22, no. 6 (1976): 644–654. This landmark paper introduced the concept of public-key cryptography and one-way trapdoor functions.

**18.**  Rivest, R.L., Shamir, A., and Adleman, L. “A Method for Obtaining Digital Signatures and Public-Key Cryptosystems.” Communications of the ACM 21, no. 2 (1978): 120–126. The RSA algorithm paper.

**19.**  For RSA-2048 classical factoring difficulty, see: Lenstra, Arjen K. “Key Lengths.” The Handbook of Information Security (2004). The General Number Field Sieve (GNFS) is the best known classical factoring algorithm. NIST SP 800-57 Part 1 Rev. 5 estimates RSA-2048 at approximately 112-bit classical security strength.

**20.**  Shor, Peter W. “Algorithms for Quantum Computation: Discrete Logarithms and Factoring.” Proceedings of the 35th Annual Symposium on Foundations of Computer Science (1994): 124–134.

**21.**  Shor’s algorithm converts integer factoring into period-finding via modular exponentiation. For an accessible explanation: Mermin, N. David. “Quantum Computer Science: An Introduction.” Cambridge University Press (2007), Chapter 3. For the original formulation: Shor (1994), ibid.

**22.**  For logical qubit estimates for Shor’s algorithm: Gidney and Ekerå (2021) use roughly 3n logical qubits for an n-bit RSA key, yielding approximately 6,150 logical qubits for RSA-2048. Beauregard’s space-optimized circuit requires 2n+3 logical qubits (≈4,099 for RSA-2048). Chevignard et al. (2024) reduced this to approximately 0.85n (≈1,730 logical qubits) at the cost of significantly more operations. Physical qubit overhead depends on error correction scheme and hardware error rates.

**23.**  Gidney, Craig and Ekerå, Martin. “How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits.” Quantum 5 (2021): 433. Assumes superconducting qubits on a square grid with 0.1% gate error rate and surface code error correction.

**24.**  Gidney, Craig. “Factoring integers with sublinear resources on a superconducting quantum processor.” arXiv:2505.15917 (May 2025). Reduces RSA-2048 factoring estimate to fewer than 1 million physical qubits in approximately one week, using approximate residue arithmetic, yoked surface codes, and magic state cultivation.

**25.**  Grover, Lov K. “A fast quantum mechanical algorithm for database search.” Proceedings of the 28th Annual ACM Symposium on Theory of Computing (1996): 212–219.

**26.**  Estimates vary widely. The Global Risk Institute publishes annual assessments; Mosca and Piani (2022) estimated a 50% chance of a CRQC by 2031–2033. The Chinese Academy of Sciences projects RSA-2048 vulnerability beyond 2045 under current models. A 2025 MITRE analysis suggests RSA-2048 could remain secure until 2055–2060 absent major breakthroughs.

**27.**  The HNDL threat model is referenced across NSA, CISA, and NIST guidance. See: CISA, “Post-Quantum Cryptography Initiative,” https://www.cisa.gov/quantum. Also: NSA Cybersecurity Advisory, “Quantum Computing and Post-Quantum Cryptography” (2022).

**28.**  Heather Adkins (VP, Security Engineering, Google), “Quantum Frontiers May Be Closer Than They Appear,” blog.google, March 25, 2026. Google announced an internal target to migrate all infrastructure to PQC by 2029. Cloudflare followed with a matching 2029 timeline within the same week. Underlying technical drivers cited include the Google Quantum AI ECDLP-256 resource estimate (approximately 20× fewer physical qubits than prior estimates) and continued reductions in Gidney’s RSA-2048 factoring estimates beyond his May 2025 sublinear-resources paper. Note: Android 17 (June 2026) integrates PQC digital signatures using ML-DSA at the OS hardware root of trust. See also: Scott Aaronson, “Will You Heed My Warnings?” Shtetl-Optimized, May 2026, citing senior quantum-hardware and error-correction researchers projecting a fault-tolerant CRQC capable of breaking deployed cryptography by approximately 2029.

Next: Chapter 2 — What’s Vulnerable and What’s Not
