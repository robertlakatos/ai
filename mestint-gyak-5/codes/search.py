import sys
from utils import *
from node import Node
from collections import deque

# ______________________________________________________________________________
# Uninformed Search algorithms

def breadth_first_tree_search(problem):
    # kezdő állapot kiolvasása
    frontier = deque([Node(problem.initial)])

    # amig nem értük el a határt
    while frontier:
        # legszélsőbb elem kiemelése
        node = frontier.popleft()

        # ha cél állapotban vagyunk akkor vége
        if problem.goal_test(node.state):
            return node

        # a kiemelt elemből az összes új állapot legyártása az operátorok segítségével
        frontier.extend(node.expand(problem))

    return None


def breadth_first_graph_search(problem):
    # kezdő állapot kiolvasása
    node = Node(problem.initial)
    
    # ha cél állapotban vagyunk akkor vége
    if problem.goal_test(node.state):
        return node

    # elem FIFO sorba helyezése
    frontier = deque([node])
    # halmaz deklarálása
    explored = set()
    
    while frontier:
        # legszélsőbb elem kiemelése
        node = frontier.popleft()
        # legszélsőbb elem hozzá adása a halmaz hoz
        explored.add(node.state)

        # legszélsőbb elemből operátorok segítségével legyártott elemek kiolvasása
        for child in node.expand(problem):
            # Ha a gyermek még felnem fedezett és még nem része FIFO sornak (szélső elemeknek) akkor
            if child.state not in explored and child not in frontier:
                # ha cél állapotban vagyunk akkor vége
                if problem.goal_test(child.state):
                    return child
                # potenciális szélső elemek bővítése
                frontier.append(child)
    return None


def depth_first_tree_search(problem): 
    # Kezdő elem verembe helyezése
    frontier = [Node(problem.initial)]  

    # Amig tudunk mélyebre menni
    while frontier:
        # Legfelső elem kiemelése a veremből
        node = frontier.pop()

        # ha cél állapotban vagyunk vége
        if problem.goal_test(node.state):
            return node

        # Az összes gyermek legyártása az operátorok segítségével
        frontier.extend(node.expand(problem))
        
    return None


def depth_first_graph_search(problem):
    # Kezdő elem verembe helyezése
    frontier = [(Node(problem.initial))] 
    # halmaz deklarálása a már bejárt elemekhez
    explored = set()

    # Amig tudunk mélyebre menni
    while frontier:
        # Legfelső elem kiemelése a veremből
        node = frontier.pop()

        # ha cél állapotban vagyunk vége
        if problem.goal_test(node.state):
            return node

        # állapot feljegyzése hogy tudjuk hogy már jártunk itt
        explored.add(node.state)

        # verem bővítése amig benemjárt elemekkel
        frontier.extend(child for child in node.expand(problem)
                        if child.state not in explored and child not in frontier)
    return None


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


def uniform_cost_search(problem, display=False):
    return best_first_graph_search(problem, lambda node: node.path_cost, display)


def depth_limited_search(problem, limit=50):
    # rekurzív deep limited search függvény
    def recursive_dls(node, problem, limit):
        # Ha cél állapotban vagyunk akkor vége
        if problem.goal_test(node.state):
            return node
        # Ha elértük a limetet akkor vége mélyebre nem mehetünk
        elif limit == 0:
            return 'cutoff'
        else:
            # Nem történt vágás
            cutoff_occurred = False

            # gyermekek legyártása az operátorokkal
            # print(node, node.expand(problem))
            for child in node.expand(problem):
                # gyermek elemből indulva ismétleés
                result = recursive_dls(child, problem, limit - 1)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result
            return 'cutoff' if cutoff_occurred else None

    # Body of depth_limited_search:
    return recursive_dls(Node(problem.initial), problem, limit)


def iterative_deepening_search(problem):
    # Elindulunk egy maximális mélységtől és addig növeljük azt amíg célba nem érünk
    for depth in range(sys.maxsize):
        result = depth_limited_search(problem, depth)
        if result != 'cutoff':
            return result
