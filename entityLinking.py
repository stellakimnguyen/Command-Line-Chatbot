from tika import parser
import spotlight
import json
import os


def parse_all_documents(localdir):
    # going through subfolders
    subdirs = [x[0] for x in os.walk(localdir)]
    for subdir in subdirs:
        files = os.walk(subdir).__next__()[2]
        if (len(files) > 0):
            for file in files:
                # parse pdf documents into txt
                parsed = parser.from_file(os.path.join(subdir, file))
                # calling spotlight api
                annotations = spotlight.annotate('https://api.dbpedia-spotlight.org/en/annotate?text=',
                                                 parsed["content"], confidence=0.9)
                # create json file
                file_object = open(os.path.join(subdir, file).replace('pdf', 'json'),
                                   "w+")
                # write spotlight response to json file
                file_object.write(json.dumps(annotations))


def main():
    parse_all_documents('universities\\Concordia University')


if __name__ == "__main__":
    main()
