from database.DAO import DAO
import networkx as nx
from matplotlib import pyplot as plt


class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo = nx.DiGraph()
        self._idMap = {}  #mappa in cui a ogni id_fermata è associato l'oggetto fermata
        for f in self._fermate:
            self._idMap[f.id_fermata] = f

    def buildGraph(self):
        """
        Costruisce il grafo (tre modalità diverse)
        """
        self._grafo.add_nodes_from(self._fermate)  #aggiungo le fermate al grafo

        # MODO 1: doppio loop sui nodi per ottenere tutti gli archi: ESEGUE N*N QUERY OGNI VOLTA
        """for u in self._fermate:
            for v in self._fermate:
                res = DAO.getEdges(u, v)
                if len(res) > 0:
                    self._grafo.add_edge(u, v)"""

        # MODO 2: per ogni nodo ciclo sui vicini e aggiungo le connessioni: ESEGUE N QUERY
        """t1 = time()
        for u in self._fermate:
            vicini = DAO.getEdgesVicini(u)
            for v in vicini:  #cicla sugli id e non sugli oggetti
                v_nodo = self._idMap[v.id_stazA]  #creo il nodo vicino tramite la mappa
                self._grafo.add_edge(u, v_nodo)  #aggiungo l'arco con i due oggetti
                print(f"Added edge between {u} and {v_nodo}")
        t2 = time()
        print(f"Elapsed: {t2-t1} s")"""

        # MODO 3: carico tutte le connessioni su python e le gestisco internamente: ESEGUE UNA SOLA QUERY
        allConnessioni = DAO.getAllConnessioni()
        for c in allConnessioni:
            u_nodo = self._idMap[c.id_stazP]  # creo il nodo u tramite
            v_nodo = self._idMap[c.id_stazA]  # creo il nodo u tramite
            self._grafo.add_edge(u_nodo, v_nodo)  # aggiungo l'arco con i due oggetti

    def builGraphPesato(self):
        """
        Costruisce un grafo pesato
        """
        self._grafo.clear_edges()
        self._grafo.add_nodes_from(self._fermate)
        self.add_edge_pesati()
        
    def add_edge_pesati(self):
        """
        Costruisce gli archi del grafo e gli dà un peso progressivo a partire da 1 a seconda del numero
        """
        self._grafo.clear_edges()
        allConnessioni = DAO.getAllConnessioni()
        for c in allConnessioni:
            if self._grafo.has_edge(self._idMap[c.id_stazP], self._idMap[c.id_stazA]):
                self._grafo[self._idMap[c.id_stazP]][self._idMap[c.id_stazA]]["weight"] += 1
            else:
                self._grafo.add_edge(self._idMap[c.id_stazP], self._idMap[c.id_stazA], weight=1)

    def get_nodes_BFS(self, source):
        """
        Cerca i vicini con metodo BFS
        """
        edges = nx.bfs_edges(self._grafo, source)
        visited = []
        for u, v in edges:
            visited.append(v)
        return visited

    def get_nodes_DFS(self, source):
        """
        Cerca i vicini con il metodo DFS
        """
        edges = nx.dfs_edges(self._grafo, source)
        visited = []
        for u, v in edges:
            visited.append(v)
        return visited

    def getArchiPesoMaggiore(self):
        if len(self._grafo.edges) == 0:
            print("Il grafo è vuoto")
            return
        edges = self._grafo.edges
        result = []
        for u, v in edges:
            peso = self._grafo[u][v]["weight"]
            if peso > 1:
                result.append((u, v, peso))
        return result

    @property
    def fermate(self):
        return self._fermate

    @property
    def grafo(self):
        return self._grafo

    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)
