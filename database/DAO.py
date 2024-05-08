from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.fermata import Fermata


class DAO:

    @staticmethod
    def getAllFermate():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM fermata"
        cursor.execute(query)

        for row in cursor:
            result.append(Fermata(row["id_fermata"], row["nome"], row["coordX"], row["coordY"]))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(v1, v2):
        """
        Restituisce l'arco tra i due vertici come parametri
        :param v1: vertice 1
        :param v2: vertice 2
        """
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM connessione c WHERE c.id_stazP = %s AND c.id_stazA = %s"
        cursor.execute(query, (v1.id_fermata, v2.id_fermata))

        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdgesVicini(v):
        """
        Restituisce gli archi che collegano v a tutti i vicini
        :param v: vertice 1
        """
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "select * from connessione c where c.id_stazP = %s"
        cursor.execute(query, (v.id_fermata, ))

        for row in cursor:
            result.append(
                Connessione(row["id_connessione"], row["id_linea"], row["id_stazP"], row["id_stazA"])
            )
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllConnessioni():
        """
        Restituisce tutte le connessioni del database, compresi i duplicati
        """
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "select * from connessione c"
        cursor.execute(query)

        for row in cursor:
            result.append(
                Connessione(row["id_connessione"], row["id_linea"], row["id_stazP"], row["id_stazA"])
            )
        cursor.close()
        conn.close()
        return result