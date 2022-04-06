# Hatékony csomag numerikus számításokhoz, n dimenziós tömbök kezeléséhez.
import numpy as np
# A standard könyvtárból hiányzó de gyakorta használt csomagok gyűjteménye
# Az utils-ra az argmax_random_tie aima projekthez definiált függvény miatt van szükség.
from utils import *
# Csomópontok létrehozására szolgáló Node osztály
from node import Node

# Próba hiba módszer
def trial_error(problem):
    # kezdő állapot
    state = Node(problem.initial)

    # végtelen ciklus definiálása
    while True:
        # Ha a probléma megoldva akkor leállítjuk a végtelen ciklust
        if problem.goal_test(state.state):
            print('Got it')
            return state

        # Az alkalmazható operátorok segítsével 
        # gyártsuk le az összes lehetséges utódot 
        succesors=state.expand(problem)

        # Ha nincs új állapot (utód)
        if len(succesors)==0:
            return 'Unsolvable'

        # random választunk egy új a legyártott utódok közül
        state=succesors[np.random.randint(0,len(succesors))]
        print(state)

def hill_climbing_for_3Cup(problem, heuristic):
    # kezdő állapot
    state = Node(problem.initial)

    # végtelen ciklus definiálása
    while True:
        # Ha a probléma megoldva akkor leállítjuk a végtelen ciklust
        if problem.goal_test(state.state):
            return state

        # Az alkalmazható operátorok segítsével 
        # gyártsuk le az összes lehetséges utódot 
        succesors=state.expand(problem)

        # keresünk egy jobb állapotott a heurisztikának
        # megfelelően
        test_succesors=[]
        for s_test in succesors:
            if heuristic(state.state)>=heuristic(s_test.state):
                test_succesors.append(s_test)

        # Ha nincs jobb állapot
        if len(test_succesors)==0:
            return 'Unsolvable'

        # legjobb állapot megkeresése
        best_succesors=[test_succesors[0]]
        for i in range(1, len(test_succesors)):
            h=heuristic(test_succesors[i].state)
            m=heuristic(test_succesors[0].state)
            if h < m:
                best_succesors=[]
                best_succesors.append(test_succesors[i])
            elif h == m:
                best_succesors.append(test_succesors[i])
        
        # ha több azonosan jó van akkor random választunk egyet
        state=best_succesors[np.random.randint(0,len(best_succesors))]