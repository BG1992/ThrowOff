from itertools import combinations_with_replacement, permutations
from throw_off_helper import *
from random import randint, choice
import os

cells = set()
blocks = set()
holes = set()

states = {}
path = 'sep_1vsn_1'

bnd = (6,6)
for i in range(bnd[0]):
    for j in range(bnd[1]):
        cells.add((i,j))

_cells_owns = list(filter(lambda x: x[0] > 2, cells))
_cells_enemies = list(filter(lambda x: x[0] <= 2, cells))

blocks.add(((0,1), (0,2)))
blocks.add(((1,1), (1,2)))
blocks.add(((2,1), (2,2)))
blocks.add(((0,3), (0,4)))
blocks.add(((1,3), (1,4)))
blocks.add(((2,3), (2,4)))
blocks.add(((2,0), (3,0)))
blocks.add(((2,1), (3,1)))
blocks.add(((2,2), (3,2)))
blocks.add(((2,3), (3,3)))
blocks.add(((2,4), (3,4)))
blocks.add(((2,5), (3,5)))
blocks.add(((1,0), (1,1)))
blocks.add(((2,0), (2,1)))
blocks.add(((0,2), (1,2)))
blocks.add(((1,4), (2,4)))

sec1 = {(0,0), (1,0), (2,0), (0,1), (1,1), (2,1)}
sec2 = {(0,2), (1,2), (2,2), (0,3), (1,3), (2,3)}
sec3 = {(0,4), (1,4), (2,4), (0,5), (1,5), (2,5)}
sec4 = {(3,0),(3,1),(3,2),(3,3),(3,4),(3,5),
        (4,0),(4,1),(4,2),(4,3),(4,4),(4,5),
        (5,0),(5,1),(5,2),(5,3),(5,4),(5,5)}

blocks_ct = randint(6,8)
k = 0
steps = [(0,1), (0,-1), (1,0), (-1,0)]
_cells = list(cells)
while k < blocks_ct:
    b1 = choice(_cells_owns)
    b2 = list(b1)
    step = choice(steps)
    b2[0] += step[0]
    b2[1] += step[1]
    b2 = tuple(b2)
    if b2[0] >= 3 and b2[0] < bnd[0] and b2[1] >= 0 and b2[1] < bnd[1]:
        if (b1, b2) not in blocks and (b2, b1) not in blocks:
            blocks.add((b1,b2))
            k += 1

blocks_to_add = set()
for b in blocks:
    blocks_to_add.add((b[1], b[0]))

for b in blocks_to_add:
    blocks.add(b)

print(blocks)
holes.add((2,1))
holes.add((0,2))
holes.add((2,4))
all_combs = [tuple()]

for cell in cells:
    if cell not in holes:
        all_combs.append((cell,))

for k in range(2, 4):
    for comb in combinations_with_replacement(_cells_enemies, k):
        cter = {1:0,2:0,3:0}
        for c in comb:
            if c in sec1: cter[1] += 1
            if c in sec2: cter[2] += 1
            if c in sec3: cter[3] += 1
        if max(cter.values()) == 1:
            to_check = True
            for c in comb:
                if c in holes:
                    to_check = False
                    break
            if to_check:
                _comb = list(comb)
                _comb.sort()
                all_combs.append(tuple(_comb))

for comb_left in sec4:
    for comb_right in all_combs:
        if len([v for v in comb_left if v in comb_right]) == 0:
            states[((comb_left,), comb_right)] = 1000

ind = 0
diff = 1
while diff > 0:
    diff = 0
    ind2 = 0
    for s in states:
        new_score = update_score(s, states, cells, blocks, holes)
        if new_score < states[s]:
            diff += (states[s] - new_score)
            states[s] = new_score
        ind2 += 1
        if ind2 % 10000 == 0: print(ind2)
    print(ind, diff)
    ind += 1

states_computed = list(states.items())
states_computed = list(filter(lambda x: x[1] < 1000, states_computed))
states_computed.sort(key= lambda x: -x[1])

if not os.path.exists(path): os.mkdir(path)

for k in range(1):
    os.mkdir(path + '/' + str(k))
    s = states_computed[k][0]
    print(s, states[s])
    display(cells, blocks, holes, s, True, path+'/'  + str(k) + '/fig_s' + str(0) + '.png')
    i = 1
    while len(s[1]) > 0:
        _min = 1000
        _ns = None
        for m in moves(s, cells, blocks):
            _next_states = next_states(s, m[0], m[1], cells, blocks, holes)
            if len(_next_states) > 0:
                _next_states.sort(key=lambda x: -get_score(x, states))
                _maxim = 0
                for ns in _next_states:
                    _maxim = max(_maxim, get_score(ns, states))
                if _min > _maxim:
                    _min = _maxim
                    _ns = _next_states[0]

        display(cells, blocks, holes, _ns, True, path+ '/' + str(k) + '/fig_s' + str(i) + '.png')
        s = _ns
        print(s, i)
        i += 1