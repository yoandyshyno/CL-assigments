#!/usr/bin/python3
import re
import sys
import copy
from pathlib import Path

# Yoandy Sanchez 09, 2012
# Mprimes problem


def parse(filename: str) -> tuple:
    """
    This function aims to extract variables and storage them in list data structures.
    by parsing the input file using simple regular expressions.
    The function returns a list of objects locations,vehicles,cargoes,goals in this order.
    """
    # (define (problem strips-mprime-l5-f60-s10-v3-c6)
    d = re.compile(r"\(problem strips-mprime-l(\d+)-f(\d+)-s(\d+)-v(\d+)-c(\d+)\)")
    # (has-fuel l0 f53)
    hf = re.compile(r"\(has-fuel l(\d+) f(\d+)\)")
    # (has-space  v0 s10)
    hs = re.compile(r"\(has-space  v(\d+) s(\d+)\)")
    # (at v0 l3)
    atv = re.compile(r"\(at v(\d+) l(\d+)\)")
    atc = re.compile(r"\(at c(\d+) l(\d+)\)")

    # Init
    t = Path(filename).read_text()
    varis = d.findall(t)
    loc = [0 for x in range(int(varis[0][0]))]
    veh = [[0, 0] for x in range(int(varis[0][3]))]
    car = [0 for x in range(int(varis[0][4]))]

    r = re.compile(r"\(:init(\s+)(.+)(\s+)\)(\s+)\(", re.DOTALL)
    init_p = r.findall(t)[0][1]
    for (l, f) in hf.findall(init_p):
        loc[int(l)] = int(f)

    for (v, s) in hs.findall(init_p):
        veh[int(v)][1] = int(s)

    for (v, l) in atv.findall(init_p):
        veh[int(v)][0] = int(l)

    for (c, l) in atc.findall(init_p):
        car[int(c)] = int(l)

    # Goal
    r = re.compile(r"\(:goal(\s+)\(and(\s+)(.+)\)(\s+)\)(\s+)\)", re.DOTALL)
    g = [list(map(int, x)) for x in atc.findall(r.findall(t)[0][2])]
    return (loc, veh, car, g)


# optimize code by using enumerate feature later.
def genInstances(lmp: list) -> list:
    ins = []
    for mp in lmp:
        for i in range(len(mp.veh)):
            o1 = copy.deepcopy(mp)
            lc = mp.veh[i][0]
            (tol, tor) = (lc - 1, lc + 1)
            if tol < 0:
                tol = mp.n - 1
            if tor >= mp.n:
                tor = 0
            o1.move(i, lc, tol)
            o2 = copy.deepcopy(mp)
            o2.move(i, lc, tor)
            o3 = copy.deepcopy(mp)
            o4 = copy.deepcopy(mp)
            for j in range(len(mp.car)):
                if mp.car[j] == lc:
                    o3.load(j, i, lc)
                if mp.car[j] == -1 and ([j, i] in mp._in):
                    o4.unload(j, i, lc)
            ins = ins + [o1, o2, o3, o4]
    return ins


def checkGoals(lmp: list) -> tuple:
    for mp in lmp:
        flag = True
        for c, l in mp.g:
            flag = flag and (mp.car[c] == l)
        if flag:
            return (True, mp)
    return (False, None)


class Mprime:
    """
    The object Mprime represent the problem. Here we deal with the variable and
    operations defined in the domain.
    """

    def __init__(self, arg: str):
        super(Mprime, self).__init__()
        (self.loc, self.veh, self.car, self.g) = arg
        self._in = []
        self.plan = []
        self.n = len(self.loc)

    def move(self, _veh: int, lfrom: int, lto: int) -> bool:
        """
        In this method we take into account the preconditions, if a matter of fuel, we put
        a donation step before go on with the move.
        If the destination is more than 1 step from the origen, then intermediaries move plans
        are added.
        """
        if lfrom == lto:
            return True
        n = self.n
        s = (lfrom - lto) // abs(lfrom - lto)
        if abs(lfrom - lto) > n // 2:
            route = list(map(lambda x: x % n, range(lfrom + s * (-1) * n, lto + s, s)))
        else:
            route = list(range(lfrom, lto + s * (-1), -1 * s))
        for i in range(len(route) - 1):
            (a, b) = (route[i], route[i + 1])
            if self.loc[a] < 1:
                self.donate(a)
            fp = self.loc[a]
            if fp > 0:
                self.loc[a] -= 1
                self.veh[_veh][0] = b
                self.plan.append(f"(move v{_veh} l{a} l{b} f{fp} f{fp - 1})")
                # return True
            else:
                # print("Fail move")
                return False
        return True

    def load(self, _car: int, _veh: int, _loc: int) -> bool:
        sp = self.veh[_veh][1]
        if [_car, _loc] in self.g:
            return True
        if self.car[_car] == _loc and self.veh[_veh][0] == _loc and sp:
            self.car[_car] = -1
            self._in.append([_car, _veh])
            self.veh[_veh][1] -= 1
            self.plan.append(f"(load c{_car} v{_veh} l{_loc} s{sp} s{sp - 1})")
            return True
        else:
            # print("Fail load")
            return False

    def unload(self, _car: int, _veh: int, _loc: int) -> bool:
        sp = self.veh[_veh][1]
        if self.car[_car] == -1 and self.veh[_veh][0] == _loc:
            self.car[_car] = _loc
            self._in.remove([_car, _veh])
            self.veh[_veh][1] += 1
            self.plan.append(f"(unload c{_car} v{_veh} l{_loc} s{sp} s{sp + 1})")
            return True
        else:
            return False

    def donate(self, lto: int) -> bool:
        """
        When the donate method is called, we perform a search of a location that contains
        enough fuel, then we force a donation to the target location.
        """
        for i in range(len(self.loc)):
            if self.loc[i] > 1:
                fo = self.loc[i]
                fd = self.loc[lto]
                self.loc[i] -= 1
                self.loc[lto] += 1
                self.plan.append(
                    f"(donate l{1} l{lto} f{fo} f{fo - 1} f{fo -2} f{fd} f{fd + 1})"
                )
                return True
        # print("Fail donation")
        return False


if __name__ == "__main__":
    vrs = parse(sys.argv[1])
    mp = Mprime(vrs)
    goalAchieved = False
    ins = [mp]

    while not goalAchieved:
        ins = genInstances(ins)
        (goalAchieved, res) = checkGoals(ins)

    for p in res.plan:
        print(p)
