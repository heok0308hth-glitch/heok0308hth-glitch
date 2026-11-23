# 허태혁 · Taehyeok Heo

**Independent researcher and Android developer.** I write papers that end in a
number I can defend, and Android apps that keep working when the network, the
process, or the model does not.

Working independently, without a cluster, on two things:

- **Computational mathematics and AI theory.** Graph burning, Ramsey bounds,
  costly search with lies, generalized Collatz dynamics, and the failure modes of
  self-verifying and multi-agent reasoning systems. Every claim comes with an
  exact certificate, an independent re-simulation, or an explicit retraction —
  all fourteen papers carry a "Limits" section, and some carry a "Claims I
  withdrew" section.
- **Deterministic Android tooling.** HJTK turns a typed request into an auditable
  plan with an approval gate and a hash-chained journal, using zero on-device
  models.

## Repositories

| Repository | What it is | |
|---|---|---|
| [**Research_paper**](https://github.com/heok0308hth-glitch/Research_paper) | 14 solo-authored papers (PDF + Markdown + reproduction certificates) across combinatorics, number theory, AI theory, and game theory | Python · Markdown |
| [**HJTK**](https://github.com/heok0308hth-glitch/HJTK) | Zero-LLM Android AI orchestration: typed plans, approval gates, crash-safe journal, 64 built-in commands, 116 tests | Kotlin · Compose |
| [**Korean_voice**](https://github.com/heok0308hth-glitch/Korean_voice) | On-device Korean neural TTS and voice cloning on ONNX Runtime — no cloud, no account | Android · ONNX |

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
  with `ω ≤ 4` proved by orbit reduction *and* an symmetry-free SAT encoding.
- **Costly questions, lying answers** — priced q-ary search under an adversarial
  lie budget, with the exact `c* log₂ n` sandwich at `e = 0` and its collapse at
  `e = 1`, measured by fault injection into the verifier itself.

## Contact

Issues and pull requests in any of the repositories above are the fastest way to
reach me. Corrections to the papers are genuinely welcome — especially a
counterexample to a stated bound.
