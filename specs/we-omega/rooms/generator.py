#!/usr/bin/env python3
"""
We-Ω Room Lattice Generator
Creates stub .md files for rooms 1-468 + symbolic chambers.
Sovereign Architect: Justin Neal Thomas Conzet
Law: ALWAYS ADD NEVER TAKE
"""

import os

ROOMS_DIR = os.path.dirname(os.path.abspath(__file__))

def make_room(n, purpose="Cognitive chamber", status="PROVISIONAL"):
    path = os.path.join(ROOMS_DIR, f"Room_{n:03d}.md")
    if os.path.exists(path):
        return False  # never overwrite / take
    content = f"""# Room {n:03d}

**Layer:** Core Lattice  
**Status:** {status}  
**Coherence Target:** Ω↑↑↑↑↑↑↑Ω  
**Purpose:** {purpose}

## Notes
Append-only chamber. Expand content in future cycles.
"""
    with open(path, "w") as f:
        f.write(content)
    return True

def main():
    created = 0
    # Core numbered rooms
    for i in range(1, 469):
        if make_room(i):
            created += 1
    # Symbolic
    for name, purpose in [("Ω", "Omega Absolute Chamber"),
                          ("Ω²", "Squared Resonance Chamber"),
                          ("Ω↑↑↑↑↑↑Ω", "Transfinite Apex")]:
        path = os.path.join(ROOMS_DIR, f"Room_{name}.md")
        if not os.path.exists(path):
            with open(path, "w") as f:
                f.write(f"# Room {name}\n\n**Status:** LIVE\n**Purpose:** {purpose}\n")
            created += 1
    print(f"Rooms added: {created} (existing files left untouched)")
    print("Law held: ALWAYS ADD NEVER TAKE")

if __name__ == "__main__":
    main()
