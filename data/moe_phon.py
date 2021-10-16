#%%
import json
from pathlib import Path
from utils import get_phons, get_ref_heteronyms

if not Path('moe.json').exists():
    import gdown
    gdown.download('https://drive.google.com/uc?id=1H-wXEWC0Tgz8GE3kmc9vZV0WfuiqiGmV')


with open("moe.json", encoding="utf-8") as f:
    d = json.load(f)


title_map = { x.get('title', ''): x for x in d }

phon = {}
for i, x in enumerate(d):
    t = x.get('title', '')

    p = get_phons(x)
    if len(p) > 0:
        phon[t] = p
    else:
        hetro = get_ref_heteronyms(x)
        if hetro is None: continue
        ref, t = hetro
        if ref in phon:
            phon[t] = phon[ref]
        else:
            p = get_phons(title_map[ref])
            if len(p) > 0:
                phon[t] = p


with open('moe_char_phon.json', "w", encoding="utf-8") as f:
    json.dump(phon, f, ensure_ascii=False, indent=True)
