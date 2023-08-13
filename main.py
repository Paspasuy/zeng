#!/usr/bin/python3
import sys
import Util
import wordlist
from random import randint, shuffle
from Util import colors


def print_score(score, train_len):
    Util.print_col('cyan', '** You scored %d/%d. **' % (score, train_len))


def train(wordlist):
    shuffle(wordlist)
    score = 0
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
            score += 1
        else:
            Util.print_col('red', 'Wrong.')
            Util.print_col('purple', 'Right answer was: ' + card[0])
            wordlist.insert(randint(0, len(wordlist)), card)
            score -= 1
    print_score(score, train_len)

flags = ['--head', '--tail']
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
    crop = None
    wl_pos = 0
    if '--tail' in sys.argv:
        pos = sys.argv.index('--tail')
        if not sys.argv[pos + 1].isdigit():
            Util.print_help()
        crop = int(sys.argv[pos + 1])
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
        train(wordlist.crop_wordlist(wordlist.load_wordlist(wl_name), crop))

parse_command_line()
