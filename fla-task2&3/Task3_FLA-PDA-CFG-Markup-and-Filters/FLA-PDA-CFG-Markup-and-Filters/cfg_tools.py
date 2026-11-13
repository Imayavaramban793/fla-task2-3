"""Context-free grammar tools: parse-tree counting/listing and CFG -> PDA conversion.

Grammars here have no epsilon rules. A symbol that is a key of `rules` is a non-terminal;
every other character is a terminal.  Right-hand sides are strings of single characters.
"""
from functools import lru_cache

from pda import PDA


class CFG:
    def __init__(self, start, rules):
        self.start, self.rules = start, rules

    def terminals(self):
        return sorted({c for rhss in self.rules.values() for r in rhss for c in r if c not in self.rules})

    def count_trees(self, s):
        n = len(s)
        if n == 0:
            return 0

        @lru_cache(None)
        def cnt(sym, i, j):
            if sym not in self.rules:
                return 1 if j - i == 1 and s[i] == sym else 0
            return sum(seq(r, i, j) for r in self.rules[sym])

        @lru_cache(None)
        def seq(rhs, i, j):
            if len(rhs) == 1:
                return cnt(rhs[0], i, j)
            total = 0
            for k in range(i + 1, j):
                a = cnt(rhs[0], i, k)
                if a:
                    total += a * seq(rhs[1:], k, j)
            return total

        return cnt(self.start, 0, n)

    def trees(self, s):
        """All parse trees as nested (symbol, children) tuples."""
        n = len(s)

        @lru_cache(None)
        def tr(sym, i, j):
            if sym not in self.rules:
                return [sym] if j - i == 1 and s[i] == sym else []
            out = []
            for r in self.rules[sym]:
                for kids in sq(r, i, j):
                    out.append((sym, kids))
            return out

        @lru_cache(None)
        def sq(rhs, i, j):
            if len(rhs) == 1:
                return [(t,) for t in tr(rhs[0], i, j)]
            out = []
            for k in range(i + 1, j):
                for a in tr(rhs[0], i, k):
                    for rest in sq(rhs[1:], k, j):
                        out.append((a,) + rest)
            return out

        return tr(self.start, 0, n) if n else []

    def accepts(self, s):
        return self.count_trees(s) > 0

    def to_pda(self):
        """Standard one-state construction, acceptance by empty stack (nondeterministic)."""
        delta = {}
        for A, rhss in self.rules.items():
            delta[("q", "", A)] = [("q", r) for r in rhss]
        for t in self.terminals():
            delta[("q", t, t)] = [("q", "")]
        return PDA(delta, "q", self.start, accept_by="empty")


def render(tree):
    if isinstance(tree, str):
        return tree
    sym, kids = tree
    return f"{sym}[{' '.join(render(k) for k in kids)}]"


def cfg_pda_prune(cfg):
    # no epsilon rules: every stack symbol needs at least one input symbol
    return len(cfg[2]) > len(cfg[1])
