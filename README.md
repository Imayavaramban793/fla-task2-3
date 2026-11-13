# Formal Language and Automata – Tasks 2 & 3

**Course:** 21CSC301T – Formal Language and Automata  
**Assignments:** CLA-2 Task 2 and Task 3

This repository combines two Formal Language and Automata assignments. Task 2 focuses on Deterministic Finite Automata (DFA) for input validation, while Task 3 explores Pushdown Automata (PDA), Context-Free Grammars (CFG), grammar ambiguity, and parsing techniques.

---

# TASK 2 – DFA INPUT VALIDATORS

## Objective

Design and implement Deterministic Finite Automata (DFA) to validate three real-world input formats:

1. **Indian Mobile Number:** Exactly 10 digits, starting with a digit between 6 and 9.
2. **Vehicle Registration Number:** 2 uppercase letters, 2 digits, 1–2 uppercase letters, followed by 4 digits (Example: TN45AB1234).
3. **24-Hour Time:** Valid HH:MM format ranging from 00:00 to 23:59.

Each character is mapped to a character class before processing. Missing transitions lead to an implicit trap state (qD).

These DFAs validate syntax only, not whether a mobile number is active or a vehicle is officially registered.

## Implementation

- Direct DFA construction for mobile number validation.
- Product construction (intersection) of two DFAs for mobile number validation.
- DFA construction for vehicle registration numbers.
- DFA construction for 24-hour time validation.
- DFA simulation with step-by-step execution traces.
- DFA minimisation using Moore's partition refinement algorithm.
- Independent validation using regular expressions.

## Results

| Validator | Accepted Format | States Built | Minimal States |
|---|---|---:|---:|
| Mobile Number | [6-9][0-9]{9} | 11 | 11 |
| Vehicle Plate | [A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4} | 11 | 11 |
| 24-Hour Time | 00:00–23:59 | 7 | 7 |

The mobile validator is implemented using both direct construction and product construction. Both produce the same 11-state minimal DFA.

## Files

- `dfa.py` – DFA simulation, trace generation, product construction and minimisation.
- `validators.py` – Three DFA input validators.
- `test_validators.py` – Automated testing against independent regular expressions.

## Execution

Run the following commands:

```bash
python test_validators.py

python validators.py mobile 9876543210

python validators.py plate TN45AB1234

python validators.py time 23:59
```

## Testing Results

The test suite checks valid inputs, invalid inputs, exhaustive strings over selected alphabets and randomly mutated valid strings.

**Total: 240,121 strings tested – ALL PASSED.**

---

# TASK 3 – PDA & CFG CASE STUDIES

## Objective

Explore languages that require stack-based memory and demonstrate the applications of Context-Free Grammars (CFG) and Pushdown Automata (PDA).

Three case studies are implemented.

## Case Study 1: Nested Markup Tags

**Concept:** Matching nested opening and closing tags.

- Opening symbols: `a`, `b`
- Closing symbols: `A`, `B`
- Every closing symbol must match the most recently opened corresponding symbol.
- The original grammar contains ambiguity due to the production `S → SS`.
- A revised grammar `S → TS | T` is introduced.
- A deterministic PDA uses a stack to validate properly nested tags.

Example:

```text
abBA  → ACCEPTED
abAB  → REJECTED
```

## Case Study 2: Boolean Search Filter Expressions

**Concept:** Parsing Boolean expressions using CFG and LL(1) parsing.

Supported operators:

- `|` – Logical OR
- `&` – Logical AND
- `!` – Logical NOT
- `( )` – Parentheses
- `x` – Boolean variable

The original grammar is ambiguous. A revised grammar separates expressions into three precedence levels:

- B – OR expressions
- T – AND expressions
- F – Negation, parenthesised expressions and variables

A recursive-descent LL(1) parser evaluates expressions while maintaining correct operator precedence.

Example:

```text
x|x&x
(x|x)&x
```

The revised grammar eliminates the ambiguity observed in the tested expressions.

## Case Study 3: Request and Acknowledgement Counting

**Language:** aⁿb²ⁿ

**Concept:** Each request requires exactly two acknowledgements.

- `a` represents a request.
- `b` represents an acknowledgement.
- For every `n` requests, exactly `2n` acknowledgements are required.
- The language is not regular.
- A deterministic PDA uses a stack to track the required acknowledgements.
- A CFG is also implemented:

