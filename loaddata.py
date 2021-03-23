universities_key = {
    "Class": "ex:University",
    "Name": "ex:uName",
    "Link": "ex:uLink"
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
                    triple += f"\t{universities_key[headers[i]]} {contents[i]} {';' if i < len(contents)-1 else '.'}\n"
        
        write_triple(triple)

def main():
    parse_universities_csv()
    # to add other functions

if __name__ == "__main__":
    main()