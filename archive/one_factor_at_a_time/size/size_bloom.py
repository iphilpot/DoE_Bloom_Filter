#!/usr/bin/env python

import mmh3
from bitarray import bitarray

# HYPO: Increase size will decrease FP

class Bloom(object):
    def __init__(self, item_count, hash_pass_count):
        self.size=item_count
        self.hash_pass=hash_pass_count
        self.present_data=self.get_present_data()
        self.absent_data=self.get_absent_data()
        self.ba=bitarray(self.size)

    def add(self, item):
        for i in range(self.hash_pass):
            h=mmh3.hash(item, i)%self.size
            self.ba[h]=True

    def check(self, item):
        digest=[]
        for i in range(self.hash_pass):
            a_hash=mmh3.hash(item, i)%self.size
            a_present=self.ba[a_hash]
            digest.append(a_present)
            if not a_present:            
                return False
            else:
                if len(digest) == self.hash_pass:
                    return True

    @classmethod
    def get_present_data(self):
        with open('../../resources/present.txt', 'r') as fp:
            present=fp.readlines()
        return present
    
    @classmethod
    def get_absent_data(self):
        with open('../../resources/absent.txt', 'r') as fp:
            absent=fp.readlines()
        return absent

for s in range(10000, 2000000, 10000):
    false_count=0
    sb = Bloom(s, 1)
    for p in sb.present_data:
        sb.add(p)
    for a in sb.absent_data:
        val = sb.check(a)
        if val:
            false_count+=1
    print(str(s) + ',' + str(false_count))
