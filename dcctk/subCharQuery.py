#%%
from typing import Sequence
from CompoTree import ComponentTree, Radicals, CharLexicon, IDC
from CompoTree import CTFounds

ctree = ComponentTree.load()
radicals = Radicals.load()


match_cache = dict(
    # (char, tk, hash): True
)
radical_map = None  # { rad: set(characters) }

def char_match_compo(char:str, tk:dict, lexicon:CharLexicon, hash):
    key = (char, str(tk), hash)
    if key in match_cache:
        return match_cache[key]
    
    match_cache[key] = False
    if char in find_compo(tk, lexicon):
        match_cache[key] = True
    
    return match_cache[key]
    

def find_compo(tk:dict, lexicon:CharLexicon):
    """[summary]

    Parameters
    ----------
    tk : dict
        
        {'match': {
            'compo': ['忄'],
            'idc': ['horz2'],
            'pos': ['0'],
            'max_depth': ['1']},
        'not_match': {}
        }

        {'match': {
            'radical': ['人']},
        'not_match': {}
        }
    """
    global radical_map

    # Radical search
    if 'radical' in tk['match']:
        # Inverse index
        build_radical_map(lexicon)
        rad = tk['match']['radical'][0]
        return radical_map.get(rad, set())

    # Component search
    sp = {
        "compo": '',
        "max_depth": 1,
        'idc': None, # IDC['horz2'].value,
        'pos': -1,
    }
    for k, v in tk['match'].items():
        if k in sp:
            v = v[0]
            if k in ['max_depth', 'pos']: 
                v = int(v)
            if k == 'idc':
                v = IDC[v].value
            sp[k] = v


    bottom_hits = ctree.find(sp['compo'], max_depth=sp['max_depth'], bmp_only=True)
    
    if sp['idc'] is None:
        return set( x[0] for x in CTFounds(bottom_hits)\
            .filter_with_lexicon(lexicon)\
            .tolist() )

    return set( x[0] for x in CTFounds(bottom_hits)\
        .filter(idc=sp['idc'], pos=sp['pos'])\
        .filter_with_lexicon(lexicon)\
        .tolist() )


def get_radicals(lexicon:CharLexicon):
    build_radical_map(lexicon)
    return set(radical_map.keys())


def build_radical_map(lexicon:CharLexicon):
    global radical_map
    # Inverse index
    if radical_map is None:
        print('Building index for character radicals...')
        radical_map = {}
        for char in lexicon.lexicon:
            rad = radicals.query(char)[0]
            radical_map.setdefault(rad, set()).add(char)


def load_lexicon(lexicon: Sequence):
        lexicon = set(lexicon)
        return CharLexicon(lexicon, [], [])
# %%
