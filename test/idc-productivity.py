import pandas as pd
from CompoTree import IDC
from hgct import CompoAnalysis, PlainTextReader

c2 = CompoAnalysis(PlainTextReader("data", auto_load=False))

df = []
for nm, val in [ (x.name, x.value) for x in IDC] + [ ("NULL", "")]:   
    p = c2.productivity(idc=nm, subcorp_idx=3)
    df.append({
        'name': nm, 
        'shape': val, 
        **p['productivity'],
        'V1C': p['V1C'],
        'V1': p['V1'],
        'NC': p['NC'],
        'N': p['N'],
    })

df = pd.DataFrame(df)
df['Proportion in sample'] = df.NC / df.N 
df