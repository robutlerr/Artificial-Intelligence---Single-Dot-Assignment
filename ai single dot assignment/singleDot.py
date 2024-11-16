from SingleDotProblem import State, Problem
from problemGraphics import pacmanGraphic
import random

p = Problem('singleDotMedium.txt')
#p = Problem('singleDotSmall.txt')

def prt(V):
    for k in V:
        print(k.agentPos, V[k])

# initialize V as an empty dictionary
V = {}
# select a value for gamma
gamma = 0.9
# epsilon is used to for exploration
epsilon = 0.1

# write a for loop for a maximum number of episodes
for episode in range(100):
    # set currentState as the problem start state
    currentState = p.getStartState()
    # write an infinite loop while True
    while True:    
        # Check if currentState is a Terminal state
        if p.isTerminal(currentState):
            # if currentState is a terminal state then
            # set the V for the currentState to be
            # problem reward of that currentState
            V[currentState] = p.reward(currentState)            
            # break the loop
            break

        # write an if to check if currentState is in V:
        # if currentState not in V then add it to V and set its
        # value to zero.
        if currentState not in V: 
            V[currentState] = 0

        # Compute maximum reward for all neighbors:
        # 1) get neighbors.
        neighbors = p.transition(currentState)
        
        # 2) get the maximum V for all neighbors
        # remember that neighbors is of the form
        # (next state, action)
        # a) set maxV and bestState
        maxV = -99999 # assume maximum V is lowest value
        bestState = None # assume best state is None
        # b) loop over all neighbors and find maximum V
        # and best state for the corresponding maximum V
        # you may encounter a situation where a state
        # is not in V dictionary. If this is the case
        # assume its V is zero.
        for s, a in neighbors:
            # if the state is not V, assume it is (v=0)
            # else it is v=V[s]
            if s in V: 
                v = V[s]
            else: 
                v = 0
            # Compare v with maxV, and store in maxV the maximum
            # do not forget to save the state with the maximum V
            # in bestState variable
            if v > maxV:
                maxV = v
                bestState = s
            
        # 3) Write Bellman equation V[s] = reward(s) + gamma max(V of all neighbors)                # s vs currentState
        #V[s] = p.reward(s) + (gamma * maxV)  # Apply Bellman equation
        V[currentState] = p.reward(currentState) + gamma * maxV

        # Leave this part unchanged
        r = random.random()
        if r < epsilon: n = bestState
        else:  n, a = random.choice(neighbors)
        
        # 4) set currentState to n
        currentState = n
        
        
# Extract Policy
policy = {}

# 1) Loop over all all states in V
for s in V:
    # 2) if currentState is termianl state:
    if p.isTerminal(s):
        # set the policy for currentState to None
        policy[s] = None
        # Leave continue
        continue
    # get the neighbors
    neighbors = p.transition(s)
    # Leave the next three lines
    bestAction = None
    maxV = -9999
    # Loop over all neighbors, remember neighbors 
    # are in the form: (state, action)
    for n, a in neighbors:
        # if state not in V, then assume it is v=0
        # else then assume it is v=V[s]
        if n in V:
            v = V[n]
        else:
            v = 0
        # set maxV to the maximum of the current v and maxV
        # also store the best action
        if v > maxV:
            maxV = v
            bestAction = a
    # save bestAction in policy[currentState]
    policy[s] = bestAction
    

pac = pacmanGraphic(1300, 700)
pac.setup(p)


for k in policy:
    if policy[k] == 'L': s = '\u2190'   # Prints left arrow
    if policy[k] == 'R': s = '\u2192'   # Prints right arrow
    if policy[k] == 'U': s = '\u2191'   # Prints up arrow
    if policy[k] == 'D': s = '\u2193'   # Prints down arrow
    
    pac.addText(k.agentPos[0]+0.5, k.agentPos[1]+0.5, s, fontSize=20)

currentState = p.getStartState()
count = 0
while currentState:
    a = policy[currentState]
    if a == None: break
    count+=1
    dx, dy = p.potential_moves[a]
    agentPos = (currentState.agentPos[0] + dx, currentState.agentPos[1] + dy)
    if agentPos in p.dots:
        index = p.dots.index(agentPos)
        pac.remove_dot(index)
    currentState = State(agentPos)
    pac.move_pacman(dx, dy)
    

print('plan length=', count)

