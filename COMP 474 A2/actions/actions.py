# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
'''
import rdflib
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
#
#
class ActionHelloWorld(Action):
#
     def name(self) -> Text:
        return "action_hello_world"
#
     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         dispatcher.utter_message(text="Hello World!")

         return []

class ActionCourseAbout(Action):

class ActionTopic(Action):

class ActionTopics(Action):
'''

from rdflib import Graph
import rdflib.plugins.sparql as sparql

g_triples = Graph()
g_triples.parse("triples.ttl", format="turtle")


g_manual_triples = Graph()
g_manual_triples.parse("manual_triples.ttl", format="turtle")


g_merged_triples = Graph()
g_merged_triples.parse("merged_triples.ttl", format="turtle")



g_schema = Graph()
g_schema.parse("schema.ttl", format="turtle")



g_merged_triples_schema = g_merged_triples + g_schema

g_all_triples = g_merged_triples_schema + g_manual_triples


def q1():

    q1 = g_manual_triples.query(
        '''
    PREFIX xsd: <https://www.w3.org/2001/XMLSchema#> 

 
    SELECT ?topic
    WHERE {
        ?course ex:cSubject "COMP".
        ?course ex:cNum "474".
        ?lec ex:assoCourse ?course.
        ?lec ex:LecNumber "2"^^xsd:integer.
        ?lec foaf:primaryTopic ?topic.
        }

        '''
        )

    for row in q1:
        print("%s" % row)


def q2():

    q2 = g_manual_triples.query(
        '''
        SELECT ?lecName
        WHERE {
            ?course ex:cSubject "COMP".
            ?course ex:cNum "474".
            ?lec ex:assoCourse ?course.
            ?lec ex:lecName ?lecName.

        }


        '''
        )
    response = ""
    for row in q2:
        response += ("%s" % row)
        response += "\n"
    return response



def q3():

    q3 = g_triples.query(
        '''
        SELECT ?cName
        WHERE{
        {
        ?course ex:cDescription ?description.
        FILTER(regex(?description, "crypto", "i")).
        ?course ex:cName ?cName.
        }
        UNION
        {
        ?course ex:cName ?name.
        FILTER(regex(?name, "crypto", "i")).
        ?course ex:cName ?cName.
        }
        }

        '''
        )

    for row in q3:
        print("%s" % row)

def q4():

    q4 = g_manual_triples.query(
        '''
        SELECT ?lab
        WHERE {
            ?course a ex:Course.
            ?course ex:cSubject "COMP".
            ?course ex:cNum "474".
            ?lab a ex:Lab .
            ?lab ex:assoLec ?lec .
            ?lec ex:assoCourse ?course .

        }


        '''
        )
    response = ""
    for row in q4:
        response += ("%s" % row)
        response += "\n"
    return response


def q5():

    q5 = g_triples.query(
        '''
        SELECT ?num
        WHERE {
            ?course ex:cSubject "SOEN".
            ?course ex:cNum "321".
            ?lec ex:assoCourse ?course.
            ?lec foaf:primaryTopic dbr:RSA.
            ?lec ex:lecNumber ?num
            }


        '''
        )

    for row in q5:
       print("%s" % row)


def q6():

    q6 = g_triples.query(
        '''
        SELECT DISTINCT ?lab
        WHERE {
            ?course a ex:Course .
            ?course ex:cSubject "SOEN".
            ?course ex:cNum "321".
            ?lab a ex:Lab .
            ?lab ex:assoLec ?lec .
            ?lec ex:assoCourse ?course .
            }


        '''
        )

    for row in q6:
        print("%s" % row)


def q7():

    q7 = g_triples.query(
        '''
        SELECT DISTINCT ?lab ?tut
WHERE
{
	{
		?course a ex:Course .
	?course ex:cSubject "COMP".
    	?course ex:cNum "474".
?lab a ex:Lab .
?lab ex:assoLec ?lec .
?lec ex:assoCourse ?course .
?lec ex:lecName ?lecname
FILTER(?lecname = "Knowledge Graphs") .
	}
UNION
{
	?course a ex:Course .
	?course ex:cSubject "COMP".
    	?course ex:cNum "474".
?tut a ex:Tutorial .
?tut ex:assoLec ?lec .
?lec ex:assoCourse ?course .
?lec ex:lecName ?lecname
FILTER(?lecname = "Knowledge Graphs") .
}
}

        '''
        )

    for row in q7:
        print("%s" % row)


def q8():

    q8 = g_triples.query(
        '''
SELECT DISTINCT ?course ?outline
WHERE {
{
	?course a ex:Course .
	?course ex:cSubject "COMP".
    	?course ex:cNum "474".
OPTIONAL { ?course ex:cOutline ?outline . }
	}
	UNION
	{
		?course a ex:Course .
	?course ex:cSubject "SOEN" .
    	?course ex:cNum "321" .
OPTIONAL { ?course ex:cOutline ?outline . }
	}
}


        '''
        )

    for row in q8:
        print("%s" % row)


