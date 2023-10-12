import heapq
from nltk.stem import PorterStemmer


# Search pocesses a query andearches or the most relevant documents, returning them with public method getPages
class Search:
    '''reates a Search object
    inverted_index_file_name: name of the built index file
    position_record: dictionary of each single token's position in the inverted index
    position_record2: dictionary of each bigram token's position in the inverted index
    position_record3: dictionary of each trigram token's position in the inverted index
    query: user's query '''
    def __init__(self, inverted_index_file_name : str, position_record : dict, position_record2 : dict, position_record3 : dict, query : str) -> None:
    
        query_length = len(query.split())

        # deciding to use single/bigram/trigram indexes based on query length
        if query_length == 1:
            self._inverted_index_file = open(inverted_index_file_name + ".txt", 'r')
            self._position_record = position_record
        elif query_length == 2:
            self._inverted_index_file = open(inverted_index_file_name + "2.txt", 'r')
            self._position_record = position_record2
        else:
            self._inverted_index_file = open(inverted_index_file_name + "3.txt", 'r')
            self._position_record = position_record3
        
        query_terms = self._processQuery(query)        
        self._results_list = self._searchCommonPages(query_terms)
        
    
    # returns the term's position in the inverted_index file
    def _seekTerm(self, term : str) -> int:
        return self._position_record[term]


    # constructs a list of tuples (word, number of websites)
    def _processQuery(self, query : str) -> list:
        ps = PorterStemmer()
        query_words = [ps.stem(w) for w in query.split()]

        # assigning word_list based on amount of terms in query
        if len(query_words) == 1:
            w = query_words[0]
            word_list = [(w, len(self._readInvertedIndex(w)[0]))]
        elif len(query_words) == 2:
            w = query_words[0] + ' ' + query_words[1]
            word_list = [(w, len(self._readInvertedIndex(w)[0]))]

        elif len(query_words) >= 3:
            word_list = []
            for i in range(0, len(query_words)-2):
                w = query_words[i] + ' ' + query_words[i+1] + ' ' + query_words[i+2]
                word_list.append((w, len(self._readInvertedIndex(w)[0])))

        word_list.sort(key=lambda x: x[1]) # sorting by frequency, increasing
        return [w[0] for w in word_list]

    # reads inverted index file and returns pages and threshold
    def _readInvertedIndex(self, query : str) -> dict:
        offset = self._seekTerm(query)
        self._inverted_index_file.seek(offset)
        line = self._inverted_index_file.readline()
        # inverted index (example formatting) -> citol:{18410: 1.0, 28585: 1.0, 46592: 1.4771212547196624}
        pages = eval(line[line.find(':')+1:].rstrip()) # gets each term's list of docID/freq
        threshold = eval(line[line.find('-')+1:line.find(':')])
        return pages, threshold


    # returns a set of pages (IDs) where all query words are found
    def _searchCommonPages(self, sorted_query : list) -> dict:
        queries = sorted_query.copy()
        query1 = sorted_query.pop(0)        
        
        ind1, threshold1 = self._readInvertedIndex(query1)
        set1 = {pageID for pageID, tfidf in ind1.items() if tfidf >= threshold1} # all pages that contain the term
        
        # finding pages in common from the sets of each of the other query terms
        while len(sorted_query) > 0:
            query2 = sorted_query.pop(0)
            ind2, threshold2 = self._readInvertedIndex(query2)
            set2 = {pageID for pageID, tfidf in ind2.items() if tfidf >= threshold2}

            set1 = set1.intersection(set2)

        ranked_list = []

        # creating a heap to find the top 5 pages
        for pageID in set1:
            heapq.heappush(ranked_list, (sum([self._readInvertedIndex(q)[0][pageID] for q in queries]), pageID))
            if len(ranked_list) > 9: # break out of loop after getting 10 pages
                break
        
        return heapq.nlargest(5, ranked_list) # returning list of top 5 highest ranked pages
    
    
    # retrieves relevant pages based on search query
    def getPages(self) -> list:
        self._inverted_index_file.close()
        return self._results_list
