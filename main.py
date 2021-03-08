# Web Scraper for Project Gutenberg
# By: Shayon Ghoshroy
# --USAGE--
#

import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import os
import re
import os.path
from os import path
import matplotlib.pyplot as plt
import re
import nltk

HOME = "http://www.gutenberg.org"
URL = "http://www.gutenberg.org/ebooks/"
SEARCH = "http://www.gutenberg.org/ebooks/search/?query="
BY_POPULARITY_SEARCH_SUFFIX = "&submit_search=Go%21"
INSIG_TAGS = ['DT', 'CC', 'PDT', 'WDT', 'PRP', 'TO', 'PRP$', 'IN', 'WRB', 'WP$', 'WP' ]


def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")


def download_from_id(id):
    url = URL + id
    soup = get_soup(url)
    for a_tag in soup.findAll('a'):  # 'a' tags are for links
        link = a_tag.get("href")
        if link is not None:
            if ".txt" in link:
                name = "ebooks/" + id + ".txt"
                if not path.exists(name):
                    os.system("wget --output-document " + name + " " + HOME + link)


def download_from_name(name):
    name = name.replace(" ", "+")
    url = SEARCH + name + BY_POPULARITY_SEARCH_SUFFIX
    soup = get_soup(url)
    for a_tag in soup.findAll('a'):  # 'a' tags are for links
        link = a_tag.get("href")
        if link is not None:
            if "/ebooks/" in link and bool(re.search(r'\d', link)) and link.count("/", 0, len(link)) == 2:
                id = re.search(r'\d+', link).group()
                download_from_id(id)


def download_all():
    os.system("wget -w 2 -m -H \"http://www.gutenberg.org/robot/harvest?filetypes[]=txt\"")


def word_count(id):
    with open("ebooks/" + id + ".txt", "r") as file:
        str = file.read().replace('\n', '')
    counts = dict()
    words = str.split()
    print("counting words...")
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    counts = {k: v for k, v in sorted(counts.items(), key=lambda item: item[1])}  # sort by words

    # filter out POS
    print("filtering out parts of speech:", INSIG_TAGS)
    for key in list(counts):
        if get_part_of_speech(key) in INSIG_TAGS:
            del counts[key]

    print("removing words occurring less than 200 times")
    # remove words that occur less than 200 times
    for key in list(counts):
        if counts[key] < 200:
            del counts[key]

    print("loading bar chart...")
    fig = plt.figure(1, [25, 8])
    plt.bar(range(len(counts)), counts.values(), align='center')
    plt.xticks(range(len(counts)), list(counts.keys()))
    plt.show()


def get_part_of_speech(word):
    tokenized = nltk.word_tokenize(word)
    tagged = nltk.pos_tag(tokenized)
    word, tag = tagged[0]
    return tag


def main():
    #download_from_name(input("Enter e-book name: "))
    #download_from_id(input("Enter e-book ID: "))
    #download_all()
    word_count(input("Enter e-book ID: "))
    #get_pos("which")
    return


main()

