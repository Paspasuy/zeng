import sys
import glob
import os

path = os.path.expanduser('~/.zeng/')

def print_help():
    print("""\
Usage:
    %s [OPTION] [WORDLIST_NAME]

If wordlist is required for the option, but not provided, then the most recent .wordlist file from ~/.zeng is used (works only for the last argument).

Options:
    -c [WL]: create empty wordlist
    -l [WL]: print wordlist
    -a [WL]: append card to wordlist (first line is treated as word, other lines — explanation and examples)
    -n <N>: takes in training pool last <N> words from wordlist
    -h: print help
""" % sys.argv[0])
#    -r: shuffle words from training pool
    sys.exit(0)

def get_latest_wordlist():
    list_of_files = glob.glob(path + '*.wordlist')
    if len(list_of_files) == 0:
        return ''
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

def make_filename(name):
    if not name.endswith('.wordlist'):
        name = path + name + '.wordlist'
    return name
