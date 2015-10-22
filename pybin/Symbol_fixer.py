#!/usr/bin/env python3
import sys
import os
import argparse


class GeneSymbolMapper:
    def __init__(self):
        self.__symbols = dict()

    def map_symbol(self, key, symbol):
        if key in self.__symbols:
            print("you attempted to map an already mapped key: %s, which is mapped to %s, tried to map it to %s" % (key, symbol, self.__symbols[key]), file=sys.stderr);
            exit(-1)
        self.__symbols[key] = symbol

    def get_mapped_name(self, oldname):
        if oldname not in self.__symbols:
            return ""
        return self.__symbols[oldname]


class MappingInputFile:
    def __init__(self):
        self.__raw_lines = list()
        self.__encoded_lines = list()

    def add_line(self, raw, encoded):
        self.__raw_lines.append(raw)
        self.__encoded_lines.append(encoded)

    def get_encoded(self, index):
        return self.__encoded_lines[index]

    def get_raw(self, index):
        return self.__raw_lines

    def get_encoded_list(self):
        return self.__encoded_lines

    def get_raw_list(self):
        return self.__raw_lines

#TODO merge functionality of all the name fixer scripts into one file for ease of use
#TODO make name fixer scripts work on either actual MAF files or custom files with numbered columns