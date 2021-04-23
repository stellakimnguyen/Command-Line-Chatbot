import rdflib

g = rdflib.Graph()
g.parse("./schema.ttl", format="turtle")
g.parse("./generated_triples.ttl", format="turtle")

q1 = """
SELECT DISTINCT ?topic_name ?topic_uri ?event_uri ?content_uri
WHERE {
	{
		?content a ex:content .
		?content foaf:Document ?content_uri .
		?content ex:contentTopic ?topic .
		?topic a ex:topic .
		?topic dc:subject ?topic_name .
		?topic dc:URI ?topic_uri .
		?event_uri ex:lecContent ?content .
		?event_uri a ex:Lecture .
		?event_uri ex:assoCourse ?course .
		?course a ex:Course .
	}
	UNION
	{
		?content a ex:content .
		?content foaf:Document ?content_uri .
		?content ex:contentTopic ?topic .
		?topic a ex:topic .
		?topic dc:subject ?topic_name .
		?topic dc:URI ?topic_uri .
		?event_uri ex:lecContent ?content .
		?event_uri ex:assoLec ?lec .
		?lec ex:assoCourse ?course .
		?course a ex:Course .
	}
	FILTER(?course = ex:5484)
}

"""
q2 = """
SELECT DISTINCT ?course_name (count(?course_name) as ?count)
WHERE {
	{
		?topic a ex:topic .
		?content ex:contentTopic ?topic .
		?lec ex:lecContent ?content .
		?lec ex:assoCourse ?course .
		?course a ex:Course .
		?course ex:cName ?course_name .
	}
	UNION
	{
		?topic a ex:topic .
		?content ex:contentTopic ?topic .
		?event ex:lecContent ?content .
		?event ex:assoLec ?lec .
		?lec ex:assoCourse ?course .
		?course a ex:Course .
		?course ex:cName ?course_name .
	}
	FILTER(?topic = ex:DBpedia) .
}
GROUP BY ?course_name
ORDER BY asc(?count)
"""

q3 = """
SELECT DISTINCT ?course_uri ?event_uri ?content_uri
WHERE {
	{
		?course_uri a ex:Course .
		?lec ex:assoCourse ?course_uri .
		?lec ex:lecContent ?content .
		?content ex:contentTopic ?topic .
		?content foaf:Document ?content_uri .
	}
	UNION
	{
		?course_uri a ex:Course .
		?lec ex:assoCourse ?course_uri .
		?event_uri ex:assoLec ?lec .
		?event_uri ex:lecContent ?content .
		?content ex:contentTopic ?topic .
		?content foaf:Document ?content_uri .
	}
	FILTER(?topic = ex:DBpedia) .
}
"""

q4 = """
PREFIX xsd: <https://www.w3.org/2001/XMLSchema#>
SELECT ?topic_name
WHERE {
	?course ex:cSubject "COMP".
	?course ex:cNum "474".
	?lec ex:assoCourse ?course.
	?lec ex:lecNumber "1"^^xsd:integer .
	?lec ex:lecContent ?content .
	?content ex:contentTopic ?topic .
	?topic dc:subject ?topic_name
}
"""
q5 = """
SELECT ?lec1 ?lec2 ?topic1
WHERE {
{
	SELECT DISTINCT ?lec1 ?topic1 ?lec2 ?topic2
	WHERE {
		?course1 a ex:Course .
		?course1 ex:cSubject "COMP".
		?course1 ex:cNum "474".
		?lec1 a ex:Lecture .
		?lec1 ex:assoCourse ?course1 .
		?lec1 ex:lecContent ?content1 .
		?content1 ex:contentTopic ?topic1 .
		?topic1 dc:subject ?topic_name1 .

		?course2 a ex:Course .
		?course2 ex:cSubject "SOEN".
		?course2 ex:cNum "321".
		?lec2 a ex:Lecture .
		?lec2 ex:assoCourse ?course2 .
		?lec2 ex:lecContent ?content2 .
		?content2 ex:contentTopic ?topic2 .
		?topic2 dc:subject ?topic_name2 .

		FILTER(?topic_name1 = ?topic_name2) .
		}
	}
}
"""

q6 = """
SELECT ?num
WHERE{
    ?course ex:cSubject "SOEN".
    ?course ex:cNum "321".
    ?lec ex:assoCourse ?course. 
	?lec ex:lecNumber ?num .
    ?lec ex:lecContent ?content .
    ?content ex:contentTopic ?topic .
	?topic dc:subject ?topic_name .
	FILTER(regex(?topic_name, "RSA", "i"))
}
"""

qres = g.query(q6)
for res in qres:
    print(res)