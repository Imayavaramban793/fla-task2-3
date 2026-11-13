"""Checks every DFA (and its minimised version) against an independent regular expression."""
import itertools
import random
import re

import validators as V

random.seed(7)

REGEX = {
    "mobile": re.compile(r"[6-9][0-9]{9}"),
    "plate": re.compile(r"[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}"),
    "time": re.compile(r"([01][0-9]|2[0-3]):[0-5][0-9]"),
}

CASES = {
    "mobile": (["9876543210", "6000000000", "7123456789", "8999999999"],
               ["5876543210", "987654321", "98765432101", "98765 43210", "98765a3210", "", "+919876543210"]),
    "plate": (["TN45AB1234", "MH12A1234", "KA01MN0001", "DL08CX9999"],
              ["tn45ab1234", "T45AB1234", "TN4AB1234", "TN45ABC1234", "TN45AB123", "TN45AB12345", "TN45-AB-1234", ""]),
    "time": (["00:00", "09:30", "12:59", "19:05", "23:59"],
             ["24:00", "23:60", "7:30", "12:5", "12-30", "1230", "ab:cd", "12:300", ""]),
}


def mutate(s, alphabet):
    s = list(s)
    r = random.random()
    i = random.randrange(len(s)) if s else 0
    if r < 0.4 and s:
        s[i] = random.choice(alphabet)
    elif r < 0.7 and s:
        del s[i]
    else:
        s.insert(i, random.choice(alphabet))
    return "".join(s)


def exhaustive(alpha, maxlen):
    for n in range(maxlen + 1):
        for t in itertools.product(alpha, repeat=n):
            yield "".join(t)


def check(name, machines):
    total = 0
    acc, rej = CASES[name]
    for s in acc:
        assert all(m.accepts(s) for m in machines), (name, s)
    for s in rej:
        assert not any(m.accepts(s) for m in machines), (name, s)
    total += len(acc) + len(rej)
    pool = {"mobile": "0123456789ab ", "plate": "AZaz09-", "time": "0123456789:x"}[name]
    streams = []
    if name == "mobile":
        streams.append(exhaustive("6a0", 10))
    elif name == "plate":
        streams.append(exhaustive("A1a", 9))
    else:
        streams.append(exhaustive("0235:x", 6))
    seeds = acc * 3000
    streams.append((mutate(random.choice(seeds), pool) for _ in range(20000)))
    streams.append(iter(seeds[:2000]))
    for stream in streams:
        for s in stream:
            want = bool(REGEX[name].fullmatch(s))
            for m in machines:
                assert m.accepts(s) == want, (name, s)
            total += 1
    return total


if __name__ == "__main__":
    grand = 0
    mob_d, mob_p, plate, time24 = V.mobile_direct(), V.mobile_product(), V.plate(), V.time24()
    for name, ms in [("mobile", [mob_d, mob_d.minimize(), mob_p, mob_p.minimize()]),
                     ("plate", [plate, plate.minimize()]),
                     ("time", [time24, time24.minimize()])]:
        n = check(name, ms)
        grand += n
        print(f"{name:7s} {n:8d} strings, no mismatch")
    print("states  mobile direct/product/minimal:", len(mob_d.states), len(mob_p.states), len(mob_p.minimize().states))
    print("states  plate  built/minimal:", len(plate.states), len(plate.minimize().states))
    print("states  time   built/minimal:", len(time24.states), len(time24.minimize().states))
    print("TOTAL", grand, "strings checked: ALL PASSED")
