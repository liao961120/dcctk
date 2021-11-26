#%%
import json
import yaml
from CompoTree import Radicals


rad = Radicals.load()
radicals = set(
    x for x in rad.radical_map.values()
    if x not in rad.ts_radicals.keys()
)
with open("semanticTag2radical.yaml", encoding="utf-8") as f:
    sem_rad = yaml.load(f, yaml.FullLoader)

rad_sem = {}
for s, rs in sem_rad.items():
    for r in rs:
        if r not in radicals: continue
        rad_sem.setdefault(r, set()).add(s)
rad_sem = { k:list(v) for k, v in rad_sem.items() }

# %%
with open("radical_semantic_tag.json", "w", encoding="utf-8") as f:
    json.dump(rad_sem, f, ensure_ascii=False)

    
with open("radical_semantic_tag.yaml", "w", encoding="utf-8") as f:
    yaml.dump(rad_sem, f, allow_unicode=True, sort_keys=False, default_flow_style=None)
# %%