```text
S → aSbb | abb
```

Example:

```text
abb       → ACCEPTED
aabbbb    → ACCEPTED
aaabbbbbb → ACCEPTED
```

## Implementation

- PDA simulator using instantaneous descriptions.
- Stack-based transition processing.
- Breadth-first search for PDA computations.
- PDA acceptance by final state or empty stack.
- CFG representation and production rules.
- Parse-tree generation and ambiguity detection.
- CFG-to-PDA conversion.
- Recursive-descent LL(1) Boolean expression parser.
- Independent checkers for all three case studies.

## Files

- `pda.py` – PDA simulator and execution trace generation.
- `cfg_tools.py` – CFG utilities, parse-tree counting and CFG-to-PDA conversion.
- `case_studies.py` – Three case studies, grammars, PDAs and Boolean parser.
- `test_case_studies.py` – Automated testing.
- `demo.py` – Demonstrations and sample execution traces.

## Execution

Run the following commands:

```bash
python test_case_studies.py

python demo.py
```

## Testing Results

**Nested Tags:**
- 274 balanced strings checked (length ≤ 8).
- Original grammar: 88 ambiguous strings.
- Revised grammar: 0 ambiguous strings.

**Boolean Expressions:**
- 80 valid strings checked (length ≤ 6).
- Original grammar: 34 ambiguous strings.
- Revised grammar: 0 ambiguous strings.
- 2,000 randomly generated expressions evaluated successfully against Python's Boolean evaluation.

**Request/Acknowledgement Language:**
- DPDA, CFG and CFG-to-PDA implementations agree with the independent checker.
- Exhaustive testing performed up to length 14.

**Overall Testing Result:**

- 176,132 exhaustive strings.
- 36 listed test cases.
- 2,000 random Boolean expressions.

**ALL TESTS PASSED.**

Note: Ambiguity counts are based on tested strings and do not constitute a general mathematical proof of unambiguity.

---

# PROJECT STRUCTURE

```text
Formal-Language-and-Automata/
│
├── dfa.py
├── validators.py
├── test_validators.py
│
├── pda.py
├── cfg_tools.py
├── case_studies.py
├── test_case_studies.py
├── demo.py
│
└── README.md
```

---

# TECHNOLOGIES USED

- Python 3
- Finite Automata (DFA)
- Pushdown Automata (PDA)
- Context-Free Grammars (CFG)
- Regular Expressions
- Moore's DFA Minimisation Algorithm
- Product Construction of DFAs
- LL(1) Parsing
- Breadth-First Search
- Automated Testing

---

# CONCEPTS DEMONSTRATED

1. Deterministic Finite Automata.
2. DFA simulation and state transitions.
3. Product construction and intersection of DFAs.
4. DFA minimisation.
5. Regular expression validation.
6. Context-Free Grammars.
7. Pushdown Automata and stack operations.
8. CFG-to-PDA conversion.
9. Parse-tree generation.
10. Grammar ambiguity and ambiguity reduction.
11. Deterministic PDA behaviour.
12. Recursive-descent LL(1) parsing.
13. Exhaustive and randomised testing.

---

# HOW TO RUN THE PROJECT

**Step 1:** Install Python 3.

**Step 2:** Clone the repository.

```bash
git clone <repository-url>
```

**Step 3:** Navigate to the project directory.

```bash
cd Formal-Language-and-Automata
```

**Step 4:** Run Task 2 tests.

```bash
python test_validators.py
```

**Step 5:** Run Task 3 tests.

```bash
python test_case_studies.py
```

**Step 6:** Execute the demonstration.

```bash
python demo.py
```

No third-party Python packages are required. The implementations use Python's standard library.

---

# CONCLUSION

This combined project demonstrates the practical implementation of Formal Language and Automata concepts through real-world input validation and stack-based language processing.

Task 2 demonstrates how DFAs can recognise structured input patterns, perform state transitions, and minimise automata efficiently.

Task 3 demonstrates how CFGs and PDAs handle nested structures, Boolean expressions, and non-regular languages requiring additional memory through stack operations.

Both assignments include independent testing, execution traces, and validation to demonstrate the correctness of the implemented automata and grammars.

**All implemented test suites completed successfully.**
