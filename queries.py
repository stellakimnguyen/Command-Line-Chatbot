from rdflib import Graph

g = Graph()
g.parse("./triples.rdf", format="application/rdf+xml")

q = "SELECT DISTINCT ?lab WHERE { ?course a ex:Course . ?course ex:cSubject \"SOEN\". ?course ex:cNum \"321\". ?lab a ex:Lab . ?lab ex:assoLec ?lec . ?lec ex:assoCourse ?course . }"
x = g.query(q)
print (list(x))