#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2012-11-1

@author: reorx
'''

import os
import sys
import codecs
import chardet
import traceback
from StringIO import StringIO
#import shutil
#import logging


#logging.basicConfig(level=logging.DEBUG)


HELPER_TEXT = """
What to do:
    (1) Auto detect & convert
    (2) Try to detect
    (3) Manually convert
    (4) Exit
"""

HELPER_TEXT_2 = """
You can:
    (1) Input encoding
    (2) Show suggestions
    (3) Set sampling line range (now %s-%s)
    (4) Go back
"""

SUGGESTIONS = """
Chinese:
    gbk(cp936), gb2312, gb18030
    big5, cp950

Japanese:
    shift_jis, euc_jp, cp932, iso2022_jp
    (or maybe using Chinese encodings above)

see full list on: http://docs.python.org/2/library/codecs.html#standard-encodings
Enter to return
"""

CANDIDATES = [
    ('GBK', 'GB2312', 'GB18030'),
]


def detect(string):
    """
    return the fixed result of chardet.detect
    """
    res = chardet.detect(string)
    
    for i in CANDIDATES:
        if res['encoding'] in i:
            res['encoding'] = i[0]
    
    return res


class Helper(object):
    text = HELPER_TEXT
    
    def __init__(self):
        source_path = sys.argv[1]
        if not os.path.isabs(source_path):
            source_path = os.path.abspath(source_path)
        dirpath, source_name = os.path.split(source_path)
        
        self.converted_path = os.path.join(dirpath, '_' + source_name)
        self.source_path = source_path
        self.finished = False
        self.sampling_line_range = (1, 30)
        
        print 'Stdout encoding: %s' % sys.stdout.encoding
        print 'Get file: %s' % self.source_path
        print 'Reading file..'
        with open(self.source_path, 'r') as source_fd:
            self.source = source_fd.read()
    
    def run(self):
        while not self.finished:
            i = raw_input(self.text)
            
            if '1' == i:
                self.auto_convert()
            elif '2' == i:
                self.try_to_detect()
            elif '3' == i:
                self.manually_convert()
            elif '4' == i:
                sys.exit(0)
            else:
                print 'Please make a valid choice'
                continue
    
    def manually_convert(self):
        while True:
            source_ec = raw_input('Type source encoding: ')
            if self._lookup_encoding(source_ec):
                break
        while True:
            aim_ec = raw_input('Type aim encoding: ')
            if self._lookup_encoding(aim_ec):
                break
        decoded = self.decode(source_ec)
        self.encode_and_write(decoded, aim_ec)
        self.finish()
        
    def decode(self, ec):
        return unicode(self.source, ec, 'replace')
    
    def finish(self, pause=False):
        raw_input('Finished.')
        sys.exit(0)
    
    def auto_convert(self):
        res = detect(self.source)
        print 'Detect result: %s, confidence %s' % (res['encoding'], res['confidence'])
        if not res['encoding']:
            raw_input('Could not detect encoding, suggest trying the second ability')
            return
            
        try:
            decoded = unicode(self.source, res['encoding'], 'strict')
        except UnicodeDecodeError:
            print 'Caught exception in decoding progress, %s' % traceback.format_exc()
            i = raw_input('Continue using this encoding(%s) in non-strict mode ? y/N ' % res['encoding'])
            if 'N' == i:
                return
            decoded = self.decode(res['encoding'])
        
        print 'Encode using utf-8(default option)'
        self.encode_and_write(decoded, 'utf-8')
        self.finish()
    
    def _stdout_encode(self, u):
        return u.encode(sys.stdout.encoding, 'replace')
    
    def _lookup_encoding(self, ec):
        try:
            codecs.lookup(ec)
            return True
        except LookupError, e:
            print '%s, please retry' % e
            return False
    
    def encode_and_write(self, decoded, ec):
        converted = decoded.encode('utf-8', 'replace')
        if os.path.exists(self.converted_path):
            ip = raw_input('Aim file %s exists, overwrite it? (y/N) ' % self.converted_path)
            if 'N' == ip:
                return
        print 'Write file: %s' % self.converted_path
        with open(self.converted_path, 'w') as converted_fd:
            converted_fd.write(converted)
    
    def test_encoding(self):
        finished = False
        while not finished:
            ip = raw_input('Type encoding (or n to return): ')
            if 'n' == ip:
                return
            elif not self._lookup_encoding(ip):
                continue
            ec = ip
                
            decoded = self.decode(ec)
            decoded_fd = StringIO(decoded)
            to_print = 'Result:\n'
            in_range = False
            for loop, line in enumerate(decoded_fd.readlines()):
                line_num = loop + 1
                if line_num >= self.sampling_line_range[0] and line_num <= self.sampling_line_range[1]:
                    in_range = True
                    to_print += ''.join('%s| %s' % (line_num, self._stdout_encode(line)))
            if not in_range:
                print 'Invalid line range, please reset'
                return
            print to_print
            
            ip = raw_input('Is %s the right encoding? (n/Y) ' % ec)
            if 'Y' != ip:
                continue
            while True:
                ip = raw_input('Type aim encoding (default utf-8): ') or 'utf-8'
                if self._lookup_encoding(ip):
                    break
            self.encode_and_write(decoded, ip)
            self.finish(True)
            
    def try_to_detect(self):
        while True:
            i = raw_input(HELPER_TEXT_2 % self.sampling_line_range)
            if '1' == i:
                self.test_encoding()
            elif '2' == i:
                print SUGGESTIONS
                raw_input()
            elif '3' == i:
                while True:
                    ip = raw_input('Type two int seperated with space (eg. 1 30): ')
                    l = ip.split()
                    try:
                        if len(l) > 2:
                            raise IndexError()
                        t = tuple(map(int, l))
                        if not t[0] > 0 or not t[1] > 0:
                            raise ValueError()
                        assert t[0] < t[1]
                        break
                    except IndexError:
                        print 'Please input two numbers'
                    except ValueError:
                        print 'Please input integer bigger than 0'
                    except AssertionError:
                        print 'The second int should be larger than the first one'
                print 'Set (%s, %s)' % t
                self.sampling_line_range = t
            elif '4' == i:
                return
            else:
                print 'Please make a valid choice'
                continue
                


def main():
    helper = Helper()
    helper.run()


if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        # for debug use
        print traceback.format_exc()
        raw_input()