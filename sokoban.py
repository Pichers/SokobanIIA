from planningPlus import *
from logic import *
from utils import *
from search import *
import traceback
import sys


def sokoban(puzzle):
    state = []
    domain = []
    goal = ''
    actions = []

    goals = []

    lines = puzzle.split('\n')

    boxCount = 0

    for i in range(len(lines)):
        line = lines[i]
        for j in range(len(line)):
            c = line[j]
            pos = (i,j)

            if c == '@' or c == '+':
                state.append(expr('S('+ str(pos) +')'))
                # state['p'] = pos
                if c == '+':
                    # state['goals'].append(pos)
                    state.append(expr('Goal(' + str(pos) + ')'))
                    goals.append(pos)

            elif c == '$' or c == '*':
                # state['boxes'].append(pos)
                state.append(expr('Box(' + str(pos) + ')'))
                boxCount += 1
                if c == '*':
                    # state['goals'].append(pos)
                    state.append(expr('Goal(' + str(pos) + ')'))
                    goals.append(pos)

            elif c == 'o':
                # state['goals'].append(pos)
                goals.append(pos)
                state.append(expr('Goal(' + str(pos) + ')'))

            elif c == '#':
                # state['walls'].append(pos)
                state.append(expr('Wall(' + str(pos) + ')'))

    print("state: " + str(state))

    for i in range(boxCount):
        g = goals[i]
        goal = goal.join('Box('+ str(g) + ')')

        if i != (boxCount - 1):
            goal = goal.join(' & ')
                
    print("goal: " + goal)

    th = PlanningProblem(state, goal, actions, domain)
    fp = ForwardPlan(th)
    return fp



linha1= "##########\n"
linha2= "#........#\n"
linha3= "#..$..+..#\n"
linha4= "#........#\n"
linha5= "##########\n"
grelha=linha1+linha2+linha3+linha4+linha5
try:
    p=sokoban(grelha)
    travel_sol = breadth_first_graph_search_plus(p)
    if travel_sol:
        print('Solução em',len(travel_sol.solution()),'passos')
    else:
        print('No way!')
except Exception as e:
    print(traceback.format_exc())