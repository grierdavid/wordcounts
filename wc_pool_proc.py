#!/usr/bin/python
import os
import urllib
import operator
import time
from multiprocessing import Process, Pool, Manager, Array
from multiprocessing.managers import BaseManager


#url = 'http://www.gutenberg.org/cache/epub/25990/pg25990.txt'
#f = urllib.urlopen(url)

manager_address = 'localhost'

f = open('pg25990.txt')

def info(title):
    print title
    print 'module name:', __name__
    if hasattr(os, 'getppid'):
        print 'parent process:', os.getppid()
    print 'process id:', os.getpid()

def m_word_list(file):
    info('server word_list function')
    words = manager.list()
    words.append(f.read().split())
    return words

def c_word_list(file):
    info('client word_list function')

def m_cleanup(words):
    info('cleanup function')
    only_words = manager.list()
    symbols = "~!@#$%^&*()_+=-{}\|\\][:\"\';<>?/.,"
    for word in words:
        for i in range(0, len(symbols)):
            word = word.replace(symbols[i], "")
        if len(word) != 0:
            only_words.append(word)
    return only_words

def c_cleanup(words):
    info('cleanup function')

def m_word_dict(clean):
    info('word_dict function')
    word_count = manager.dict()
    return word_count

def c_word_dict(clean):
    info('word_dict function')
    for word in clean:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count

def top_ten(wordcount):
    for key, value in sorted(word_count.items(), key=operator.itemgetter(1), reverse=True)[:10]:
        print key, value

def wordcount(f):
    words = word_list(f)
    clean = cleanup(words)
    word_dict(clean)

if __name__ == '__main__':
    manager = Manager()
    word_list = m_word_list(f) 
#    clean_list = manager.list(m_cleanup(word_list))
    word_count = manager.dict()
#    server = manager.get_server()
#    server.start()

    p = Pool(3)
#    p.map(cleanup, words)
    p.map(c_word_dict, word_list, chunksize=100)

    top_ten(word_count)
