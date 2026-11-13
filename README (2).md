# Formal Language and Automata – Tasks 2 & 3

**Course:** 21CSC301T – Formal Language and Automata  
**Assignments:** CLA-2 Task 2 (DFA Input Validators) and CLA-2 Task 3 (PDA & CFG Case Studies)

This repository combines two Formal Language and Automata assignments. Task 2 demonstrates Deterministic Finite Automata (DFAs) for validating structured inputs. Task 3 explores Context-Free Grammars (CFGs), Pushdown Automata (PDAs), ambiguity, and deterministic parsing through three case studies.

---

## Task 2 – DFA Input Validators

### Objective
Design and implement DFAs to validate three common input formats:

1. **Indian mobile number:** exactly 10 digits, with the first digit between 6 and 9.
2. **Vehicle registration number:** 2 uppercase letters, 2 digits, 1–2 uppercase letters, followed by 4 digits (for example, `TN45AB1234`).
3. **24-hour time:** `HH:MM` format, covering values from `00:00` to `23:59`.

Each input character is mapped to a character class before the DFA processes it. Missing transitions lead to an implicit trap state (`qD`). These validators check the **syntax/format** of the input only; they do not verify whether a mobile number is active or whether a vehicle registration is present in a government database.

### DFA implementation
- The mobile-number validator is implemented in two ways:
  - Direct DFA construction.
  - Product construction (intersection) of a length-10 DFA and a DFA that checks the first digit.
- The vehicle-plate validator checks the required letter/digit sequence.
- The time validator checks both the `HH:MM` structure and valid 24-hour ranges.
- DFA simulation supports step-by-step traces.
- Moore partition refinement is used to minimise the automata.

### Task 2 results

| Validator | Accepted format | States built | Minimal states |
|---|---|---:|---:|
| Indian mobile number | `[6-9][0-9]{9}` | 11 | 11 |
| Vehicle plate | `[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}` | 11 | 11 |
| 24-hour time | `00:00`–`23:59` in `HH:MM` format | 7 | 7 |

The mobile validator's direct and product constructions produce the same 11-state minimal DFA.

### Run Task 2
```bash
python test_validators.py
python validators.py mobile 9876543210
python validators.py plate TN45AB1234
python validators.py time 23:59
```

The test suite compares each DFA and its minimised version against independent regular expressions. It checks listed valid and invalid examples, exhaustive strings over selected small alphabets, and randomly mutated valid strings.

**Recorded result:** 240,121 strings checked across the three validators; all passed with no mismatch.

---

## Task 3 – PDA and CFG Case Studies

### Objective
Explore languages that require stack-based memory and demonstrate how CFGs and PDAs can model them. The assignment contains three case studies.

### Case studies

#### 1. Nested markup tags
- Opening symbols: `a`, `b`
- Closing symbols: `A`, `B`
- Each closing symbol must match the most recently opened corresponding symbol.
- The original CFG is ambiguous because it includes the production `S → SS`.
- A revised grammar, `S → TS | T`, removes the ambiguity observed in the tested strings.
- A deterministic PDA (DPDA) uses a stack to check properly nested and matching tags.

#### 2. Boolean search-filter expressions
- Supported symbols: `x`, `|`, `&`, `!`, `(`, `)`.
- The original grammar is ambiguous.
- The revised grammar separates the expression into precedence levels:
  - `B` – OR expressions
  - `T` – AND expressions
  - `F` – negation, parenthesised expressions, or `x`
- A recursive-descent LL(1) parser evaluates expressions while respecting operator precedence.
- The CFG-to-PDA construction is nondeterministic; the LL(1) parser provides deterministic parsing.

#### 3. Request and acknowledgement counts: `aⁿb²ⁿ`
- Each request (`a`) requires exactly two acknowledgements (`b`).
- The language has the form `aⁿb²ⁿ`, where `n ≥ 1`.
- It is not a regular language.
- A DPDA uses its stack to track the required acknowledgements.
- A CFG is also provided: `S → aSbb | abb`.

### Task 3 implementation
- PDA simulator using instantaneous descriptions: `(state, remaining input, stack)`.
- Breadth-first search explores possible PDA computations.
- PDA acceptance can be based on a final state or an empty stack.
- CFG utilities count and list parse trees and convert a CFG into a PDA.
- Case-study implementations include PDA constructions, grammars, independent checkers, and an LL(1) Boolean-expression parser.
- Demo output shows PDA traces and examples of grammar ambiguity.

### Run Task 3
```bash
python test_case_studies.py
python demo.py
```

### Task 3 recorded results
- **Nested tags:** 274 balanced strings of length up to 8 were checked. The original grammar had 88 ambiguous strings; the revised grammar had 0.
- **Boolean expressions:** 80 valid strings of length up to 6 were checked. The original grammar had 34 ambiguous strings; the revised grammar had 0. The LL(1) parser also matched Python's Boolean evaluation for 2,000 generated expressions.
- **`aⁿb²ⁿ`:** DPDA, CFG, and CFG-to-PDA results agreed with the independent checker for exhaustive strings up to length 14.
- **Overall:** 176,132 exhaustive strings, 36 listed test cases, and 2,000 random Boolean expressions were checked; all passed.

The ambiguity counts are results for the tested strings. They are experimental evidence and are not a general proof that a CFG is unambiguous.

---

## Project Structure

```text
.
├── dfa.py                  # DFA simulator, trace formatting, product construction, minimisation
├── validators.py           # Mobile, vehicle-plate, and time DFA builders
├── test_validators.py      # Tests DFA validators against regular expressions
├── pda.py                  # PDA simulator and trace formatting
├── cfg_tools.py            # CFG utilities, parse trees, CFG-to-PDA conversion
├── case_studies.py         # Three CFG/PDA case studies and Boolean LL(1) parser
├── test_case_studies.py    # Tests for Task 3 case studies
├── demo.py                 # Demonstrations and sample traces
└── README.md               # Combined documentation for Tasks 2 and 3
```

Use the filenames shown in the project structure when organising the combined repository. If your downloaded files currently have suffixes such as `(1)` or `(2)`, rename them to the canonical filenames above before running the commands.

---

## Concepts Demonstrated

- Deterministic Finite Automata (DFA)
- Character-class mapping and trap states
- Product construction (intersection) of DFAs
- DFA simulation and state minimisation
- Regular expressions as independent validators
- Context-Free Grammars (CFG)
- Pushdown Automata (PDA) and stack operations
- CFG-to-PDA conversion
- Parse-tree generation and grammar ambiguity
- Deterministic PDA behaviour
- Recursive-descent LL(1) parsing and operator precedence
- Exhaustive, example-based, and randomised testing

---

## Requirements

- Python 3
- No third-party packages are required by the provided Python source files; the implementations use Python's standard library.

## Run All Tests

```bash
python test_validators.py
python test_case_studies.py
```

Both test scripts should complete successfully when the project files are placed together using the filenames listed above.
