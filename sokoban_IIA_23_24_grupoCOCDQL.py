from planningPlus import *
from logic import *
from utils import *
from search import *


def sokoban(puzzle):
    state = []
    goal = []
    actions = []
    walls = []

    lines = puzzle.split('\n')

    for i in range(len(lines)):
        line = lines[i]
        for j in range(len(line)):
            c = line[j]
            pos = (i, j)

            if c == '@' or c == '+':
                state.append(expr('S(I'+ str(i) + 'J' + str(j) + ')'))
                state.append(expr('~Box(I'+ str(i) + 'J' + str(j) + ')'))
                state.append(expr('~Wall(I'+ str(i) + 'J' + str(j) + ')'))
                if c == '+':
                    goal.append(expr('Box(I'+ str(i) + 'J' + str(j) + ')'))
                    state.append(expr('Goal(I'+ str(i) + 'J' + str(j) + ')'))

            elif c == '$' or c == '*':
                state.append(expr('Box(I'+ str(i) + 'J' + str(j) + ')'))
                state.append(expr('~S(I'+ str(i) + 'J' + str(j) + ')'))
                state.append(expr('~Wall(I'+ str(i) + 'J' + str(j) + ')'))
                if c == '*':
                    goal.append(expr('Box(I'+ str(i) + 'J' + str(j) + ')'))
                    state.append(expr('Goal(I'+ str(i) + 'J' + str(j) + ')'))

            elif c == 'o':
                goal.append(expr('Box(I'+ str(i) + 'J' + str(j) + ')'))

                state.append(expr('Goal(I'+ str(i) + 'J' + str(j) + ')'))
                state.append(expr('~S(I'+ str(i) + 'J' + str(j) + ')'))
                state.append(expr('~Box(I'+ str(i) + 'J' + str(j) + ')'))
                state.append(expr('~Wall(I'+ str(i) + 'J' + str(j) + ')'))
            elif c == '#':
                state.append(expr('Wall(I'+ str(i) + 'J' + str(j) + ')'))
                state.append(expr('~S(I'+ str(i) + 'J' + str(j) + ')'))
                state.append(expr('~Box(I'+ str(i) + 'J' + str(j) + ')'))
                walls.append(pos)
            else:
                state.append(expr('~Box(I'+ str(i) + 'J' + str(j) + ')'))
                state.append(expr('~Wall(I'+ str(i) + 'J' + str(j) + ')'))
                state.append(expr('~S(I'+ str(i) + 'J' + str(j) + ')'))

    for i in range(len(lines)):
        for j in range(len(lines[i])):
            posS = '(I' + str(i) + 'J' + str(j) + ')'
            
            up = '(I' + str(i-1) + 'J' + str(j) + ')'
            up2 = '(I' + str(i-2) + 'J' + str(j) + ')'

            down = '(I' + str(i+1) + 'J' + str(j) + ')'
            down2 = '(I' + str(i+2) + 'J' + str(j) + ')'

            left = '(I' + str(i) + 'J' + str(j - 1) + ')'
            left2 = '(I' + str(i) + 'J' + str(j - 2) + ')'

            right = '(I' + str(i) + 'J' + str(j + 1) + ')'
            right2 = '(I' + str(i) + 'J' + str(j + 2) + ')'

            if (i,j) not in walls:
                if i > 1:
                    actions.append(Action('MoveUpBox' + posS,
                                        precond='S' + posS  + ' & Box' + up + ' & ~Box' + up2 + ' & ~Wall' + up2,
                                        effect='~S' + posS + ' & S' + up + ' & ~Box' + up + ' & Box' + up2))
                if i > 0:
                    actions.append(Action('MoveUp' + posS,
                                        precond='S' + posS + ' & ~Wall' + up + ' & ~Box' + up,
                                        effect='~S' + posS + ' & S' + up))
                
                if i < (len(lines) - 2):
                    actions.append(Action('MoveDownBox' + posS,
                                        precond='S' + posS + ' & Box' + down + ' & ~Box' + down2 + ' & ~Wall' + down2,
                                        effect='~S' + posS + ' & S' + down + ' & ~Box' + down + ' & Box' + down2))
                if i < (len(lines) - 1):
                    actions.append(Action('MoveDown' + posS,
                                        precond='S' + posS + ' & ~Wall' + down + ' & ~Box' + down,
                                        effect='~S' + posS + ' & S' + down))

                if j > 0:
                    actions.append(Action('MoveLeftBox' + posS,
                                        precond='S' + posS + ' & Box' + left + ' & ~Box' + left2 + ' & ~Wall' + left2,
                                        effect='~S' + posS + ' & S' + left + ' & ~Box' + left + ' & Box' + left2))
                if j > 1:
                    actions.append(Action('MoveLeft' + posS,
                                        precond='S' + posS + ' & ~Wall' + left + ' & ~Box' + left,
                                        effect='~S' + posS + ' & S' + left))
                
                if j < (len(lines[i]) - 1):
                    actions.append(Action('MoveRightBox' + posS,
                                        precond='S' + posS + ' & Box' + right + ' & ~Box' + right2 + ' & ~Wall' + right2,
                                        effect='~S' + posS + ' & S' + right + ' & ~Box' + right + ' & Box' + right2))
                if j < (len(lines[i]) - 2):
                    actions.append(Action('MoveRight' + posS,
                                        precond='S' + posS + ' & ~Wall' + right + ' & ~Box' + right,
                                        effect='~S' + posS + ' & S' + right))
                #actions.append(Action('TestAction(pl)', precond='S' + posS + ' & ' + '~Wall(I2J6)', effect='Box(I2J6)'))
    #print(actions)
                    
    th = PlanningProblem(state, goal, [], [])
    fp = ForwardPlan(th)

    fp.expanded_actions = actions
    return fp