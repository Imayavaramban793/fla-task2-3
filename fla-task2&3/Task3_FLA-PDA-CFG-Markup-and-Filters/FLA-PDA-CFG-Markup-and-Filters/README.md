# FLA – PDA & CFG Case Study: Markup Tags, Boolean Filters, Request/Ack Counts

Course: 21CSC301T Formal Language and Automata (CLA-2, Task 3)

## Case studies
| Case | Language | Ambiguous original? | Fix | Deterministic? |
|---|---|---|---|---|
| Nested tags (`a/b` open, `A/B` close) | matching tags | yes, `S → SS` | `S → TS \| T` | yes (DPDA) |
| Boolean filter `x \| & ! ( )` | search/rule expressions | yes, `B → B\|B \| B&B` | levels `B / T / F` | CFG→PDA no, LL(1) parser yes |
| `aⁿ b²ⁿ` (n requests, 2 acks each) | not regular | no | – | yes (DPDA) |

## Files
`pda.py` PDA simulator (ID trace, determinism test) · `cfg_tools.py` parse-tree count/list, CFG→PDA · `case_studies.py` grammars, PDAs, LL(1) parser · `test_case_studies.py` · `demo.py`

## Run
```
python test_case_studies.py
python demo.py
```
## Measured results
- Tags: 274 balanced strings (length ≤ 8); 88 ambiguous in the original grammar, 0 in the revised one. `aAaAaA` has 2 trees, `aAaAaAaA` has 5.
- Boolean: 80 valid strings (length ≤ 6); 34 ambiguous in the original, 0 in the revised. With x = (T,F,F): `x|x&x` = True (precedence) but `(x|x)&x` = False, so ambiguity is a real bug.
- 2000 random expressions: LL(1) parser result equals Python's own `and/or/not` result.
- 176 132 exhaustive strings + 36 listed cases, all PDA / CFG / CFG→PDA / parser agree with independent checkers.
- Ambiguity of CFGs is undecidable in general: counting trees of short strings is evidence, not a proof.

## Output
Saved in the `output/` folder (`test_results.txt`, `demo_output.txt`).
```
tags   : 274 balanced strings (len<=8); ambiguous in original: 88, in revised: 0
tags   : e.g. aAaAaA trees (orig) = 2 | aAaAaAaA = 5
bool   : 80 valid strings (len<=6); ambiguous in original: 34, in revised: 0
bool   : 2000 random expressions evaluated = Python's own result
bool   : x|x&x with x=(T,F,F) -> True (precedence), vs (x|x)&x -> False
anb2n  : DPDA, CFG and CFG->PDA agree with a^n b^2n checker (len<=14)
TOTAL  176132 exhaustive strings + 36 listed cases + 2000 random: ALL PASSED
```
Demo:
```
== DPDA trace, nested tags ==
(s,abBA,Z) ⊢ (q1,bBA,aZ) ⊢ (q1,BA,baZ) ⊢ (q1,A,aZ) ⊢ (q1,ε,Z) ⊢ (q0,ε,Z)   ACCEPT
'abAB': REJECT (no computation reaches an accepting configuration)

== Ambiguity: x|x&x in the ORIGINAL boolean grammar ==
  B[B[x] | B[B[x] & B[x]]]
  B[B[B[x] | B[x]] & B[x]]
  trees in revised grammar: 1
  CFG->PDA (nondeterministic) explored 50 configurations, accept=True

== a^n b^2n DPDA ==
(p,aabbbb,Z) ⊢ (p,abbbb,XXZ) ⊢ (p,bbbb,XXXXZ) ⊢ (r,bbb,XXXZ) ⊢ (r,bb,XXZ) ⊢ (r,b,XZ) ⊢ (r,ε,Z) ⊢ (f,ε,Z)   ACCEPT
```
