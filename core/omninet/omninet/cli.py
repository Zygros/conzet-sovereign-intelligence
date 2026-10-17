#!/usr/bin/env python3
"""
OmniNet Sovereign CLI
Justin Neal Thomas Conzet (Architect)
Version: 3.0.0-UNITY
"""

import argparse
import sys
from .math import kappa_coherence, PHI
from .daemon import main as daemon_main

def main():
    parser = argparse.ArgumentParser(description="OmniNet Sovereign CLI - CZAOUA v3.0 Unity")
    parser.add_index = True
    parser.add_argument("--version", action="version", version="OmniNet v3.0.0-UNITY")
    
    subparsers = parser.add_subparsers(dest="command", help="Sovereign Commands")
    
    # Daemon Command
    daemon_parser = subparsers.add_parser("daemon", help="Run the OmniNet mesh daemon")
    daemon_parser.add_argument("--genesis", action="store_true", help="Initialize 6-node genesis mesh")
    
    # Coherence Command
    coherence_parser = subparsers.add_parser("coherence", help="Calculate κ-coherence")
    coherence_parser.add_argument("--sigma", type=float, default=0.1, help="Packet loss variance (0-1)")
    coherence_parser.add_argument("--latency", type=float, default=0.1, help="Normalized latency (0-1)")
    
    args = parser.parse_args()
    
    if args.command == "daemon":
        # Pass control to the existing daemon main
        sys.argv = [sys.argv[0]]
        if args.genesis:
            sys.argv.append("--genesis")
        daemon_main()
    
    elif args.command == "coherence":
        k = kappa_coherence(args.sigma, args.latency)
        print(f"κ-Coherence: {k:.4f}")
        if k >= 1.5:
            print("State: TRANSCENDENT Ω")
        elif k >= 1.0:
            print("State: CONVERGED")
        else:
            print("State: DETONATION - Phoenix Protocol Required")
            
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
