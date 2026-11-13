"""Compare every PDA / CFG / parser with independent checkers."""
import itertools
import random

from case_studies import *
from cfg_tools import cfg_pda_prune

random.seed(11)


def allstr(alpha, maxlen):
    for n in range(1, maxlen + 1):
        for t in itertools.product(alpha, repeat=n):
            yield "".join(t)


LISTED = {
    "tags": (["aA", "abBA", "aAbB", "aabBAA", "abBAaA", "bBaAbB"], ["", "a", "aB", "abAB", "aAA", "Aa", "abBAa"]),
    "bool": (["x", "x|x&x", "!x", "(x|x)&x", "!(x&x)|x", "((x))", "x&x&x"], ["", "x|", "|x", "xx", "(x|x", "x&|x", "!"]),
    "anb2n": (["abb", "aabbbb", "aaabbbbbb"], ["", "ab", "abbb", "aabbb", "bba", "aabbbbb"]),
}

n = 0
# --- case 1
orig_pda, rev_pda = TAGS_ORIG.to_pda(), TAGS_REV.to_pda()
dp = tags_pda()
assert dp.is_deterministic() and not orig_pda.is_deterministic()
amb_orig = amb_rev = total = 0
for s in allstr("abAB", 8):
    want = tags_checker(s)
    assert dp.accepts(s) == want, s
    assert TAGS_ORIG.accepts(s) == want and TAGS_REV.accepts(s) == want, s
    if len(s) <= 6:
        assert orig_pda.accepts(s, cfg_pda_prune) == want, s
    if want:
        total += 1
        amb_orig += TAGS_ORIG.count_trees(s) > 1
        amb_rev += TAGS_REV.count_trees(s) > 1
        assert TAGS_REV.count_trees(s) == 1
    n += 1
print(f"tags   : {total} balanced strings (len<=8); ambiguous in original: {amb_orig}, in revised: {amb_rev}")
print("tags   : e.g. aAaAaA trees (orig) =", TAGS_ORIG.count_trees("aAaAaA"), "| aAaAaAaA =", TAGS_ORIG.count_trees("aAaAaAaA"))
for s in LISTED["tags"][0]:
    assert dp.accepts(s)
for s in LISTED["tags"][1]:
    assert not dp.accepts(s)

# --- case 2
bo_pda, br_pda = BOOL_ORIG.to_pda(), BOOL_REV.to_pda()
assert not bo_pda.is_deterministic()
amb_o = amb_r = tot = 0
for s in allstr("x|&!()", 6):
    want = ll1_accepts(s)
    assert BOOL_ORIG.accepts(s) == want and BOOL_REV.accepts(s) == want, s
    if len(s) <= 5:
        assert bo_pda.accepts(s, cfg_pda_prune) == want and br_pda.accepts(s, cfg_pda_prune) == want, s
    if want:
        tot += 1
        amb_o += BOOL_ORIG.count_trees(s) > 1
        amb_r += BOOL_REV.count_trees(s) > 1
        assert BOOL_REV.count_trees(s) == 1
    n += 1
print(f"bool   : {tot} valid strings (len<=6); ambiguous in original: {amb_o}, in revised: {amb_r}")
for s in LISTED["bool"][0]:
    assert ll1_accepts(s) and BOOL_REV.accepts(s)
for s in LISTED["bool"][1]:
    assert not ll1_accepts(s)


def gen_b(d):
    if d == 0 or random.random() < 0.3:
        return "x"
    r = random.random()
    if r < 0.3:
        return gen_b(d - 1) + "|" + gen_b(d - 1)
    if r < 0.6:
        return gen_b(d - 1) + "&" + gen_b(d - 1)
    if r < 0.8:
        return "!(" + gen_b(d - 1) + ")"
    return "(" + gen_b(d - 1) + ")"


rnd = 0
for _ in range(2000):
    s = gen_b(4)
    k = s.count("x")
    vals = [random.random() < 0.5 for _ in range(k)]
    it = iter(vals)
    py = "".join(str(next(it)) if c == "x" else {"|": " or ", "&": " and ", "!": " not "}.get(c, c) for c in s)
    assert ll1_eval(s, vals) == eval(py), (s, vals)
    rnd += 1
print(f"bool   : {rnd} random expressions evaluated = Python's own result")
print("bool   : x|x&x with x=(T,F,F) ->", ll1_eval("x|x&x", [True, False, False]), "(precedence), vs (x|x)&x ->", ll1_eval("(x|x)&x", [True, False, False]))

# --- case 3
ap, ag = anb2n_pda(), ANB2N.to_pda()
assert ap.is_deterministic() and not ag.is_deterministic()
for s in allstr("ab", 14):
    want = anb2n_checker(s)
    assert ap.accepts(s) == want and ANB2N.accepts(s) == want, s
    if len(s) <= 12:
        assert ag.accepts(s, cfg_pda_prune) == want, s
    if want:
        assert ANB2N.count_trees(s) == 1
    n += 1
for s in LISTED["anb2n"][0]:
    assert ap.accepts(s)
for s in LISTED["anb2n"][1]:
    assert not ap.accepts(s)
print("anb2n  : DPDA, CFG and CFG->PDA agree with a^n b^2n checker (len<=14)")
listed = sum(len(a) + len(b) for a, b in LISTED.values())
print(f"TOTAL  {n} exhaustive strings + {listed} listed cases + {rnd} random: ALL PASSED")
