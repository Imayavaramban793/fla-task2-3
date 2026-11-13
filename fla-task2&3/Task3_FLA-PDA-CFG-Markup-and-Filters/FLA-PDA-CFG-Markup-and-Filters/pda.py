"""Pushdown automaton simulator over instantaneous descriptions (state, rest of input, stack).

delta: {(state, symbol_or_'', stack_top): [(new_state, push_string), ...]}
The stack is a string whose FIRST character is the top; push_string replaces the popped top.
"""
from collections import deque


def fmt(cfg):
    q, rest, stack = cfg
    return f"({q},{rest or 'ε'},{stack or 'ε'})"


class PDA:
    def __init__(self, delta, start, start_stack, finals=(), accept_by="final"):
        self.delta, self.start, self.start_stack = delta, start, start_stack
        self.finals, self.accept_by = set(finals), accept_by

    def moves(self, cfg):
        q, rest, stack = cfg
        if not stack:
            return
        top = stack[0]
        if rest:
            for q2, push in self.delta.get((q, rest[0], top), []):
                yield (q2, rest[1:], push + stack[1:])
        for q2, push in self.delta.get((q, "", top), []):
            yield (q2, rest, push + stack[1:])

    def is_accepting(self, cfg):
        q, rest, stack = cfg
        if rest:
            return False
        return q in self.finals if self.accept_by == "final" else stack == ""

    def run(self, text, prune=None):
        """Breadth-first search of all computations. Returns (accepted, trace, explored)."""
        if prune is None:
            limit = 2 * len(text) + 3
            prune = lambda c: len(c[2]) > limit
        start = (self.start, text, self.start_stack)
        parent, dq, explored = {start: None}, deque([start]), 0
        while dq:
            cfg = dq.popleft()
            explored += 1
            if self.is_accepting(cfg):
                path = []
                while cfg is not None:
                    path.append(cfg)
                    cfg = parent[cfg]
                return True, path[::-1], explored
            for nxt in self.moves(cfg):
                if nxt not in parent and not prune(nxt):
                    parent[nxt] = cfg
                    dq.append(nxt)
        return False, [], explored

    def accepts(self, text, prune=None):
        return self.run(text, prune)[0]

    def is_deterministic(self):
        by_top = {}
        for (q, a, t), targets in self.delta.items():
            if len(targets) > 1:
                return False
            by_top.setdefault((q, t), set()).add(a)
        # an epsilon-move must not compete with an input move
        return all(not ("" in s and len(s) > 1) for s in by_top.values())

    def format_trace(self, text):
        ok, path, _ = self.run(text)
        if not ok:
            return f"{text!r}: REJECT (no computation reaches an accepting configuration)"
        return " ⊢ ".join(fmt(c) for c in path) + "   ACCEPT"
