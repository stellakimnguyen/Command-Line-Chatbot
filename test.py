import tika
from tika import parser
import spotlight

parsed = parser.from_file('universities/Concordia University/COMP474/Week 1/Lectures/Slides/slides01.pdf')
annotations = spotlight.annotate('http://spotlight.dbpedia.org/rest/', parsed["content"], confidence=0.4, support=20)

# print(parsed["metadata"])
# print(parsed["content"])
# File_object = open("slides1.txt", "w+")
# File_object.write(parsed["content"])