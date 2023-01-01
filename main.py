#!/usr/bin/python3
import sys
import Util
import wordlist
from random import randint, shuffle


def train(wordlist):
    shuffle(wordlist)
    score = 0
    train_len = len(wordlist)

    while len(wordlist):
        card = wordlist.pop()
        print(card[1])
        word = input().strip().lower()
        if word == card[0].strip().lower():
            print('\x1B[32mCorrect!\033[0m')
            score += 1
        else:
            print('\x1B[31mWrong.\033[0m')
            print('\x1B[35m' + 'Right answer was: ' + card[0] + '\033[0m')
            wordlist.insert(randint(0, len(wordlist)), card)
            score -= 1
    print('Your score is %d/%d.' % (score, train_len))

flags = ['-c', '-l', '-a', '-n', '-h']

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
    print(wl_name)
    crop = None
    while pos < len(sys.argv):
        if sys.argv[pos] in flags:
            if sys.argv[pos] == flags[0]:
                wordlist.create_wordlist(get_wl_name(pos))
                pos += 2
            elif sys.argv[pos] == flags[1]:
                should_train = False
                print(wordlist.load_wordlist(get_wl_name(pos)))
                pos += 2
            elif sys.argv[pos] == flags[2]:
                wordlist.append_to_wordlist(get_wl_name(pos))
                pos += 2
            elif sys.argv[pos] == flags[3]:
                if not sys.argv[pos + 1].isdigit():
                    Util.print_help()
                crop = int(sys.argv[pos + 1])
                pos += 2
            elif sys.argv[pos] == flags[4]:
                Util.print_help()
        else:
            wl_name = sys.argv[pos]
            break
    if should_train:
        train(wordlist.crop_wordlist(wordlist.load_wordlist(wl_name), crop))

parse_command_line()
