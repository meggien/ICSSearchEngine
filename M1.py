from pathlib import Path
from collections import defaultdict
import sys
from index import Index


if __name__ == "__main__":
    path = Path("/Users/meggie/Downloads/DEV")
    index1 = Index(path)
    
    # for key, value in index1._URLid.items(): ### testing
    #     print(key + " : " + str(value))

    # for report
    print(len(index1.getInvertedIndex()), "unique tokens")
    print(len(index1.geturlID()), "unique documents")
    print("index total size is", (sys.getsizeof(index1.getInvertedIndex()) / 1000), "KB")