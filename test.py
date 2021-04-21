import tika
import requests
from tika import parser
import spotlight
import json
import os


def list_files(localdir):
    r = []
    subdirs = [x[0] for x in os.walk(localdir)]
    for subdir in subdirs:
        files = os.walk(subdir).__next__()[1]
        if (len(files) > 0):
            for file in files:
                r.append(os.path.join(subdir, file))
    return r


# parsed = parser.from_file('universities/Concordia University/COMP474/Week 1/Lectures/Slides/slides01.pdf')
# annotations = spotlight.annotate('https://api.dbpedia-spotlight.org/en/annotate?text=', parsed["content"])

# Loop 1: Course

# Loop 2: Week/Outline
# Loop 3: Lecture/Labs/Tutorials
# Loop 4: Content (Slides/Worksheets/Instructions)

# File_object = open("universities/Concordia University/COMP474/Week 1/Lectures/Slides/slides01.json", "w+")
# File_object.write(json.dumps(annotations))

def main():
    print(list_files('universities\\Concordia University'))


if __name__ == "__main__":
    main()
