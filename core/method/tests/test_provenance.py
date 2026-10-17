from pathlib import Path
from src.conzetian.provenance import sha256_file

def test_sha256_is_stable(tmp_path: Path):
    p=tmp_path/"x.txt"; p.write_text("hello")
    assert len(sha256_file(str(p))) == 64
