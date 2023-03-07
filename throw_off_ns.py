from itertools import combinations_with_replacement
from throw_off_helper import *
from random import randint, choice
import os

cells = set()
blocks = set()
holes = set()

states = {}
path = 'sep_ns2bn_5'

bnd = (2,6)
for i in range(bnd[0]):
    for j in range(bnd[1]):
        cells.add((i,j))
        blocks.add(((0,j), (1,j)))

for i in range(randint(4,6)):
    holes.add((randint(0, bnd[0]-1), randint(0, bnd[1]-1)))

check_holes = [False, False]
for h in holes:
    check_holes[h[0]] = True

if not (check_holes[0] and check_holes[1]):
    raise ValueError

all_combs = [tuple()]

for cell in cells:
    if cell not in holes:
        all_combs.append((cell,))

# blocks_ct = randint(3,5)
# k = 0
# steps = [(0,1), (0,-1), (1,0), (-1,0)]
# _cells = list(cells)
# while k < blocks_ct:
#     b1 = choice(_cells)
#     b2 = list(b1)
#     step = choice(steps)
#     b2[0] += step[0]
#     b2[1] += step[1]
#     b2 = tuple(b2)
#     if b2[0] >= 0 and b2[0] < bnd[0] and b2[1] >= 0 and b2[1] < bnd[1]:
#         if (b1, b2) not in blocks and (b2, b1) not in blocks:
#             blocks.add((b1,b2))
#             k += 1

blocks_to_add = set()
for b in blocks:
    blocks_to_add.add((b[1], b[0]))

for b in blocks_to_add:
    blocks.add(b)


for k in range(2,6):
    for comb in combinations_with_replacement(cells, k):
        #print(k, comb)
        for c in comb:
            to_check = True
            for c in comb:
                if c in holes:
                    to_check = False
                    break
            if to_check:
                _comb = list(comb)
                _comb.sort()
                all_combs.append(tuple(_comb))

for comb_left in all_combs:
    #print(comb_left)
    for comb_right in all_combs:
        if len([v for v in comb_left if v in comb_right]) == 0:
            states[(comb_left, comb_right)] = 1000

ind = 0
diff = 1
while diff > 0:
    diff = 0
    ind2 = 0
    keys = list(states.keys())
    print(len(keys))
    for s in keys:
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