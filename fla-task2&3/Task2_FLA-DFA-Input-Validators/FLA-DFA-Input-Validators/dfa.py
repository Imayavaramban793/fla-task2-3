"""Small DFA toolkit: simulation with step trace, product (intersection), minimisation.

A DFA here works over *character classes*. `classify(ch)` maps a raw character to a class
(or None if the character belongs to no class). A missing transition leads to the implicit
trap state qD, which never accepts and is left out of tables and figures.
"""
from collections import deque

TRAP = "qD"


class DFA:
    def __init__(self, delta, start, accepting, classify, alphabet):
        self.delta = dict(delta)          # {(state, class): state}
        self.start = start
        self.accepting = set(accepting)
        self.classify = classify
        self.alphabet = list(alphabet)    # list of classes

    @property
    def states(self):
        s = {self.start} | self.accepting
        for (p, _), q in self.delta.items():
            s.add(p)
            s.add(q)
        return s

    def move(self, state, cls):
        if state == TRAP:
            return TRAP
        return self.delta.get((state, cls), TRAP)

    def run(self, text, trace=False):
        state, steps = self.start, []
        for ch in text:
            cls = self.classify(ch)
            nxt = self.move(state, cls)
            steps.append((state, ch, cls, nxt))
            state = nxt
        ok = state in self.accepting
        return (ok, steps) if trace else ok

    def accepts(self, text):
        return self.run(text)

    def format_trace(self, text, name="DFA"):
        ok, steps = self.run(text, trace=True)
        lines = [f"{name} on {text!r}"]
        for i, (p, ch, cls, q) in enumerate(steps, 1):
            lines.append(f" {i}. d({p}, {ch!r} -> {cls}) = {q}")
        final = steps[-1][3] if steps else self.start
        lines.append(f" final state {final} -> {'ACCEPTED' if ok else 'REJECTED'}")
        return "\n".join(lines)

    def minimize(self):
        """Moore partition refinement on the complete automaton; trap state dropped."""
        seen, dq = {self.start}, deque([self.start])
        while dq:
            p = dq.popleft()
            for c in self.alphabet:
                q = self.move(p, c)
                if q not in seen:
                    seen.add(q)
                    dq.append(q)
        block = {s: (1 if s in self.accepting else 0) for s in seen}
        while True:
            sig = {s: (block[s], tuple(block[self.move(s, c)] for c in self.alphabet)) for s in seen}
            ids = {}
            new = {s: ids.setdefault(sig[s], len(ids)) for s in seen}
            stable = len(set(new.values())) == len(set(block.values()))
            block = new
            if stable:
                break
        live = set(self.accepting & seen)
        changed = True
        while changed:
            changed = False
            for s in seen:
                if s not in live and any(self.move(s, c) in live for c in self.alphabet):
                    live.add(s)
                    changed = True
        rep = {}
        for s in sorted(seen, key=str):
            rep.setdefault(block[s], s)
        live_blocks = {block[s] for s in live}
        raw = {}
        for b in live_blocks:
            for c in self.alphabet:
                t = self.move(rep[b], c)
                if block[t] in live_blocks:
                    raw[(b, c)] = block[t]
        start_b = block[self.start]
        order, dq = {start_b: "q0"}, deque([start_b])
        while dq:
            b = dq.popleft()
            for c in self.alphabet:
                if (b, c) in raw and raw[(b, c)] not in order:
                    order[raw[(b, c)]] = f"q{len(order)}"
                    dq.append(raw[(b, c)])
        delta = {(order[b], c): order[t] for (b, c), t in raw.items() if b in order}
        acc = {order[block[s]] for s in self.accepting if block[s] in order}
        return DFA(delta, "q0", acc, self.classify, self.alphabet)


def product(a, b):
    """Intersection of two DFAs over the same class alphabet (reachable part only)."""
    assert a.alphabet == b.alphabet
    start = (a.start, b.start)
    delta, seen, dq = {}, {start}, deque([start])
    while dq:
        p = dq.popleft()
        for c in a.alphabet:
            x, y = a.move(p[0], c), b.move(p[1], c)
            if x == TRAP or y == TRAP:
                continue
            q = (x, y)
            delta[(p, c)] = q
            if q not in seen:
                seen.add(q)
                dq.append(q)
    acc = {p for p in seen if p[0] in a.accepting and p[1] in b.accepting}
    return DFA(delta, start, acc, a.classify, a.alphabet)
