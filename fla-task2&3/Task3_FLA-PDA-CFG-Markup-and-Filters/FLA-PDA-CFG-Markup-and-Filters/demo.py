from case_studies import *
from cfg_tools import render, cfg_pda_prune

print("== DPDA trace, nested tags ==")
print(tags_pda().format_trace("abBA"))
print(tags_pda().format_trace("abAB"))
print("\n== Ambiguity: x|x&x in the ORIGINAL boolean grammar ==")
for t in BOOL_ORIG.trees("x|x&x"):
    print(" ", render(t))
print("  trees in revised grammar:", BOOL_REV.count_trees("x|x&x"))
ok, _, explored = BOOL_REV.to_pda().run("x|x&x", cfg_pda_prune)
print(f"  CFG->PDA (nondeterministic) explored {explored} configurations, accept={ok}")
print("\n== a^n b^2n DPDA ==")
print(anb2n_pda().format_trace("aabbbb"))
