import requests
from Util import print_col

def fetch_def(word):
    resp = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
    if resp.status_code != 200:
        print_col('red', 'Failed to fetch definition from internet')
        return [], []
    definitions = []
    synonyms = []
    js = resp.json()
    for item in js:
        for mn in item['meanings']:
            for df in mn['definitions']:
                definitions.append(df['definition'])
            synonyms += mn['synonyms']
    return definitions, synonyms

