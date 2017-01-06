# encoding: utf-8

import os
import cPickle
import codecs
import random
import numpy as np

root = './data/sentiment140/'
train_file = 'traindata'
test_file = 'testdata'
lex_file = 'lexicon.pickle'
delimiter = ':%:%:%'

class Sentiment140(object):
    def __init__(self):
        self.lex = cPickle.load(open(root + lex_file))
        self.train_fp = codecs.open(root + train_file, 'r', encoding='latin-1')
        self.test_fp = codecs.open(root + test_file, 'r', encoding='latin-1')

    def _get_line(self, pos, fp):
        # seek 是把指针指向 pos 个字节处，而不是行
        fp.seek(pos)
        # 读取所在行
        fp.readline()
        # 返回下一完整行
        return fp.readline()

    def get_train_batch(self, n=150):
        X = []
        Y = []
        sz = os.stat(root + train_file).st_size
        i = 0
        while True:
            pos = random.randint(0, sz)
            line = self._get_line(pos, self.train_fp)
            if line:
                features, label = self._line_to_data(line)
                X.append(features)
                Y.append(label)
                i += 1
                if i == n:
                    break
        return X, Y

    def get_test_dataset(self):
        X = []
        Y = []
        for line in self.test_fp:
            features, label = self._line_to_data(line)
            X.append(features)
            Y.append(label)
        return X, Y

    def _line_to_data(self, line):
        # features 是一个数组，长度为词典 lex 长度
        # line 中有字段为 tweet 中的词在 lex 中的位置索引
        # features 从这个字段中取出索引，把对应位置置 1，其他位置保持 0 不变
        features = np.zeros(len(self.lex))
        label, indices, _ = line.split(delimiter)
        for idx in eval(indices):
            features[idx] = 1
        return list(features), eval(label)
