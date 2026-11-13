"""Three real-time input validators built as DFAs.

1. Indian mobile number : exactly 10 digits, first digit 6-9
2. Vehicle number plate : e.g. TN45AB1234  (2 letters, 2 digits, 1-2 letters, 4 digits)
3. 24-hour time         : HH:MM, 00:00 .. 23:59

Usage:  python validators.py mobile 9876543210
        python validators.py plate TN45AB1234
        python validators.py time 23:59
"""
import sys
from dfa import DFA, product

DIGITS = "0123456789"


# ---------- 1. Mobile number (designed twice: direct and as a product) ----------
def _mobile_class(ch):
    if ch in "6789":
        return "S"       # strong first digit
    if ch in "012345":
        return "D"
    return None


def mobile_direct():
    delta = {("q0", "S"): "q1"}
    for i in range(1, 10):
        for c in "SD":
            delta[(f"q{i}", c)] = f"q{i + 1}"
    return DFA(delta, "q0", {"q10"}, _mobile_class, ["S", "D"])


def mobile_product():
    length10 = DFA({(i, c): i + 1 for i in range(10) for c in "SD"}, 0, {10}, _mobile_class, ["S", "D"])
    first_ok = DFA({("h0", "S"): "h1", ("h1", "S"): "h1", ("h1", "D"): "h1"},
                   "h0", {"h1"}, _mobile_class, ["S", "D"])
    return product(length10, first_ok)


# ---------- 2. Vehicle number plate ----------
def _plate_class(ch):
    if "A" <= ch <= "Z":
        return "L"
    if ch in DIGITS:
        return "D"
    return None


def plate():
    d = {("q0", "L"): "q1", ("q1", "L"): "q2", ("q2", "D"): "q3", ("q3", "D"): "q4",
         ("q4", "L"): "q5", ("q5", "L"): "q6", ("q5", "D"): "q7", ("q6", "D"): "q7",
         ("q7", "D"): "q8", ("q8", "D"): "q9", ("q9", "D"): "q10"}
    return DFA(d, "q0", {"q10"}, _plate_class, ["L", "D"])


# ---------- 3. 24-hour time ----------
def _time_class(ch):
    return ch if (ch in DIGITS or ch == ":") else None


def time24():
    d = {}
    for c in "01":
        d[("q0", c)] = "q1"
    d[("q0", "2")] = "q2"
    for c in DIGITS:
        d[("q1", c)] = "q3"
        d[("q5", c)] = "q6"
    for c in "0123":
        d[("q2", c)] = "q3"
    d[("q3", ":")] = "q4"
    for c in "012345":
        d[("q4", c)] = "q5"
    return DFA(d, "q0", {"q6"}, _time_class, list(DIGITS) + [":"])


BUILDERS = {"mobile": mobile_direct, "plate": plate, "time": time24}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in BUILDERS:
        print(__doc__)
        sys.exit(1)
    m = BUILDERS[sys.argv[1]]()
    print(m.format_trace(sys.argv[2], sys.argv[1]))
