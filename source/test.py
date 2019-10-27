#!/usr/bin/env python3
# coding: utf-8
from janome.tokenizer import Tokenizer
from pykakasi import kakasi

kakasi = kakasi()
tokenizer = Tokenizer()
kakasi.setMode('H', 'a')
kakasi.setMode('K', 'a')
kakasi.setMode('J', 'a')



f = open(u"./5.壱章－１.txt", 'r', encoding='utf-8')
test = f.read()
f.close
kata=""
for token in tokenizer.tokenize(test):
    kata += token.reading
kata=kata.replace('*', '\n')
conv = kakasi.getConverter()
print(conv.do(kata))