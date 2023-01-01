import os
import sys
from pathlib import Path
from Util import path, colors
import Util

def create_wordlist(name):
    name += '.wordlist'
    if not os.path.exists(path):
        os.makedirs(path)
    # if os.path.exists(path + name):
    #     raise Exception('File exists')
    Path(path + name).touch()
    print("Created:", path + name)
    sys.exit(0)

def load_wordlist(name):
    if name == '':
        raise Exception('No filename provided')
    name = Util.make_filename(name)
    if not os.path.exists(name):
        raise Exception('No such wordlist')
    with open(name, 'r') as file:
        lines = [line.rstrip() for line in file]
        res = []
        i = 0
        was = True
        cur_word = ''
        cur_desc = ''
        for line in lines:
            if line == '':
                if not was:
                    res.append((cur_word, cur_desc))
                    cur_word = ''
                    cur_desc = ''
                was = True
                continue
            elif was:
                was = False
                cur_word = line
            else:
                if cur_desc != '':
                    cur_desc += '\n'
                cur_desc += line
        if not was:
            res.append((cur_word, cur_desc))
        return res

def print_wordlist(name):
    wordlist = load_wordlist(name)
    Util.print_col('yellow', 'Wordlist: %s; contains %d words.' % (name, len(wordlist)))

def append_to_wordlist(name):
    name = Util.make_filename(name)
    print('Appending to wordlist:', name)
    with open(name, 'a') as f:
        f.write('\n')
        for line in sys.stdin:
            f.write(line)
    sys.exit(0)


def crop_wordlist(wordlist, crop):
    if crop == None or len(wordlist) <= crop:
        return wordlist
    return wordlist[-crop:]

def grep(wordlist, word):
    ans = []
    for card in wordlist:
        if word in card[0]:
            ans.append(colors['red'] + card[0] + colors['zero'] + '\n' +
                       colors['purple'] + card[1] + colors['zero'])
    return ans

