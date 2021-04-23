import os
import pathlib
import json

course_key = {
    'COMP474': {
        'code': 'ex:5484',
        'cName': 'Intelligent Systems',
        'cSubject': 'COMP',
        'cNum': '474',
        'seeAlso': '<https://moodle.concordia.ca/moodle/course/info.php?id=122223>'
    },
    'SOEN321': {
        'code': 'ex:32005',
        'cName': 'Information Systems Security',
        'cSubject': 'SOEN',
        'cNum': '321',
        'seeAlso': '<https://moodle.concordia.ca/moodle/course/view.php?id=132738#section-1>'
    }
}

lec_key = {
    'Slides': 'ex:lecContentSlide',
    'Worksheets': 'ex:lecContentWorksheets',
    'Readings': 'ex:lecContentReadings',
    'Other': 'ex:lecContentOther',
    'seeAlso': 'https://moodle.concordia.ca/moodle/course/view.php?id=132738#section-'
}

event_key = {
    'Slides': 'ex:eventContentSlides',
    'Instructions': 'ex:eventContentInstructions' 
}

def remove_special_chars(text):
    return ''.join(c for c in text if c.isalnum())

def write_triple(triple, op):
    with open("generated_triples.ttl", op) as f:
        f.write(triple)

def write_prefixes():
    prefixes = """@prefix rdfs: <https://www.w3.org/2000/01/rdf-schema#> .
@prefix rdf: <https://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <https://www.w3.org/2001/XMLSchema#> .
@prefix foaf: <https://xmlns.com/foaf/0.1/> .
@prefix dbo: <https://dbpedia.org/ontology/> .
@prefix dbr: <https://dbpedia.org/resource/> .
@prefix ex: <http://example.org/>.
@prefix dc: <http://purl.org/dc/terms/>.
"""

    write_triple(prefixes, "w")

topics_set = set()
def add_topics(path):
    global topics_set
    
    topics = {}
    with open(path + ".json") as f:
        data = json.load(f)
        for field in data:
            if field['percentageOfSecondRank'] == 0.0:
                topics.update({field['surfaceForm']: field['URI']})
                    
        topic_triple = ""
        for topic in topics:
            topic_name = "ex:" + remove_special_chars(topic)
            topic_uri = topics[topic].replace("http://dbpedia.org/resource/", "dbr:")

            if topic_name not in topics_set:
                topics_set.add(topic_name)
                topic_class = f'''
    {topic_name}
        a ex:topic ;
        dc:subject "{topic}" ;
        dc:URI {topic_uri if "'" not in topic_uri and "(" not in topic_uri and "." not in topic_uri else "<" + topics[topic] + ">"} .
                '''
                write_triple(topic_class, "a")

            topic_triple += f"\tex:contentTopic {topic_name} ; \n"

        return topic_triple

def get_uri(path, content):
    cont_name, _ = content.split(".")
    full_path = f"{path}\\{cont_name}"
    path_in_uri = pathlib.Path(os.path.abspath(full_path + ".pdf")).as_uri()
    content_name = "ex:" + remove_special_chars(cont_name)
    no_topics = add_topics(full_path)
    topics = no_topics[:no_topics.rfind(";")] + ".\n"
    
    uri = f"""
{content_name}
    a ex:content ;
    foaf:Document <{path_in_uri}> ;
{topics}"""

    write_triple(uri, "a")

    return content_name

def write_courses(files, course_course_key):
    outline = pathlib.Path(os.path.abspath(files[0] + "\\" + files[2][1])).as_uri()
    course = f"""
{course_key[course_course_key]['code']}
    a ex:Course ;
    ex:cName "{course_key[course_course_key]['cName']}" ;
    ex:cSubject "{course_key[course_course_key]['cSubject']}" ;
    ex:cNum "{course_key[course_course_key]['cNum']}" ;
    ex:Description "..." ;
    ex:cOutline <{outline}> ;
    rdfs:seeAlso {course_key[course_course_key]['seeAlso']} .
    """

    write_triple(course, "a")

lecture = ""
def write_lectures(files, course_course_key, path_name, week):
    global lecture

    content_name = get_uri(files[0], files[2][1])
    if previous_week_lec != week:
        if lecture != "":
            lecture = lecture[:lecture.rfind(";")] + ".\n"
            write_triple(lecture, "a")

        _, week_num = week.split(" ")
        see_also = "\n\trdfs:seeAlso <" + lec_key['seeAlso'] + week_num + "> ;" if course_course_key == "COMP474" else ""
        lecture = f"""
{course_key[course_course_key]['code']}_Lec_{week_num}  
    a ex:Lecture ;
    ex:assoCourse {course_key[course_course_key]['code']} ;
    ex:lecNumber "{week_num}"^^xsd:integer ;
    ex:lecName "{files[2][1]}" ; {see_also}
    ex:lecContent {content_name} ;
    {lec_key[path_name]} {content_name} ;"""
    else:
        lecture += f"""
    ex:lecContent {content_name} ;
    {lec_key[path_name]} {content_name} ;"""

event = ""
def write_event(files, course_course_key, path_name, week, event_name):
    global event

    content_name = get_uri(files[0], files[2][1])
    if previous_week_event != week:
        if event != "":
            event = event[:event.rfind(";")] + ".\n"
            write_triple(event, "a")

        _, week_num = week.split(" ")
        event = f"""
{course_key[course_course_key]['code']}_{event_name}_{int(week_num) - 1}  
    a ex:{event_name} ;
    ex:assoLec {course_key[course_course_key]['code']}_Lec_{week_num} ;
    ex:lecContent {content_name} ;
    {event_key[path_name]} {content_name} ;"""
    else:
        event += f"""
    ex:lecContent {content_name} ;
    {event_key[path_name]} {content_name} ;"""

# ======================== MAIN ========================
write_prefixes()

subdirs = [x[0] for x in os.walk('universities\\Concordia University')]
previous_week_lec = None
previous_week_event = None

for subdir in subdirs:
    files = os.walk(subdir).__next__()

    if len(files[2]):
        paths = files[0].split('\\')
        path_name = paths[-1]
        # Check if we are in a lecture/tutorial/etc or an outline
        if path_name == "Outline":
            write_courses(files, paths[2])
        else:
            path_type = paths[-2]
            if path_type == "Lectures":
                write_lectures(files, paths[2], path_name, paths[3])
                previous_week_lec = paths[3]
            elif path_type == "Labs":
                test = write_event(files, paths[2], path_name, paths[3], "Lab")
                previous_week_event = paths[3]
            elif path_type == "Tutorial":
                test = write_event(files, paths[2], path_name, paths[3], "Tutorial")
                previous_week_event = paths[3]