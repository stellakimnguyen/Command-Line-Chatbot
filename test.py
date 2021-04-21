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
        files = os.walk(subdir).__next__()[2]
        if (len(files) > 0):
            for file in files:
                r.append(os.path.join(subdir, file))
                parsed = parser.from_file(os.path.join(subdir, file))
                annotations = spotlight.annotate('https://api.dbpedia-spotlight.org/en/annotate?text=',
                                                 parsed["content"])
                File_object = open(os.path.join(subdir, file).replace('pdf', 'json'),
                                   "w+")
                File_object.write(json.dumps(annotations))
    return r

# Loop 1: Course

# Loop 2: Week/Outline
# Loop 3: Lecture/Labs/Tutorials
# Loop 4: Content (Slides/Worksheets/Instructions)

def main():
    print(list_files('universities\\Concordia University'))


if __name__ == "__main__":
    main()
