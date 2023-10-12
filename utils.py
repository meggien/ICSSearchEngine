import re
import json
from bs4 import BeautifulSoup
from collections import defaultdict
from json.decoder import JSONDecodeError
from nltk.stem import PorterStemmer


def tokenize(clean_text: str) -> defaultdict:
    wordfinder = re.compile(r"([A-Za-z\d]+)") # regex equation to accept alphabetic chars and digits in the text file
    words = wordfinder.findall(clean_text) # finds matches in the line, can take longer depending on line size which means it runs on O(N) time, however, should be quicker than using against entire file
    ps = PorterStemmer()  

    # stemming all words with nltk Porter stemmer
    for i in range(len(words)):
        words[i] = ps.stem(words[i].lower())
    
    token_dict = defaultdict(int) # dict {token : freq}
    bigram_dict = defaultdict(int)
    trigram_dict = defaultdict(int)
    
    num_words = len(words)

    for i in range(num_words):
        token_dict[words[i]] += 1

        if num_words - i >= 2:
            bigram_dict[words[i] + ' ' + words[i+1]] += 1

        if num_words - i >= 3:
            trigram_dict[words[i] + ' ' + words[i+1] + ' ' + words[i+2]] += 1

    return token_dict, bigram_dict, trigram_dict


# reads json data from a file and turns it into a python dictionary
def read(filePath: str) -> dict:
    try:
        data_file = open(filePath, 'r')
        results = json.load(data_file)
    except FileNotFoundError:
        print('FAILED')
        print(filePath)
        print('MISSING')
        exit()
    except (json.decoder.JSONDecodeError) as error:
        print('FAILED')
        print(filePath)
        print('FORMAT')
        exit()
    else:
        data_file.close()
        return results


def parseHtml(html_content) -> str:
    soup = BeautifulSoup(html_content, 'lxml')
    for data in soup(['style', 'script']): # remove all html markup
        data.decompose() # remove tags

    # accumulate words in specific tags (title, heading, strong, b) as important words
    tags = re.compile('<.*?>')
    title = soup.find_all("title")
    for i in range(len(title)):
        title[i] = re.sub(tags, '', str(title[i])).strip()

    headings = soup.find_all(re.compile("^h[1-6]$"))
    for i in range(len(headings)):
        headings[i] = re.sub(tags, '', str(headings[i])).strip()

    strong = soup.find_all("strong")
    for i in range(len(strong)):
        strong[i] = re.sub(tags, '', str(strong[i])).strip()

    bold = soup.find_all("b")
    for i in range(len(bold)):
        bold[i] = re.sub(tags, '', str(bold[i])).strip()

    important = ' '.join(title + headings + strong + bold)
    
    return ' '.join(soup.stripped_strings), important