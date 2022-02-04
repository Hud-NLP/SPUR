import neo4j
from neo4j import GraphDatabase
class NeoQuery(object):
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))
        self.userQuery = ""

    def close(self):
        self._driver.close()

    def set(self, textToSet):
        self.userQuery = textToSet

    def add(self, textToAdd):
        self.userQuery += " "+textToAdd

    def removelast(self, num_chars):
        self.userQuery = self.userQuery[:len(self.userQuery)-num_chars]

    def get(self):
        return self.userQuery

    def runDirectQuery(self, queryToRun):
        with self._driver.session() as session:
            resultOfQuery = session.run(queryToRun)
            return resultOfQuery

    def runQuery(self):
        with self._driver.session() as session:
            resultOfQuery = session.run(self.userQuery)
            return resultOfQuery

    def getResultsArray(self):
        with self._driver.session() as session:
            resultOfQuery = session.run(self.userQuery)
            resultsArray = []
            for line in resultOfQuery:
                lineOfResults = []
                for item in line:
                    lineOfResults.append(item)
                resultsArray.append(lineOfResults)
            return resultsArray