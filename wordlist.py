import os
import sys
from pathlib import Path
from Util import path, colors
import Util
from fetch_def import fetch_def

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
    Util.print_col('cyan', f'Appending to wordlist {name}:')
    with open(name, 'a') as f:
        word = input()
        Util.print_col('yellow', 'Searching for definition...')
        defs, syns = fetch_def(word)
        print(f'{colors["gray2"]}Definitions:{colors["cyan2"]} {" | ".join(defs)}{colors["zero"]}')
        print(f'{colors["gray2"]}Synonyms:{colors["purple2"]} {" | ".join(syns)}{colors["zero"]}')
        f.write('\n' + word + '\n')
        for line in sys.stdin:
            f.write(line)
    sys.exit(0)


def crop_wordlist(wordlist, head, tail, rng):
    if head is not None:
        return wordlist[:head]
    if tail is not None:
        return wordlist[-tail:]
    if rng is not None:
        return wordlist[rng[0]: rng[1] + 1]
    return wordlist


def grep(wordlist, word):
    ans = []
    for card in wordlist:
        if word in card[0]:
            ans.append(colors['red'] + card[0] + colors['zero'] + '\n' +
                       colors['purple'] + card[1] + colors['zero'])
    return ans

