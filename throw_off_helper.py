import matplotlib.pyplot as plt
import matplotlib.patches as patches

def next_states(state, curr_place, next_place, cells, blocks, holes):
    _next_states = []
    _owns, _enemies = list(state[0]), list(state[1])
    _ct_owns = _owns.count(curr_place)
    _owns = list(filter(lambda x: x != curr_place, _owns))
    #_owns.extend([curr_place]*_ct_owns)
    vec = (next_place[0] - curr_place[0], next_place[1] - curr_place[1])
    if vec[0] > 0 and vec[1] == 0: step = (1,0)
    elif vec[0] < 0 and vec[1] == 0: step = (-1,0)
    elif vec[0] == 0 and vec[1] > 0: step = (0,1)
    else: step = (0,-1)
    _unique_enemies = set(_enemies)
    for en in _unique_enemies:
        _ct_en = _enemies.count(en)
        _next_owns = _owns[:]
        _next_enemies = list(filter(lambda x: x!=en, _enemies))
        curr_vec = [0,0]
        _old_place = en
        _place = list(en)
        while tuple(curr_vec) != vec:
            _place[0] += step[0]
            _place[1] += step[1]
            if tuple(_place) not in cells:
                if tuple(_old_place) not in holes:
                    _next_enemies.extend((tuple(_old_place),)*_ct_en)
                    _next_owns = list(filter(lambda x: x!= _old_place, _next_owns))
                break
            if (_old_place, tuple(_place)) in blocks:
                if tuple(_old_place) not in holes:
                    _next_enemies.extend((tuple(_old_place),)*_ct_en)
                    _next_owns = list(filter(lambda x: x != _old_place, _next_owns))
                break
            curr_vec[0] += step[0]
            curr_vec[1] += step[1]
            _old_place = tuple(_place)
        if tuple(curr_vec) == vec:
            if tuple(_place) not in holes:
                _next_enemies.extend((tuple(_place),)*_ct_en)
                _next_owns = list(filter(lambda x: x != tuple(_place), _next_owns))
        if next_place not in _enemies and next_place not in holes and next_place not in _next_enemies:
            _next_owns.extend([next_place]*_ct_owns)
        _next_owns.sort()
        _next_enemies.sort()
        if tuple(_next_enemies) != tuple(sorted(_enemies)):
            _next_states.append((tuple(_next_owns), tuple(_next_enemies)))
    return _next_states

def moves(state, cells, blocks):
    _moves = []
    _owns = state[0]
    _unique_owns = set(_owns)
    for o in _unique_owns:
        for vec in [(0,-1), (0,1), (-1,0), (1,0)]:
            _place = list(o)
            _old_place = tuple(_place)
            _place[0] += vec[0]
            _place[1] += vec[1]
            while tuple(_place) in cells and (_old_place, tuple(_place)) not in blocks:
                _moves.append((o, tuple(_place)))
                _old_place = tuple(_place)
                _place[0] += vec[0]
                _place[1] += vec[1]
    return _moves

