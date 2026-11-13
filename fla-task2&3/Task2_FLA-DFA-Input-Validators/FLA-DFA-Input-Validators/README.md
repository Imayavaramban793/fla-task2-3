# FLA – DFA Input Validators: Mobile Number, Vehicle Plate, 24-hour Time

Course: 21CSC301T Formal Language and Automata (CLA-2, Task 2)

| Validator | Accepts | Classes | States built | Minimal |
|---|---|---|---|---|
| Mobile (India) | exactly 10 digits, first digit 6–9 | S (6–9), D (0–5) | 11 (direct) / 11 (product) | 11 |
| Vehicle plate | 2 letters, 2 digits, 1–2 letters, 4 digits (`TN45AB1234`) | L, D | 11 | 11 |
| 24-hour time | `HH:MM`, 00:00–23:59 | digits, `:` | 7 | 7 |

Each character is first mapped to a class; a missing transition goes to an implicit trap state `qD`. The DFAs check **syntax only**: whether a number is really in service or a plate is registered needs a database and is checked after the DFA accepts.

The mobile validator is built twice: directly, and as the **product (intersection)** of "length 10" and "first digit 6–9"; both give the same 11-state minimal DFA.

## Files
`dfa.py` simulation with trace, product, minimisation · `validators.py` the three machines · `test_validators.py`

## Run
```
python test_validators.py
python validators.py mobile 9876543210
python validators.py plate TN45AB1234
python validators.py time 23:59
```
## Testing
240 121 strings (listed cases, exhaustive small alphabets, random mutations of valid strings) compared against independent regular expressions for every DFA and every minimised DFA: no mismatch.

## When a DFA is not enough
Needs only bounded memory (counts up to a limit, which part of the string) → DFA. Needs outside data or unbounded counting (`as many 6s as 9s`, nested tags) → PDA / CFG (see the PDA-CFG repo).

## Output
Saved in the `output/` folder (`test_results.txt`, `sample_traces.txt`, `state_counts.txt`).
```
mobile    110584 strings, no mismatch
plate      51536 strings, no mismatch
time       78001 strings, no mismatch
states  mobile direct/product/minimal: 11 11 11
states  plate  built/minimal: 11 11
states  time   built/minimal: 7 7
TOTAL 240121 strings checked: ALL PASSED
```
Sample trace:
```
time on '23:60'
 1. d(q0, '2' -> 2) = q2
 2. d(q2, '3' -> 3) = q3
 3. d(q3, ':' -> :) = q4
 4. d(q4, '6' -> 6) = qD
 5. d(qD, '0' -> 0) = qD
 final state qD -> REJECTED
```
