from requests.auth import HTTPBasicAuth
import requests
import pandas as pd
import json
import pyparsing as pp

universities_key = {
    "Class": "ex:University",
    "Name": "ex:uName",
    "Link": "ex:uLink"
}

courses_key = {
    "Class": "ex:Course",
    "Subject": "ex:cSubject",
    "Catalog": "ex:cNum",
    "Long Title": "ex:cName",
    "Outline": "ex:cOutline",
    "Description": "ex:cDescription",
    "University": "ex:fromUniversity",
}


def write_triple(triple):
    with open("triples.ttl", "a") as f:
        f.write(triple)


def parse_universities_csv():
    with open("./universities/Universities.csv") as f:
        lines = f.readlines()
        headers = lines[0].rstrip().split(",")

        for line in lines[1:]:
            contents = line.rstrip().split(",")
            triple = ""
            for i in range(len(contents)):
                if headers[i] == "Key":
                    triple += f"\nex:{contents[i]}\n"
                    triple += f"\ta {universities_key['Class']} ;\n"
                else:
                    temp = contents[i]
                    if headers[i] == "Name":
                        temp = "\"" + contents[i] + "\""
                    triple += f"\t{universities_key[headers[i]]} {temp} {';' if i < len(contents) - 1 else '.'}\n"

        write_triple(triple)


def parse_courses_csv(university):
    url = "https://opendata.concordia.ca/API/v1/course/description/filter/"
    auth = HTTPBasicAuth('408', '018841334459b6c95023edc6dffbd8d7')

    col_list = ["Course ID", "Subject", "Catalog", "Long Title", "Component Code"]
    df = pd.read_csv("./universities/CU_SR_OPEN_DATA_CATALOG.csv", usecols=col_list,
                     encoding="ISO-8859-1")
    courses = df[df['Component Code'] == 'LEC'].drop_duplicates('Course ID', keep='last')
    courses['Description'] = ""
    courses['University'] = university

    courses.to_csv("./universities/allcourses.csv")

    with open("./universities/allcourses.csv") as i:
        lines = i.readlines()
        headers = lines[0].rstrip().split(",")
        for line in lines[1:]:
            contents = line.rstrip()
            contents = pp.commaSeparatedList.parseString(contents).asList()  # doesn't split the commas within quotes
            req = requests.get(url + contents[1].zfill(6), auth=auth)
            contents[-2] = (json.loads(req.content)[0]['description']).replace('\n', '\\n').replace('\"', '\\"').replace('\r', ' ')

            triple = ""

            for j in range(len(contents)):
                if j == 0 or j == 5:    # skipping identifier columns
                    continue
                if headers[j] == "Course ID":
                    triple += f"\nex:{contents[j]}\n"
                    triple += f"\ta {courses_key['Class']} ;\n"
                else:
                    if j == 4 or j == 7:
                        # avoid duplicate quotation marks in course title
                        contents[j] = contents[j].strip('\"').replace('\"', "\'").replace('\r', ' ')
                    temp = "\"" + contents[j] + "\""
                    triple += f"\t{courses_key[headers[j]]} {temp} {';' if j < len(contents) - 1 else '.'}\n"
            write_triple(triple)

def main():
    parse_universities_csv()
    parse_courses_csv("ex:Concordia_University")
    # to add other functions


if __name__ == "__main__":
    main()
