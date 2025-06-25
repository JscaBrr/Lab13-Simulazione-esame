import networkx as nx
from database.DAO import DAO
import copy

class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._idMap = {}

    def getAllYears(self):
        return DAO.getAllYears()

    def getAllNodes(self, y):
        nodes = DAO.getAllNodes(y)
        for i in nodes:
            self._idMap[i.driverId] = i
        return nodes

    def getAllEdges(self, y):
        edges = []
        for i in DAO.getAllEdges(y):
            if i[0] in self._idMap and i[1] in self._idMap:
                edges.append((self._idMap[i[0]], self._idMap[i[1]], {'weight': i[2]}))
        return edges

    def creaGrafo(self, y):
        self._grafo.clear()
        self._idMap.clear()
        self._grafo.add_nodes_from(self.getAllNodes(y))
        self._grafo.add_edges_from(self.getAllEdges(y))
        bilanci = {}
        for i in self._grafo.nodes:
            vittorie = self._grafo.out_degree(i, weight="weight")
            sconfitte = self._grafo.in_degree(i, weight="weight")
            bilanci[i.surname] = vittorie - sconfitte
        driver = sorted(bilanci.items(), key=lambda x: x[1], reverse=True)[0]
        return True, self._grafo.number_of_nodes(), self._grafo.number_of_edges(), driver

    def calcolaDreamTeam(self, k):
        self._insertedK = int(k)
        self._teamOttimo = []
        self._costoBest = float('inf')
        for i in self._grafo.nodes:
            sequenza = [x for x in self._grafo.nodes if x != i]
            self.ricorsione([i], sequenza)
        return self._teamOttimo, self._costoBest

    def ricorsione(self, parziale, sequenza):
        if len(parziale) == self._insertedK:
            costo = self.costo(parziale)
            if costo < self._costoBest:
                self._costoBest = costo
                self._teamOttimo = copy.deepcopy(parziale)
                print(f"aggiornamento ({len(self._teamOttimo)}) - {self._costoBest} - {self._teamOttimo}")
        else:
            for i in sequenza:
                if self.vincoli(parziale, i):
                    parziale.append(i)
                    nuova_sequenza = [x for x in self._grafo.nodes if x not in parziale]
                    self.ricorsione(parziale, nuova_sequenza)
                    parziale.pop()

    def vincoli(self, parziale, i):
        if i in parziale:
            return False
        if len(parziale)+1 > self._insertedK:
            return False
        return True

    def costo(self, parziale):
        costoTot = 0
        for i in parziale:
            for j in self._grafo.predecessors(i):
                if j not in parziale:
                    peso = self._grafo[j][i]['weight']
                    costoTot += peso
        return costoTot




