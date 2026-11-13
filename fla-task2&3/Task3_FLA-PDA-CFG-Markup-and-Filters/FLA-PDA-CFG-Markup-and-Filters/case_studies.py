"""Three case studies: nested markup tags, boolean search filters, request/acknowledgement counts.

Case 1  Nested tags     open a,b  close A,B   (a mini HTML/XML checker)
Case 2  Boolean filter  x | & ! ( )           (search-filter / rule engine expression)
Case 3  a^n b^(2n)      n requests, each needing two acknowledgements
"""
from cfg_tools import CFG
from pda import PDA

# ---------------- Case 1: nested tags ----------------
TAGS_ORIG = CFG("S", {"S": ["SS", "aSA", "bSB", "aA", "bB"]})            # ambiguous
TAGS_REV = CFG("S", {"S": ["TS", "T"], "T": ["aSA", "bSB", "aA", "bB"]})  # unambiguous


def tags_pda():
    d = {}
    for q in ("s", "q0"):                      # s = start (not accepting), q0 = all closed
        d[(q, "a", "Z")] = [("q1", "aZ")]
        d[(q, "b", "Z")] = [("q1", "bZ")]
    for x in "ab":
        d[("q1", "a", x)] = [("q1", "a" + x)]
        d[("q1", "b", x)] = [("q1", "b" + x)]
    d[("q1", "A", "a")] = [("q1", "")]
    d[("q1", "B", "b")] = [("q1", "")]
    d[("q1", "", "Z")] = [("q0", "Z")]
    return PDA(d, "s", "Z", finals={"q0"})


def tags_checker(s):
    """Independent plain-stack checker."""
    st = []
    for ch in s:
        if ch in "ab":
            st.append(ch)
        elif ch in "AB" and st and st[-1] == ch.lower():
            st.pop()
        else:
            return False
    return bool(s) and not st


# ---------------- Case 2: boolean filter ----------------
BOOL_ORIG = CFG("B", {"B": ["B|B", "B&B", "!B", "(B)", "x"]})                       # ambiguous
BOOL_REV = CFG("B", {"B": ["B|T", "T"], "T": ["T&F", "F"], "F": ["!F", "(B)", "x"]})  # unambiguous


def ll1_eval(s, values=None):
    """Recursive-descent parser for  B -> T('|'T)*, T -> F('&'F)*, F -> '!'F | '(' B ')' | 'x'.
    Returns the truth value (k-th 'x' takes values[k], default True) or raises SyntaxError."""
    pos = 0
    vals = iter(values) if values is not None else None

    def peek():
        return s[pos] if pos < len(s) else None

    def eat(c):
        nonlocal pos
        if peek() != c:
            raise SyntaxError(f"expected {c!r} at {pos}")
        pos += 1

    def B():
        v = T()
        while peek() == "|":
            eat("|")
            r = T()
            v = v or r
        return v

    def T():
        v = F()
        while peek() == "&":
            eat("&")
            r = F()
            v = v and r
        return v

    def F():
        c = peek()
        if c == "!":
            eat("!")
            return not F()
        if c == "(":
            eat("(")
            v = B()
            eat(")")
            return v
        if c == "x":
            eat("x")
            return True if vals is None else next(vals)
        raise SyntaxError(f"unexpected {c!r} at {pos}")

    v = B()
    if pos != len(s):
        raise SyntaxError("trailing input")
    return v


def ll1_accepts(s):
    try:
        ll1_eval(s)
        return True
    except (SyntaxError, StopIteration):
        return False


# ---------------- Case 3: a^n b^(2n) ----------------
ANB2N = CFG("S", {"S": ["aSbb", "abb"]})


def anb2n_pda():
    d = {("p", "a", "Z"): [("p", "XXZ")], ("p", "a", "X"): [("p", "XXX")],
         ("p", "b", "X"): [("r", "")], ("r", "b", "X"): [("r", "")],
         ("r", "", "Z"): [("f", "Z")]}
    return PDA(d, "p", "Z", finals={"f"})


def anb2n_checker(s):
    n = s.count("a")
    return n >= 1 and s == "a" * n + "b" * (2 * n)
