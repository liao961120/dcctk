import json
from pathlib import Path


with open("tier1.jsonl") as f:
    for line in f:
        data = json.loads(line)
        ts = data["dynGroup"][0]

        ts_dir = Path(f"data/{str(ts).zfill(2)}/")
        if not ts_dir.exists():
            ts_dir.mkdir(parents=True)

        title = data["title"]
        for text in data["text"]:
            with open(ts_dir / f"{title}-{text['t']}.txt", "w", encoding="utf-8") as f:
                f.write(text["c"])
