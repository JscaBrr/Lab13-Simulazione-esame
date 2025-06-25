from database.DB_connect import DBConnect
from model.driver import Driver

class DAO:

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()
        cursor = conn.cursor()
        query = "SELECT DISTINCT year FROM seasons"
        cursor.execute(query)
        rows = cursor.fetchall()
        years = [row[0] for row in rows]
        cursor.close()
        conn.close()
        return years

    @staticmethod
    def getAllNodes(y):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT DISTINCT D.* 
        FROM drivers D, results R, races Ra
        WHERE R.driverId = D.driverId
        AND R.position IS NOT NULL
        AND Ra.raceId = R.raceId
        AND Ra.year = %s
        """
        cursor.execute(query, (y,))
        listobj = []
        for dct in cursor:
            listobj.append(Driver(**dct))
        print(listobj)
        cursor.close()
        conn.close()
        return listobj


    @staticmethod
    def getAllEdges(y):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT R1.driverId AS winnerId, R2.driverId AS loserId, COUNT(*) AS weight
        FROM 
            results R1, results R2, Races Ra
        WHERE 
            R1.raceId = R2.raceId
            AND R1.raceId = Ra.raceId
            AND R1.position IS NOT NULL 
            AND R2.position IS NOT NULL
            AND R1.position < R2.position
            AND Ra.year = %s
        GROUP BY 
            R1.driverId, R2.driverId
        """
        cursor.execute(query, (y,))
        listobj = []
        for dct in cursor:
            listobj.append((dct['winnerId'], dct['loserId'], dct['weight']))
        print(len(listobj))
        cursor.close()
        conn.close()
        return listobj

    if __name__ == "__main__":
        getAllNodes(1951)
        getAllEdges(1951)

