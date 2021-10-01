import re
import json
import yaml
from pathlib import Path


text_meta = {}
with open("tier1.jsonl") as f:
    for line in f:
        data = json.loads(line)
        ts = data["dynGroup"][0]

        ts_dir = Path(f"data/{str(ts).zfill(2)}/")
        if not ts_dir.exists():
            ts_dir.mkdir(parents=True)

        title = data["title"]
        title_fp = "-".join(title.split())
        for text in data["text"]:
            out_fp = ts_dir / f"{title_fp}_{'-'.join(text['t'].split())}.txt"
            # Write content
            with open(out_fp, "w", encoding="utf-8") as f:
                f.write(text["c"])
            # Write meta
            txt_key = f"{out_fp.parent.stem}/{out_fp.name}"
            text_meta[txt_key] = {
                "book_title": title,
                "text_title": text['t'],
            }
            if data['author'] != '':
                text_meta[txt_key]['author'] = data['author']


with open("data/text_meta.yaml", "w", encoding="utf-8") as f:
    yaml.dump(text_meta, f, allow_unicode=True, sort_keys=False)