def q9():

    q9 = g_triples.query(
        '''
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
?lec1 foaf:primaryTopic ?topic1 .

?course2 a ex:Course .
	?course2 ex:cSubject "SOEN".
    	?course2 ex:cNum "321".
?lec2 a ex:Lecture .
?lec2 ex:assoCourse ?course2 .
?lec2 foaf:primaryTopic ?topic2 .

FILTER(?topic1 = ?topic2) .
}
}
}

        '''
        )

    for row in q9:
        print("%s" % row)


def q10():

    q10 = g_triples.query(
        '''
SELECT DISTINCT ?slides
WHERE {
?course a ex:Course .
?course ex:cSubject "SOEN".
?course ex:cNum "321".
?lec a ex:Lecture .
?lec ex:assoCourse ?course .
?lec ex:lecNumber "2"^^xsd:integer .
?lec ex:lecContentSlide ?slides .
}


        '''
        )

    for row in q10:
        print("%s" % row)




#good
def q11():
    q11 = g_merged_triples.query(
        '''
        SELECT ?description
        WHERE {
            ?course ex:cSubject "COMP".
            ?course ex:cNum "474".
            ?course ex:cDescription ?description.
            }


        '''
        )
    response = ""
    for row in q11:
        response += ("%s" % row)
        
    return response

#which topics are covered in Lab#2 of COMP 474?
#query needs to be changed to match Lab#2 and extract topic        
def q12(name, cNum, num):
    q12 = g_manual_triples.query(
        '''
        PREFIX xsd: <https://www.w3.org/2001/XMLSchema#>   
        SELECT ?topic
        WHERE {
            ?course ex:cSubject "'''+name+'''".
            ?course ex:cNum "'''+cNum+'''".
            ?lec ex:assoCourse ?course.
            ?lec ex:LecNumber "'''+num+'''"^^xsd:integer.
            ?lec foaf:primaryTopic ?topic.
            }


        '''
        )
    response = ""
    for row in q12:
        response += ("%s" % row)
        response += "\n"
    return response
    

def q13():
    q13 = g_merged_triples_schema.query(
        '''
        SELECT DISTINCT ?cName
        WHERE{
            {
                ?course ex:cDescription ?description.
                FILTER(regex(?description, "Expert Systems", "i")).
                ?course ex:cName ?cName.

                }
            UNION
            {
                ?course ex:cName ?name.
                FILTER(regex(?name, "Expert Systems", "i")).
                ?course ex:cName ?cName.
                
                }
            }

        '''
        )
    response = ""
    for row in q13:
        response += ("%s" % row)
        
    return response









from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionCourseAbout(Action):
    
    
    def name(self) -> Text: 
        return "action_course_about"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        for word in tracker.latest_message['entities']:
            if word['entity'] == 'courses':
                response = q11()
                dispatcher.utter_message(text = response)
   
class ActionTopics(Action):
    
    def name(self) -> Text:
        return "action_topics"
    
    def run(self, dispatcher: CollectingDispatcher, tracker:Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         #counter = 0
         name = ""
         cNum = ""
         num = ""
         for word in tracker.latest_message['entities']:
             if word['entity'] == 'course_event':
                 num = word['value'][-1]
             if word['entity'] == 'courses':
                 split = word['value'].split(' ')
                 name = split[0]
                 cNum = split[1]
         response = q12(name, cNum, num)
         dispatcher.utter_message(text = response)
             #print(word)
             #if word['entity'] == 'courses':
                 #dispatcher.utter_message(text = "test1")
                 #counter += 1
                 
             #if word['entity'] == 'courses':
              #   counter += 1
        
         #if counter == 2:
             #response = q12()
             #dispatcher.utter_message(text = "yezzirrr")
   
     
class ActionTopic(Action):
    
    def name(self) -> Text:
        return "action_topic"

    def run(self, dispatcher: CollectingDispatcher, tracker:Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         for word in tracker.latest_message['entities']:
             if word['entity'] == 'topic':
                 response = q13()
                 dispatcher.utter_message(text = response)



class ActionLecOff(Action):
    def name(self) -> Text:
        return "action_lec_off"
    
    def run(self, dispatcher: CollectingDispatcher, tracker:Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        for word in tracker.latest_message['entities']:
            if word['entity'] == 'courses':
                response = q2()
                dispatcher.utter_message(text = response)



class ActionAnyLab(Action):
    def name(self) -> Text:
        return "action_any_lab"
    
    def run(self, dispatcher: CollectingDispatcher, tracker:Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        for word in tracker.latest_message['entities']:
            if word['entity'] == 'courses':
                response = q4()
                dispatcher.utter_message(text = response)

#q12("COMP", "474")
