# 허태혁 · Taehyeok Heo

학생

## Repositories

| Repository | What it is | |
|---|---|---|
| [**Research_paper**](https://github.com/heok0308hth-glitch/Research_paper) | 16 solo-authored papers (PDF + Markdown + reproduction certificates) across combinatorics, number theory, AI theory, game theory, and market microstructure | Python · Markdown |
| [**HJTK**](https://github.com/heok0308hth-glitch/HJTK) | Android assistant that installs no AI model: signs into Claude · ChatGPT · Gemini · Grok · DeepSeek and conducts them as a team — bidding, shared board, cross-checks, one-tap approval | Kotlin · Compose |
| [**Korean_voice**](https://github.com/heok0308hth-glitch/Korean_voice) | On-device Korean neural TTS and voice cloning (ONNX Runtime) — one-time model download, then fully offline | Android · ONNX |

## How I work

1. **Compute the small case exactly.** If the definition can be enumerated for
   `n ≤ 8`, enumerate it and publish the numbers.
2. **Verify every optimum twice.** A separate checker that follows the definition
   literally, plus a solver from a different family (SAT, MILP, brute force).
3. **Write down what broke.** Wrong claims are retracted in the paper, not
   quietly deleted. The retraction log is the most useful part of the document.
4. **Keep the effect off until a human taps.** In software, anything that leaves
   the device — mail, share, call, spend — waits behind an approval card.

## Selected papers

- **Burning graphs with heterogeneous thresholds** — the ignition profile
  `s_k(G, τ)` as a single function that contains classical burning, uniform
  `r`-burning, and target-set selection as slices; exact DP over
  (burned mask, rounds) with triple cross-validation.
- **A new lower bound R(5,24) ≥ 565** — a 564-vertex two-block cyclotomic witness,
  with `ω ≤ 4` proved by orbit reduction *and* a symmetry-free SAT encoding.
- **Costly questions, lying answers** — priced q-ary search under an adversarial
  lie budget, with the exact `c* log₂ n` sandwich at `e = 0` and its collapse at
  `e = 1`, measured by fault injection into the verifier itself.
- **Irreversible memory compression in a finite context window** — recursive
  summarization as a finite-state Markov chain over facts, giving a closed-form
  two-factor survival law (what the budget buys × what friction erases each pass)
  and a spending-unit cliff: a 4-bit per-item cap throws away 58% of a set that
  needs 4 bits per item, while the same 4 bits spent through an optimal code
  throws away nothing. Re-summarizing more often, keeping more, or enlarging the
  window cannot substitute for the other factor — each was rejected by
  simulation, not argued.
- **Reflexive order-book phase transitions under finite latency and discrete
  ticks** — the critical reflexivity gain `γ_c = N / (2 S₀ μ₀ T a σ² H)` in closed
  form, giving 0.368 against 0.349 measured (within 5%); the collapse is a jump,
  not a slide, with the depth ratio falling from 1.04 to 0.00 while `γ` moves by
  0.07–0.11, and its order is fixed by one measured elasticity (`ε_D = 0.784 < 1`).
  A circuit breaker fitted to the natural drawdown is exactly neutral, but with an
  anticipation channel at `L = 8` it makes the drawdown 19.9% worse — in all sixty
  paired runs.

## Contact

Issues and pull requests in any of the repositories above are the fastest way to
reach me. Corrections to the papers are genuinely welcome — especially a
counterexample to a stated bound.
