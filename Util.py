import sys
import glob
import os

path = os.path.expanduser('~/.zeng/')
colors = {'zero': '\033[0m', 'green': '\x1B[32m', 'red': '\x1B[31m', 
          'purple': '\x1B[35m', 'yellow': '\x1B[33m', 'cyan': '\x1B[36m',
          'cyan2': '\x1B[96m', 'purple2': '\x1B[95m', 'gray2': '\x1B[90m'}


def print_help():
    cmd_name = sys.argv[0]
    print(f"""\
Usage:
    {cmd_name} [TRAINING_OPTION] [WORDLIST_NAME]
OR
    {cmd_name} [COMMAND] [WORDLIST_NAME]

If wordlist is required for the option, but not provided, then the most recent .wordlist file from ~/.zeng is used (works only for the last argument).

Commands:
    create [WL]: create empty wordlist
    print [WL]: print wordlist
    append [WL]: append card to wordlist (first line is treated as word, other lines — explanation and examples)
    search <WORD> [WL]: search for a definition of the <word>
    lists: print all wordlists
    help: print help

Training options:
    --tail <N>: adds last <N> words from wordlist to training set 
    --head <N>: adds first <N> words from wordlist to training set
    --range <X-Y>: adds words from X to Y to training set
""")
#    -r: shuffle words from training pool
    sys.exit(0)


def get_latest_wordlist():
    list_of_files = glob.glob(path + '*.wordlist')
    if len(list_of_files) == 0:
        return ''
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file


def get_wordlists():
    list_of_files = glob.glob(path + '*.wordlist')
    if len(list_of_files) == 0:
        return ''
    return list_of_files


def get_wordlist_names():
    return [make_name(x) for x in get_wordlists()]


def make_filename(name):
    if not name.endswith('.wordlist'):
        name = path + name + '.wordlist'
    return name


def make_name(name):
    if name.endswith('.wordlist'):
        i1 = name.rfind('/')
        i2 = name.rfind('.')
        name = name[i1 + 1: i2]
    return name

def print_col(col, s):
    print(colors[col] + s + colors['zero'])
