import os
import math
from pathlib import Path
from collections import defaultdict
from sys import getsizeof
from utils import read, parseHtml, tokenize

# Index builds the inverted index using partial indexes (later merging into a single larger file), 
# computes the tf-idf scores for each token, stores the position of each token and the ID of each URL
class Index:
    def __init__(self, path: Path) -> None:
        self._path = path
        # whole index should not be stored as member variable in index class    
        self._inverted_index = defaultdict(dict) # {token : {web1_id: f1, web2_id: f2, web3_id: f3, ...}}
        self._inverted_index2 = defaultdict(dict)
        self._inverted_index3 = defaultdict(dict)
        self._URLid = dict() # {id(int) : url}
        self._doc_counter = 1

        with open("id_url_map.txt", 'r') as file:
            self._URLid = eval(file.readline())


    # building inverted index dictionary
    def _build(self) -> None:
        index_counter = 1 # for numbering the partial index files
        index_counter2 = 1
        index_counter3 = 1
        
        for subdomains in self._path.iterdir():
            page_val_set = set() # stores values corresponding to the page content (for checking for duplicates)
            try:
                for file in subdomains.iterdir():
                    file_extension = Path(file).suffix
                    if file_extension == ".json": # take suffix and check it is JSON so that we can read
                        json_dict = read(file)
                        str_content, important_tokens = parseHtml(json_dict['content']) # retrieve content of file
                        token_dict, bigram_dict, trigram_dict = tokenize(str_content.lower()) # tokenize content
                        
                        if len(token_dict) != 0: # deals with bad html pages with no content
                            page_val = len(str_content)/len(token_dict) # value corresponding to page content

                            # if the value is already in the set, the page isn't added because it's a duplicate
                            if page_val not in page_val_set: 
                                page_val_set.add(page_val)

                                # content marked with header, bold, and strong html tags
                                important_tokens_dict, important2, important3 = tokenize(important_tokens)

                                self._URLid[self._doc_counter] = json_dict['url'] # assign url to id

                                # assigning score to each token
                                for token in token_dict:
                                    # token_dict is originally {token : frequency}
                                    # giving a higher ranking to the important content
                                    if token in important_tokens_dict:
                                        token_dict[token] += 1
                                    tf_score = 1+math.log10(token_dict[token])
                                    
                                    # inverted index -> {token : {doc1: tf1, doc2: tf2}, ...}
                                    self._inverted_index[token][self._doc_counter] = tf_score
                                
                                for token in bigram_dict:
                                    if token in important2:
                                        bigram_dict[token] += 1
                                    tf_score = 1+math.log10(bigram_dict[token])
                                    
                                    self._inverted_index2[token][self._doc_counter] = tf_score

                                for token in trigram_dict:
                                    if token in important3:
                                        trigram_dict[token] += 1
                                    tf_score = 1+math.log10(trigram_dict[token])
                                    
                                    self._inverted_index3[token][self._doc_counter] = tf_score
                                
                                self._doc_counter += 1 # counting total number of documents
            
                    # 10 MB: 10_000_000
                    # if the index size exceeds 10 MB, dump the current index contents to a file (partial indexes)
                    if (getsizeof(self._inverted_index) > 10_000_000): # 10 MB
                        self._writeToDisk(self._inverted_index, "inverted_index" + str(index_counter) + ".txt", os.getcwd() + "/inverted_index/")
                        self._inverted_index = defaultdict(dict)
                        index_counter += 1

                    if (getsizeof(self._inverted_index2) > 10_000_000): # 10 MB
                        self._writeToDisk(self._inverted_index2, "inverted_index2_" + str(index_counter2) + ".txt", os.getcwd() + "/inverted_index2/")
                        self._inverted_index2 = defaultdict(dict)
                        index_counter2 += 1
                    
                    if (getsizeof(self._inverted_index3) > 10_000_000): # 10 MB
                        self._writeToDisk(self._inverted_index3, "inverted_index3_" + str(index_counter3) + ".txt", os.getcwd() + "/inverted_index3/")
                        self._inverted_index3 = defaultdict(dict)
                        index_counter3 += 1
                
            except:
               continue
        
        self._writeToDisk(self._inverted_index, "inverted_index" + str(index_counter) + ".txt", os.getcwd() + "/inverted_index/")
        self._writeToDisk(self._inverted_index2, "inverted_index2_" + str(index_counter2) + ".txt", os.getcwd() + "/inverted_index2/")
        self._writeToDisk(self._inverted_index3, "inverted_index3_" + str(index_counter3) + ".txt", os.getcwd() + "/inverted_index3/")
        
        # writing the {id: url} dictionary in one line to the file
        with open("id_url_map.txt", 'w') as file:
            file.write(str(self._URLid))
        
        self.mergeIndex("inverted_index", "inverted_index.txt")
        self.mergeIndex("inverted_index2", "inverted_index2.txt")
        self.mergeIndex("inverted_index3", "inverted_index3.txt")
        self._calculateIDF("inverted_index.txt", "tfIDF.txt")
        self._calculateIDF("inverted_index2.txt", "tfIDF2.txt")
        self._calculateIDF("inverted_index3.txt", "tfIDF3.txt")
        self._writePositionRecord("tfIDF.txt", "position_record.txt")
        self._writePositionRecord("tfIDF2.txt", "position_record2.txt")
        self._writePositionRecord("tfIDF3.txt", "position_record3.txt")
    
    
    # calculates IDF score and threshold for each token in the inverted index file, writing these to the tfIDF file
    def _calculateIDF(self, index_file_name : str, tfIDF_file_name : str):
        with open(index_file_name, 'r') as file1:
            with open(tfIDF_file_name, "w+") as file2:
                for line in file1:
                    dic = eval(line[line.find(':')+1:].rstrip())
                    num_docs = len(dic)
                
                    if num_docs == 0:
                        num_docs = 1

                    # IDF(t) = log_e(Total number of documents / Number of documents with term t in it)
                    IDF = math.log10(self._doc_counter/num_docs) 
                    for k in dic.keys():
                        dic[k] *= IDF
                    
                    list1 = sorted(dic.values(), reverse=True)

                    # setting threshold for 1 word index
                    if index_file_name[-5] == 'x':
                        if len(list1) > 20:
                            k = 20
                        else:
                            k = len(list1) - 1
                    
                    # setting threshold for bigram and trigram index
                    else:
                        if len(list1) // 8 < 30: # cutoff at 240 pages
                            k = len(list1)-1
                        else:
                            k = len(list1) // 10 # sets threshold to top 10% of pages
                   
                    if len(list1) == 0:
                        threshold = 0
                    else:
                        threshold = list1[k]
                        
                    # index -> token-t:{tfidf}
                    file2.write(f"{line[:line.find(':')]}-{threshold}:{dic}\n") # {token: tfidf score}


    # writes partial indexes to disk (within inverted index directory)
    def _writeToDisk(self, inverted_index: dict, filename : str, directory: str):
        if not os.path.exists(directory):
            os.mkdir(directory)
            
        with open(directory + filename, 'w') as f:
            for token in sorted(inverted_index.keys()):
                f.write(f"{token}:{inverted_index[token]}\n")
    

    # writes position of each token to position_record file, in this format {term(token) : position(in bytes)}
    def _writePositionRecord(self, input_file : str, output_file : str):
    # tokenize these fewer pages,looking for words next to e/o
        position_record = dict()
        with open(input_file, 'r') as file:
        # first term
            counter = file.tell()
            line = file.readline()
            while line:
                position_record[line[:line.find('-')]] = counter
                counter = file.tell()
                line = file.readline()

        # write location_record to file
        with open(output_file, 'w') as f:
            f.write(str(position_record))
    
    
    # merges partial indexes together, writing to a larger single file
    def mergeIndex(self, index_dir : str, index_file_name : str):
        directory = os.getcwd() + "/" + index_dir
        file_lst = []
        for file in os.listdir(directory):
            file_extension = Path(file).suffix
            if file_extension != ".DS_Store":
                file_lst.append(open(directory+"/"+file, 'r'))
        
        # min term is the term among partial indexes that comes first in alphabetical order
        min_term = ""
        file_pos_lst = [0] * len(file_lst) # keep track of file positions
        with open(index_file_name, 'w') as resulting_file:
            while (file_lst):
                
                # first iteration finds min term
                for i, file in enumerate(file_lst): 
                    file_pos_lst[i] = file.tell()
                    try:
                        line = file.readline().rstrip()

                        # if reached EOF, remove
                        if (line == ""):
                            file.close()
                            file_lst.pop(i)
                            file_pos_lst.pop(i)
                        else:
                            term = line[:line.find(':')]

                            if (i == 0):
                                min_term = term
                            elif term < min_term:
                                min_term = term
                            
                            # move file position back by one line
                            file.seek(file_pos_lst[i])
                    except Exception as e:
                        continue          
                
                # accumulate posting lists associated with min term
                min_term_entry = dict()
                for i, file in enumerate(file_lst):
                    try:
                        line = file.readline().rstrip()
                        term = line[:line.find(':')]
                        
                        if (term == min_term):
                            min_term_entry.update(eval(line[line.find(':')+1:]))
                        else:
                            file.seek(file_pos_lst[i])
                    except:
                        continue
                resulting_file.write(f"{min_term}:{min_term_entry}\n")


    # Return the url associated with the id given
    def geturlID(self, id : int) -> str:
        return self._URLid[id]
