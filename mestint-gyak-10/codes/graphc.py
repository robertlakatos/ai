import time

import matplotlib
import matplotlib.pyplot as plt

import networkx as nx

from collections import defaultdict

def setup_canvas(size = (10.0, 10.0)):
    matplotlib.rcParams['figure.figsize'] = size

def make_update_step_function(graph, instru_csp):
    
    def draw_graph(graph):
        # Gráf elkészítése
        G=nx.Graph(graph)
        pos = nx.spring_layout(G,k=0.15)
        return (G, pos)
    
    G, pos = draw_graph(graph)
    
    def update_step(iteration):
        # Az iterációs lépés alamján meghatározott elem lekérdezése a history-ból
        current = instru_csp.assignment_history[iteration]
        # Az adott hozzárendelést szótárrá alakítjuk, így a hozzá nem rendelt csomópontok 
        # színe alapértelmezés szerint fekete lesz.
        current = defaultdict(lambda: 'Black', current)

        # Az adott iterációs lépésben (history) meghatározott színeket használjuk egyébként
        # alapértelmezés szerint fekete lesz a csomópont színe
        colors = [current[node] for node in G.nodes.keys()]
        # Kiszínezük a csomópontokat
        nx.draw(G, pos, node_color=colors, node_size=500)

        labels = {label:label for label in G.nodes}
        # A címkéket térben eltoljuk, hogy ne fedjék a csompontokkal egymást
        label_pos = {key:[value[0], value[1]+0.03] for key, value in pos.items()}
        nx.draw_networkx_labels(G, label_pos, labels, font_size=20)

        # Megjelenítjük a gráfot
        plt.show()

    return update_step

def make_visualize(slider):
    ''' A slider bemenetét felhasználva and vissza ad
    egy callback függvényt az időíztett animáció megjelenítéséhez
    '''
    
    def visualize_callback(Visualize, time_step):
        if Visualize is True:
            for i in range(slider.min, slider.max + 1):
                slider.value = i
                time.sleep(float(time_step))
    
    return visualize_callback
    