def display(cells, blocks, holes, state, save=False, path=None):
    width = 20
    fig, ax = plt.subplots(figsize=(4,8))
    # x1, y1, x2, y2 = [], [], [], []
    plt.xlim(-10,150)
    plt.ylim(-10,200)
    # for cell in cells:
    #     for k in range(4):
    #         x1.append((cell[0]+int(k==0)+int(k==2)+int(k==3))*width)
    #         y1.append((cell[1]+int(k==1)+int(k==3)+int(k==2))*width)
    #         x2.append((cell[0]+int(k==2))*width)
    #         y2.append((cell[1]+int(k==3))*width)
    # for i in range(len(x1)):
    #     plt.plot((x1[i], x2[i]), (y1[i], y2[i]), linewidth=0.1, color='black')
    x1, y1, x2, y2 = [], [], [], []
    for cell in cells:
        if cell in holes:
            fig.gca().add_patch(patches.Rectangle((cell[0]*width,cell[1]*width),
                                  width, width, linewidth=0.1, edgecolor='black', facecolor= '#b09a99'))
        else:
            fig.gca().add_patch(patches.Rectangle((cell[0]*width,cell[1]*width),
                                  width, width, linewidth=0.1, edgecolor='black', facecolor='None'))
        if (cell[0]+1, cell[1]) not in cells:
            x1.append((cell[0]+1)*width)
            x2.append((cell[0]+1)*width)
            y1.append(cell[1]*width)
            y2.append((cell[1]+1)*width)
        if (cell[0]-1, cell[1]) not in cells:
            x1.append((cell[0])*width)
            x2.append((cell[0])*width)
            y1.append(cell[1]*width)
            y2.append((cell[1]+1)*width)
        if (cell[0], cell[1]+1) not in cells:
            x1.append((cell[0])*width)
            x2.append((cell[0]+1)*width)
            y1.append((cell[1]+1)*width)
            y2.append((cell[1]+1)*width)
        if (cell[0], cell[1]-1) not in cells:
            x1.append((cell[0])*width)
            x2.append((cell[0]+1)*width)
            y1.append(cell[1]*width)
            y2.append((cell[1])*width)

    for b in blocks:
        if b[0][0] == b[1][0]:
            x1.append((min(b[0][0], b[1][0]))*width)
            x2.append((min(b[0][0], b[1][0])+1)*width)
            y1.append((min(b[0][1], b[1][1])+1)*width)
            y2.append((min(b[0][1], b[1][1])+1)*width)
        if b[0][1] == b[1][1]:
            x1.append((min(b[0][0], b[1][0])+1)*width)
            x2.append((min(b[0][0], b[1][0])+1)*width)
            y1.append((min(b[0][1], b[1][1]))*width)
            y2.append((min(b[0][1], b[1][1])+1)*width)
    for i in range(len(x1)):
        ax.plot((x1[i], x2[i]), (y1[i], y2[i]), linewidth=2, color='black')
    #plt.axis('off')
    _x_ticks = set()
    _y_ticks = set()
    for cell in cells:
        _x_ticks.add(cell[0])
        _y_ticks.add(cell[1])
    _x_ticks = list(_x_ticks)
    _y_ticks = list(_y_ticks)
    _x_ticks.sort()
    _y_ticks.sort()
    x_ticks = []
    y_ticks = []
    for i in range(len(_x_ticks)-1):
        x_ticks.append(width*(_x_ticks[i]+_x_ticks[i+1])/2)
    x_ticks.append(width*(2*_x_ticks[-1]+1)/2)
    for i in range(len(_y_ticks)-1):
        y_ticks.append(width*(_y_ticks[i]+_y_ticks[i+1])/2)
    y_ticks.append(width*(2*_y_ticks[-1]+1)/2)
    plt.xticks(x_ticks, [i for i in range(len(x_ticks))])
    plt.yticks(y_ticks, [i for i in range(len(y_ticks))])
    _owns, _enemies = state[0], state[1]
    used = set()
    for o in _owns:
        if o not in used:
            ax.add_patch(patches.Circle((width*(2*o[0]+1)/2, width*(2*o[1]+1)/2),
                                              width/4, linewidth=0.1, edgecolor='black', facecolor='#edeb51'))
            used.add(o)
        if _owns.count(o) > 1:
            ax.text(width*(2*o[0]+0.8)/2, width*(2*o[1]+0.8)/2, str(_owns.count(o)), fontsize=12)
    for e in _enemies:
        if e not in used:
            ax.add_patch(patches.Circle((width*(2*e[0]+1)/2, width*(2*e[1]+1)/2),
                                                  width/4, linewidth=0.1, edgecolor='black', facecolor='#e32f27'))
            used.add(e)
        if _enemies.count(e) > 1:
            ax.text(width*(2*e[0]+0.8)/2, width*(2*e[1]+0.8)/2, str(_enemies.count(e)), fontsize=12)
    if save: fig.savefig(path)
    else: plt.show()

def get_score(state, states):
    if len(state[0]) == 0:
        return 10000
    if len(state[1]) > 0:
        if state in states:
            return states[state]
        states[state] = 1000
        return 1000
    else:
        return 0

def update_score(state, states, cells, blocks, holes):
    _minim = states[state]
    for m in moves(state, cells, blocks):
        _maxim = -1
        for ns in next_states(state, m[0], m[1], cells, blocks, holes):
            _maxim = max(_maxim, get_score(ns, states))
        if _maxim == -1: _maxim = 10000
        _minim = min(_minim, _maxim+1)
    return _minim

