Module Structure:
*we have 3 of some files, bigram indexing has a 2 appended to the name and trigram
 indexing has a 3 appended (file_name/2/3)*

	main.py → runs program
	gui.py → desktop application built with Tkinter
	index.py → builds inverted index
	search.py → processes query terms and returns top 5 pages
	utils.py → deals with tokenization, opening and processing json and html content
	id_url_map.txt → holds dictionary of each URL's assigned integer ID to the URL
	position_record/2/3.txt → holds file positions of terms in bytes
	tfIDF/2/3.txt → holds tf-idf score of each term
	inverted_index/2/3.txt → merged files of inverted index
	inverted_index/2/3 → folder of partial indexes
		inverted_index1.txt
		inverted_index2.txt
		...

Installation:
	install BeautifulSoup, NLTK, and Tkinter packages before running program
		a. BeautifulSoup is used to parse the json files
		b. NLTK is used to stem tokens with PorterStemmer
		c. Tkinter is used for implementing graphical user interface

How to Use: Console
	1. Open main.py and run the program
	2. A prompt will show up asking if the user wants to build the index, type "y"
	   into the terminal if they want it to be built (otherwise click enter), once
	   it is done building the program will continue
			a. index.py will be called upon and it will call on utils.py to
			   tokenize and parse through the content 
			b. id_url_map.txt is built and a folder of all the inverted_index files
			c. All the inverted_index files will be merged into inverted_index.txt
			d. The tf-idf score will be calculated and placed into tfIDF.txt
			e. The location of each term will be written to position_record.txt
	3. Otherwise, the program will assume the index is already built and continue,
	   “Loading…” should appear
	4. Wait until the “Enter query  (q to quit)” prompt to appear, then type query
	   and press return to start searching
			a. position_record.txt is read prior
	5. Type in your query
			a. search.py is called upon
	6. Boom! The top 5 pages are printed out :D


How to Use: GUI
	1. Open gui.py and run the program
	2. Wait for the launcher to load
	3. Once the launcher opens, type in your query and hit the “Search” button
	4. Yay! The top 5 pages are displayed below :D
		a. If the query does not exist in the database, it will display "Bad input.
		   Try again” and you can re-enter a new query
