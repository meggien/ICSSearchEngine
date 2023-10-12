import time
from pathlib import Path
from index import Index
from search import Search


def readPositionRecord(input_file : str) -> dict:
    position_record = dict() # {term(str) : pos(int)}
    with open(input_file, 'r') as file:
        line = file.readline()
        position_record = eval(line.rstrip())

    return position_record


if __name__ == "__main__":
    path = Path("/Users/meggie/Downloads/DEV") 

    # asks user if they want to build inverted index
    index1 = Index(path)
    build_index = input("Do you want to build the index? (y to build)  ")
    if build_index == "y" or build_index == "Y":
        index1._build()

    print("Loading...")
    
    pos_record = readPositionRecord("position_record.txt")
    pos_record2 = readPositionRecord("position_record2.txt")
    pos_record3 = readPositionRecord("position_record3.txt")
    
    
    query = input("Enter query (q to quit) -->  ") # taking input line as a string

    while query != "q":
        start_time = time.time()
            
        try:
            search1 = Search("tfIDF", pos_record, pos_record2, pos_record3, query)
            pages = [index1.geturlID(id) for _, id in search1.getPages()]

            t = time.time() - start_time
        
            print("Top 5 results:")
            for p in pages:
                print(p)
            
            print("My program took", t, "s to run")
        except:
            print("Bad input, try again")

        query = input("Enter query (q to quit) -->  ")
