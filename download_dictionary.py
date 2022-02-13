# Dependency
# pip3 install BeautifulSoup
# pip3 install lxml
# pip3 install nltk
# then
# python3
# import nltk
# nltk.download("words")

from bs4 import BeautifulSoup
import requests
import multiprocessing
import sys
import enchant
from nltk.corpus import words

url_dictionary = "https://www.englishtools.org/en/find-english-words-by-length/any"
def visit_website(url): # It will return BeautifulSoup
    response = requests.get(url)
    if response.status_code != requests.codes.ok:
        print("Cannot visit the website.")
        return 
    html_content = response.text
    soup = BeautifulSoup(html_content, features = 'lxml')
    return soup

def download_words(word_pool, word_len, page):
    print(f"Downloading... Word length: {word_len}, Page: {page}")
    d = enchant.Dict("en_US")
    url = url_dictionary + f"/{word_len}/{page}"
    soup = visit_website(url)
    words_list = soup.find_all('td')
    for word in words_list:
        if word.text == "No results found.":
            print("Finish Downloading the words.")
            return 
        if d.check(word.text):
            word_pool.append(word.text)
def get_word_pool(word_len):
    url = url_dictionary + f"/{word_len}/1"
    word_pool = multiprocessing.Manager().list()
    soup = visit_website(url)
    last_page = str()
    for char in soup.find(class_ = "last").find("a")["href"][::-1]:
        try:
            checker = int(char)
            last_page = char + last_page
        except:
            last_page = int(last_page)
            break
    multiprocessing_arguments = list()
    for i in range(last_page):
        multiprocessing_arguments.append((word_pool, word_len, i+1))
    # arguments for download_words
    #print(multiprocessing_arguments)
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    pool.starmap(download_words, multiprocessing_arguments)
    return word_pool

def create_file(word_pool, word_len): # Let the other program read the words
    with open(f"./dictionary_{word_len}", 'w') as f:
        for index, word in enumerate(word_pool):
            if index != 0:
                f.write(",")
            f.write(word)
if __name__ == "__main__":
    try:
        word_len = sys.argv[1]
        print(f"***** Start download the WORDS: {word_len} *****")
        word_pool = get_word_pool(word_len)
        create_file(word_pool, word_len)
    except:
        print("***** Start download the WORDS *****")
        word_pool = get_word_pool(4)
        create_file(word_pool, 4)
        word_pool = get_word_pool(5)
        create_file(word_pool, 5)
        word_pool = get_word_pool(6)
        create_file(word_pool, 6)
    #print(word_pool)
    #print(len(word_pool))
