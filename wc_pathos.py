#!/usr/bin/python
import os
import urllib
import operator
import timing

from pathos.parallel import ParallelPool as Pool
pool = Pool()



#url = 'http://www.gutenberg.org/cache/epub/25990/pg25990.txt'
#f = urllib.urlopen(url)

manager_address = 'localhost'

f = open('/root/homework/pg25990.txt')

def info(title):
    print title
    print 'module name:', __name__
    if hasattr(os, 'getppid'):
        print 'parent process:', os.getppid()
    print 'process id:', os.getpid()

@timing.timed
def m_word_list(file):
    info('server word_list function')
    words = []
    words.append(f.read().split())
#    print words
#    print "time: %s" % m_word_list.timed()
    return words

def c_word_list(file):
    info('client word_list function')

def m_cleanup(words):
    info('cleanup function')
    only_words = []
    symbols = "~!@#$%^&*()_+=-{}\|\\][:\"\';<>?/.,"
    for word in words:
        for i in range(0, len(symbols)):
            word = word.replace(symbols[i], "")
        if len(word) != 0:
            only_words.append(word)
#    print only_words
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
    info('Mainline function')

    pool.ncpus = 2
    pool.servers = ('localhost:17320',)

    words = pool.map(m_word_list, f) 
    pool.join()

    pool.servers = ('localhost:17320',)
    clean_list = pool.map(m_cleanup, words)
    pool.join(clean_list, )

    pool.servers = ('localhost:17320',)
    word_count = pool.map(word_dict, cleanlist)
    pool.join(word_count, )

    top_ten(word_count)
