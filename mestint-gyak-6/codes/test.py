from problem import Problem
from collections import namedtuple
State=namedtuple("State", ["disk","rod"])

class Node:
    """Csomópont a kereső fában. Tartalmaz egy mutatót a szülőre (a csomópontra, amelynek ez az utódja) és a csomópont aktuális állapotára. 
       Egy állapotot két útvonalon érünk el, akkor két azonos állapotú csomópont van. Tartalmazza azt a műveletet is, amely ebbe az állapotba juttatott minket, 
       valamint a csomópont eléréséhez szükséges teljes path_cost (más néven g) értéket. Más függvények hozzáadhatnak egy f és h értéket; lásd a 
       best_first_graph_search és az astar_search leírását az f és h értékek kezelésének magyarázatához."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Node osztály konstruktora."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        """Speciális metódus mely az objektum string állapotát definiálja"""
        return "<Node {}>".format(self.state)

    def __lt__(self, node):
        """Speciálist metódus mely definiálja hogy az adott Node objektum
        mikor kisebb e egy másik Node objektumnál"""
        return self.state < node.state

    def __eq__(self, other):
        """Speciálist metódus mely definiálja hogy az adott Node objektum
        mikor egyenlő egy másik Node objektummal"""
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        """Speciális megódus mely definiálja hogy egy adott Node objektum
        hash állapotát definiálja"""
        return hash(self.state)

    def child_node(self, problem, action):
        """A következő csomópont az adott probléma szerinti elkészítése és visszaadása"""
        next_state = problem.result(self.state, action)
        next_node = Node(state = next_state, 
                         parent = self, 
                         action = action, 
                         path_cost = problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node

    def expand(self, problem):
        """A csomópontból egy lépésben eléhető csomópontok visszadása"""
        return [self.child_node(problem, action) for action in problem.actions(self.state)]

    def solution(self):
        """A gyökér csomópontól a csompontig terjedő műveletek listájának visszaadása"""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """A gyökér csomópontól a csompontig vezető utvonal csomópontjainak listája"""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

class Hanoi(Problem):
    def __init__(self, n):
        self.size = n
        super().__init__("1" * n, "3" * n)

    def actions(self, state):
        """Operátorok definiálása"""
        acts = []
        f1 = state.find("1")
        f2 = state.find("2")
        f3 = state.find("3")
        if -1 < f1 and (f1 < f2 or f2 == -1):
            acts.append(State(f1, "2"))

        if -1 < f1 and (f1 < f3 or f3 == -1):
            acts.append(State(f1, "3"))

        if -1 < f2 and (f2 < f1 or f1 == -1):
            acts.append(State(f2, "1"))

        if -1 < f2 and (f2 < f3 or f3 == -1):
            acts.append(State(f2, "3"))

        if -1 < f3 and (f3 < f1 or f1 == -1):
            acts.append(State(f3, "1"))

        if -1 < f3 and (f3 < f2 or f2 == -1):
            acts.append(State(f3, "2"))

        return acts

    def result(self, state, action):
        """Operátorok hatásának definiálása"""

        # diks = korong, char = rúd
        disk, char = action
        # Előtte és utánna lévő korongok helyeinek hozzáfűzése hozzá fűzése
        return state[0:disk] + char + state[disk + 1:]

h2 = Hanoi(3)
init_node = Node("212")
init_node.expand(h2)