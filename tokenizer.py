#!/usr/bin/env python
"""
Tool for de/tokenizing and using BPE.

Supported tokenizers:
- Moses.
- Sentencepiece
- Mecab. (Tokenization only.)
- Stanford Word Segmenter. (Tokenization only.)
"""

from sacremoses import MosesTokenizer, MosesDetokenizer
import sentencepiece as spm
from subword_nmt.apply_bpe import BPE
import os, codecs, sys
from subprocess import run
from re import sub


class Tokenizer:
    def __init__(self, tokenizer, model=None, bpe_codes=None):
        """
        :param tokenizer: (str) tokenizer to use (moses, sentencepiece, mecab or stanford).
        :param model: (str) path to tokenizer model.
        :param bpe_codes: (str) path to bpe_codes.
        """
        # Set tokenizer.
        if tokenizer == 'moses':
            self.tokenizer, self.detokenizer = MosesTokenizer(), MosesDetokenizer()

        elif tokenizer == 'sentencepiece':
            self.tokenizer = spm.SentencePieceProcessor()
            if model is None:
                raise ValueError("Tokenizer model is mandatory for Sentencepiece.")
            self.tokenizer.Load(model)
            self.detokenizer = None

        elif tokenizer == 'mecab':
            self.tokenizer = None
            self.detokenizer = None

        elif tokenizer == 'stanford':
            self.tokenizer = None
            self.detokenizer = None

        else:
            raise ValueError("Invalid value for tokenizer. Supported tokenizers: moses, "
                             "sentencepiece, mecab and stanford")

        self.tokenizer_type = tokenizer
        self.bpe = None if bpe_codes is None else BPE(codecs.open(bpe_codes, encoding='utf-8'))

    def tokenize(self, sentence):
        """
        This method tokenizes a sentence.
        :param sentence: (str) sentence.
        :return: (str) tokenized sentence.
        """
        if self.tokenizer_type == 'moses':
            return " ".join(self.tokenizer.tokenize(sentence))

        if self.tokenizer_type == 'sentencepiece':
            return " ".join(self.tokenizer.EncodeAsPieces(sentence))

        dir_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        if self.tokenizer_type == 'mecab':
            try:
                sentence_ = run([dir_path + '/tokenizers/mecab/bin/mecab', '-O', 'wakati'], capture_output=True,
                                  encoding='utf-8', input=sentence).stdout.strip()
            except:
                raise ValueError("Mecab not install.")
            return sentence_

        if self.tokenizer_type == 'stanford':
            try:
                sentence_ = run([dir_path + '/tokenizers/stanford_segmenter/segment.sh', 'ctb', '/dev/stdin',
                                 'UTF-8', '0'], capture_output=True, encoding='utf-8', input=sentence).stdout.strip()
            except:
                raise ValueError("Stanford Word Segmenter not install.")
            return sentence_

    def detokenize(self, sentence):
        """
        This method detokenizes a sentence.
        :param sentence: (str) sentence.
        :return: (str) detokenized sentence.
        """
        if self.tokenizer_type == 'moses':
            return self.detokenizer.detokenize(sentence.split())

        if self.tokenizer_type == 'sentencepiece':
            return self.tokenizer.DecodePieces(sentence.split())

        raise ValueError("Detokenization not yet implemented for this tokenizer.")

    def apply_bpe(self, sentence):
        """
        This method applies BPE to a sentence.
        :param sentence: (str) sentence.
        :return: (str) BPE sentence.
        """
        return self.bpe.segment(sentence)

    def remove_bpe(self, sentence):
        """
        This method removes BPE from a sentence.
        :param sentence: (str) BPE sentence.
        :return: sentence.
        """
        return sub("(@@ )|(@@ ?$)", '', sentence)

