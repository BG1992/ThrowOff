from itertools import combinations_with_replacement, combinations
from throw_off_helper import *
from random import randint, choice
import os

cells = set()
blocks = set()
holes = set()

states = {}
path = '1vsn_4'

bnd = (5,5)
for i in range(bnd[0]):
    for j in range(bnd[1]):
        cells.add((i,j))

# blocks.add(((0,1), (1,1)))
# blocks.add(((0,2), (1,2)))
# blocks.add(((1,0), (1,1)))
# blocks.add(((2,0), (2,1)))
# blocks.add(((2,0), (3,0)))
# blocks.add(((1,2), (2,2)))
# blocks.add(((1,3), (2,3)))
# blocks.add(((2,2), (3,2)))
# blocks.add(((3,2), (3,3)))

blocks_ct = randint(6, 9)
k = 0
steps = [(0,1), (0,-1), (1,0), (-1,0)]
_cells = list(cells)
while k < blocks_ct:
    b1 = choice(_cells)
    b2 = list(b1)
    step = choice(steps)
    b2[0] += step[0]
    b2[1] += step[1]
    b2 = tuple(b2)
    if b2[0] <= bnd[0] and b2[0] >= 0 and b2[1] <= bnd[1] and b2[1] >= 0:
        if (b1, b2) not in blocks and (b2, b1) not in blocks:
            blocks.add((b1,b2))
            k += 1

blocks_to_add = set()
for b in blocks:
    blocks_to_add.add((b[1], b[0]))

for b in blocks_to_add:
    blocks.add(b)

print(blocks)
holes.add((randint(0, bnd[0]), randint(0, bnd[1])))
all_combs = [tuple()]

for cell in cells:
    if cell not in holes:
        all_combs.append((cell,))

for k in range(2, 3):
    for comb in combinations_with_replacement(cells, k):
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
    if len(comb_left) <= 1:
        for comb_right in all_combs:
            if len([v for v in comb_left if v in comb_right]) == 0:
                states[(comb_left, comb_right)] = 1000

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
states_computed = list(filter(lambda x: x[1] < 1000 and len(x[0][1]) == 2, states_computed))
states_computed = list(filter(lambda x: x[0][1][0] != x[0][1][1], states_computed))
states_computed.sort(key= lambda x: -x[1])

# for m in moves(states_computed[0][0], cells, blocks):
#     print(m)
#     for ns in next_states(states_computed[0][0], m[0], m[1], cells, blocks, holes):
#         print(ns)
#     print('*************************************')

s = states_computed[0][0]
print(s, states[s])
if not os.path.exists(path): os.mkdir(path)
else: os.rmdir(path)
display(cells, blocks, holes, s, True, path+'/fig_s' + str(0) + '.png')
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

    display(cells, blocks, holes, _ns, True, path+'/fig_s' + str(i) + '.png')
    s = _ns
    print(s, i)
    i += 1