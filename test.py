import tika
import requests
from tika import parser
import spotlight
import json

parsed = parser.from_file('universities/Concordia University/COMP474/Week 1/Lectures/Slides/slides01.pdf')
# url = "https://api.dbpedia-spotlight.org/en/annotate?text="
# print(url)
# req = requests.get(url)
annotations = spotlight.annotate('https://api.dbpedia-spotlight.org/en/annotate?text=', parsed["content"])
# annotations = spotlight.annotate('http://localhost/rest/annotate', parsed["content"], confidence=0.4, support=20)

# print(parsed["metadata"])
# print(parsed["content"])
File_object = open("universities/Concordia University/COMP474/Week 1/Lectures/Slides/slides01.json", "w+")
File_object.write(json.dumps(annotations))