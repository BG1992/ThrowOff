from itertools import combinations
from throw_off_helper import *
import os

cells = set()
blocks = set()
holes = set()

states = {}

for i in range(3):
    for j in range(3):
        cells.add((i,j))

blocks.add(((0,1), (1,1)))
blocks.add(((1,1), (1,2)))

blocks_to_add = set()
for b in blocks:
    blocks_to_add.add((b[1], b[0]))

for b in blocks_to_add:
    blocks.add(b)

holes.add((2,2))

for comb in combinations(cells, 2):
    if comb[0] not in holes and comb[1] not in holes:
        _tp = ((comb[0],), (comb[1],))
        states[_tp] = 1000
        _tp = ((comb[1],), (comb[0],))
        states[_tp] = 1000

ind = 0
diff = 1
while diff > 0:
    diff = 0
    for s in states:
        new_score = update_score(s, states, cells, blocks, holes)
        if new_score < states[s]:
            diff += (states[s] - new_score)
            states[s] = new_score
    print(ind, diff)
    ind += 1

states_computed = list(states.items())
states_computed = list(filter(lambda x: x[1] < 1000, states_computed))
states_computed.sort(key= lambda x: -x[1])

for m in moves(states_computed[0][0], cells, blocks):
    print(m)
    for ns in next_states(states_computed[0][0], m[0], m[1], cells, blocks, holes):
        print(ns)
    print('*************************************')

print(states_computed[0])
display(cells, blocks, holes, states_computed[0][0])
s = states_computed[0][0]
os.mkdir('3x3_1')
i = 0
while len(s[1]) > 0:
    _min = 1000
    _ns = None
    for m in moves(s, cells, blocks):
        _next_states = next_states(s, m[0], m[1], cells, blocks, holes)
        if len(_next_states) > 0:
            if _min > get_score(_next_states[0], states):
                _min = get_score(_next_states[0], states)
                _ns = _next_states[0]

    display(cells, blocks, holes, _ns, True, '3x3_1/fig_s' + str(i) + '.png')
    s = _ns
    print(s, i)
    i += 1