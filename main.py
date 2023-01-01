#!/usr/bin/python3
import sys
import Util
import wordlist
from random import randint, shuffle
from Util import colors

def print_score(score, train_len):
    print('** You scored %d/%d. **' % (score, train_len))

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

flags = ['-c', '-l', '-a', '--head', '--tail', '-h', '--help', '-q']

#TODO implement --head

def get_wl_name(pos):
    if pos + 1 >= len(sys.argv):
        return Util.get_latest_wordlist()
    if sys.argv[pos + 1] in flags:
        Util.print_help()
    return sys.argv[pos + 1]

def parse_command_line():
    should_train = True
    pos = 1
    wl_name = Util.get_latest_wordlist()
    crop = None
    while pos < len(sys.argv):
        if sys.argv[pos] in flags:
            if sys.argv[pos] == '-c':
                wordlist.create_wordlist(get_wl_name(pos))
                pos += 2
            elif sys.argv[pos] == '-l':
                should_train = False
                wordlist.print_wordlist(get_wl_name(pos))
                pos += 2
            elif sys.argv[pos] == '-a':
                wordlist.append_to_wordlist(get_wl_name(pos))
                pos += 2
            elif sys.argv[pos] == '--tail':
                if not sys.argv[pos + 1].isdigit():
                    Util.print_help()
                crop = int(sys.argv[pos + 1])
                pos += 2
            elif sys.argv[pos] == '-h' or sys.argv[pos] == '--help':
                Util.print_help()
            elif sys.argv[pos] == '-q':
                should_train = False
                if pos + 2 >= len(sys.argv):
                    Util.print_help()
                print(*wordlist.grep(wordlist.load_wordlist(get_wl_name(pos + 1)), sys.argv[pos + 1]), sep='\n\n')
                pos += 3
        else:
            wl_name = sys.argv[pos]
            break
    if should_train:
        train(wordlist.crop_wordlist(wordlist.load_wordlist(wl_name), crop))

parse_command_line()
