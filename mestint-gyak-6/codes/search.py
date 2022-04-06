from utils import *
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

def best_first_graph_search(problem, f, display=False):
    f = memoize(f, 'f')
    # kezdő állapot létrehozása
    node = Node(problem.initial)
    # prioritásos sor létrehozása
    frontier = PriorityQueue('min', f)
    # kezdő állapot felvétele a prioritásos sorba
    frontier.append(node)
    # halmaz létrehozása a már megvizsgál elemekhez
    explored = set()

    # amíg találunk elemet
    while frontier:
        # elem kivétele a verem tetejéről
        node = frontier.pop()
        
        # ha cél állapotban vagyunk a kkor kész
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node
        
        # feldolgozott elemek bővítése
        explored.add(node.state)

        # operátorral legyártott gyermek elemek bejárása
        for child in node.expand(problem):
            # ha még nem dolgoztuk fel
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            # ha az adott pozicióbol elérhető gyermek függvény szerinti értéke
            # kisebb mint a már tárolté akkor újra rögzítjük
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

def astar_search(problem, h=None, display=False):
    """Az A* keresés a legjobb első gráfkeresés, ahol f(n) = g(n)+h(n). Meg kell adnia a h függvényt csillagkeresés hívásakor, vagy a Probléma alosztályban."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)