# encoding: utf-8

import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import OrderedDict, defaultdict as dd
import cPickle
import codecs
import numpy as np

root = './data/sentiment140/'
org_train_file = 'training.1600000.processed.noemoticon.csv'
org_test_file = 'testdata.manual.2009.06.14.csv'

train_file = 'traindata'
test_file = 'testdata'
lex_file = 'lexicon.pickle'

delimiter = ':%:%:%'

def process_origin_file(org_file, output_file):
    lemmatizer = WordNetLemmatizer()
    lex = cPickle.load(open(root + lex_file, 'r'))
    lex_sz = len(lex)
    print "Lex size: {}".format(lex_sz)
    with codecs.open(output_file, 'w', encoding='latin-1') as output:
        with codecs.open(org_file, buffering=10000, encoding='latin-1') as f:
            for line in f:
                # line like: # "4","2193601966","Tue Jun 16 08:40:49 PDT 2009","NO_QUERY","AmandaMarie1028","Just woke up."
                line = line.replace('"', '')    # remove double-quote
                parts = line.split(',')
                # '0' neg, '2' neutral, '4' pos; 表达成矢量形式
                clf = [0, 0, 1] if parts[0] == '0' else [0, 1, 0] if parts[0] == '2' else [1, 0, 0]
                tweet = parts[-1]
                words = word_tokenize(tweet.lower())
                words = [lemmatizer.lemmatize(word) for word in words]
                # features dict 记录了一个 tweet 中所有在 lex 中存在的词在 lex 中的索引号
                features = {}
                for word in words:
                    try:
                        features[lex.index(word)] = 1
                    except:
                        pass
                output.write(str(clf) + delimiter + str(features.keys()) + delimiter + tweet)    # tweet 自带换行符


def create_lexicon(org_file, outfname):
    lex = []
    lemmatizer = WordNetLemmatizer()
    count_word = dd(int)
    with codecs.open(org_file, 'r', buffering=10000, encoding='latin-1') as f:
        for line in f:
            # line like: # "4","2193601966","Tue Jun 16 08:40:49 PDT 2009","NO_QUERY","AmandaMarie1028","Just woke up."
            line = line.replace('"', '')    # remove double-quote
            tweet = line.split(',')[-1]
            words = word_tokenize(tweet.lower())
            for word in words:
                word = lemmatizer.lemmatize(word)
                count_word[word] += 1

            # 按词频排序，由少到多
        count_word = OrderedDict(sorted(count_word.items(), key=lambda t: t[1]))
        # 去除长尾词频和常见词词频
        for word, count in count_word.iteritems():
            if count < 100000 and count > 100:
                lex.append(word)
        print "Total word count in lexicon: {}".format(len(lex))
        print "Max count: {} - {}".format(count_word.keys()[-1], count_word.values()[-1])
        print "Min count: {} - {}".format(count_word.keys()[0], count_word.values()[0])
        cPickle.dump(lex, open(outfname, 'w'))


if __name__ == '__main__':
    print "lexicon ..."
    # create_lexicon(root + train_file, root + lex_file)
    print "processing test file ..."
    process_origin_file(root + org_test_file, root + test_file)
    print "processing train file ..."
    process_origin_file(root + org_train_file, root + train_file)
