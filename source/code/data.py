###############################################################################
# Author: Wasi Ahmad
# Project: Quora Duplicate Question Detection
# Date Created: 7/25/2017
#
# File Description: This script contains code to read and parse input files.
###############################################################################

import os, helper


class Dictionary(object):
    """Dictionary class that stores all words of train/dev corpus."""

    def __init__(self):
        self.word2idx = {}
        self.idx2word = []
        # Create and store three special tokens
        self.pad_token = '<pad>'
        self.start_token = '<s>'
        self.end_token = '</s>'
        self.unknown_token = '<unk>'
        self.idx2word.append(self.pad_token)
        self.word2idx[self.pad_token] = len(self.idx2word) - 1
        self.idx2word.append(self.start_token)
        self.word2idx[self.start_token] = len(self.idx2word) - 1
        self.idx2word.append(self.end_token)
        self.word2idx[self.end_token] = len(self.idx2word) - 1
        self.idx2word.append(self.unknown_token)
        self.word2idx[self.unknown_token] = len(self.idx2word) - 1

    def add_word(self, word):
        if word not in self.word2idx:
            self.idx2word.append(word)
            self.word2idx[word] = len(self.idx2word) - 1
        return self.word2idx[word]

    def contains(self, word):
        return True if word in self.word2idx else False

    def __len__(self):
        return len(self.idx2word)


class Instance(object):
    """Instance that represent a sample of train/dev/test corpus."""

    def __init__(self, instance_id):
        self.id = instance_id
        self.sentence1 = []
        self.sentence2 = []
        self.label = ''

    def add_sentence(self, sentence, sentence_no, dictionary, is_test_instance):
        words = [dictionary.start_token] + helper.tokenize_and_normalize(sentence) + [dictionary.end_token]
        if is_test_instance:
            for i in range(len(words)):
                if not dictionary.contains(words[i]):
                    words[i] = dictionary.unknown_token
        else:
            for word in words:
                dictionary.add_word(word)
        if sentence_no == 1:
            self.sentence1 = words
        else:
            self.sentence2 = words

    def add_label(self, label):
        self.label = label


class Corpus(object):
    """Corpus class which contains all information about train/dev/test corpus."""

    def __init__(self, path, filename, dictionary, is_test_corpus=False):
        self.data = self.parse(os.path.join(path, filename), dictionary, is_test_corpus)

    @staticmethod
    def parse(path, dictionary, is_test_corpus):
        """Parses the content of a file."""
        assert os.path.exists(path)

        samples = []
        with open(path, 'r') as f:
            f.readline()
            for line in f:
                tokens = line.strip().split('\t')
                instance = Instance(int(tokens[0]))
                instance.add_sentence(tokens[3], 1, dictionary, is_test_corpus)
                instance.add_sentence(tokens[4], 2, dictionary, is_test_corpus)
                instance.add_label(int(tokens[5]))
                samples.append(instance)

        return samples
