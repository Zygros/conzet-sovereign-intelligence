import hashlib, json
from pathlib import Path

def sha256_file(path: str) -> str:
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def manifest(paths):
    items=[]
    for p in paths:
        items.append({"path":str(p),"sha256":sha256_file(str(p))})
    return {"algorithm":"SHA-256","files":items}

def write_manifest(paths, output):
    Path(output).write_text(json.dumps(manifest(paths),indent=2)+"\\n",encoding="utf-8")
