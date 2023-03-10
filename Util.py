import sys
import glob
import os

path = os.path.expanduser('~/.zeng/')
colors = {'zero' : '\033[0m', 'green' : '\x1B[32m', 'red' : '\x1B[31m', 
          'purple' : '\x1B[35m', 'yellow' : '\x1B[33m'}

def print_help():
    print("""\
Usage:
    %s [OPTION] [WORDLIST_NAME]

If wordlist is required for the option, but not provided, then the most recent .wordlist file from ~/.zeng is used (works only for the last argument).

Options:
    -c [WL]: create empty wordlist
    -l [WL]: print wordlist
    -a [WL]: append card to wordlist (first line is treated as word, other lines — explanation and examples)
    --tail <N>: adds last <N> words from wordlist to training pool
    --head <N>: adds first <N> words from wordlist to training pool
    -q <word> [WL]: search for a definition of the <word>
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

def print_col(col, s):
    print(colors[col] + s + colors['zero'])
