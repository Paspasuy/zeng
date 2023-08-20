#!/usr/bin/python3
import sys
import Util
import wordlist
from random import randint, shuffle
from Util import colors


def print_score(ok, wrong, total):
    print(f'{colors["cyan"]}** You scored {colors["green"]}{ok}{colors["cyan"]} correct / \
{colors["red"]}{wrong}{colors["cyan"]} \
incorrect of total {colors["gray2"]}{total}{colors["cyan"]} words. **')


def train(wordlist):
    shuffle(wordlist)
    correct = 0
    mistakes = 0
    train_len = len(wordlist)

    while len(wordlist):
        card = wordlist.pop()
        print(card[1])
        try:
            word = input().strip().lower()
        except EOFError:
            print_score(score, train_len)
            sys.exit(0)
        if word == card[0].strip().lower():
            Util.print_col('green', 'Correct!')
            correct += 1
        else:
            Util.print_col('red', 'Wrong.')
            Util.print_col('purple', 'Right answer was: ' + card[0])
            wordlist.insert(randint(0, len(wordlist)), card)
            mistakes -= 1
    print_score(correct, mistakes, train_len)


flags = ['--head', '--tail', '--range']
actions = ['create', 'print', 'append', 'search', 'lists', 'help']

#TODO implement --head


def get_wl_name(pos, new_allowed=False):
    wordlists = Util.get_wordlist_names()
    if not new_allowed and pos + 1 >= len(sys.argv):
        return Util.get_latest_wordlist()
    if (sys.argv[pos + 1] not in wordlists and not new_allowed) or (new_allowed and pos + 1 >= len(sys.argv)):
        if new_allowed:
            Util.print_col('red', 'Please provide name for wordlist')
        else:
            Util.print_col('red', 'Such wordlist does not exist')
        Util.print_help()
        sys.exit(0)
    return sys.argv[pos + 1]


def parse_command_line():
    wl_name = Util.get_latest_wordlist()
    tail = None
    head = None
    rng = None
    wl_pos = 0

    if '--tail' in sys.argv:
        pos = sys.argv.index('--tail')
        if not sys.argv[pos + 1].isdigit():
            Util.print_help()
        tail = int(sys.argv[pos + 1])
        wl_pos = max(wl_pos, pos + 1)
    if '--head' in sys.argv:
        pos = sys.argv.index('--head')
        if not sys.argv[pos + 1].isdigit():
            Util.print_help()
        head = int(sys.argv[pos + 1])
        wl_pos = max(wl_pos, pos + 1)
    if '--range' in sys.argv:
        pos = sys.argv.index('--range')
        rng = list(map(int, sys.argv[pos + 1].split('-')))
        wl_pos = max(wl_pos, pos + 1)

    if len(sys.argv) > 1 and sys.argv[1] in actions:
        if sys.argv[1] == 'create':
            wordlist.create_wordlist(get_wl_name(1, True))
        elif sys.argv[1] == 'print':
            wordlist.print_wordlist(get_wl_name(1))
        elif sys.argv[1] == 'append':
            wordlist.append_to_wordlist(get_wl_name(1))
        elif sys.argv[1] == 'help':
            Util.print_help()
        elif sys.argv[1] == 'lists':
            for name in Util.get_wordlist_names():
                wordlist.print_wordlist(name)
        elif sys.argv[1] == 'search':
            if 3 >= len(sys.argv):
                Util.print_help()
            print(*wordlist.grep(wordlist.load_wordlist(get_wl_name(2)), sys.argv[2]), sep='\n\n')
    else:
        wl_name = get_wl_name(wl_pos)
        train(wordlist.crop_wordlist(wordlist.load_wordlist(wl_name), head, tail, rng))

parse_command_line()
