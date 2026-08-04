#!/usr/bin/env python3
"""
MUSTY - Educational Password Hash Cracker
-------------------------------------------
Dictionary-based hash cracker for learning purposes.
Use ONLY on hashes you own or have explicit permission to test
(e.g. your own test accounts, CTF challenges, TryHackMe/HackTheBox labs).

Supports: md5, sha1, sha256, sha512
"""

import argparse
import hashlib
import itertools
import string
import sys
import time

RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"

BANNER = f"""{RED}{BOLD}
 888b     d888 888     888  .d8888b. 88888888888 Y88b   d88P
 8888b   d8888 888     888 d88P  Y88b    888      Y88b d88P
 88888b.d88888 888     888 Y88b.         888       Y88o88P
 888Y88888P888 888     888  "Y888b.      888        Y888P
 888 Y888P 888 888     888     "Y88b.    888        d888b
 888  Y8P  888 888     888       "888    888       d88888b
 888   "   888 Y88b. .d88P Y88b  d88P    888      d88P Y88b
 888       888  "Y88888P"   "Y8888P"     888     d88P   Y88b
{RESET}{CYAN}          educational dictionary hash cracker{RESET}
"""

HASH_FUNCS = {
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
    "sha256": hashlib.sha256,
    "sha512": hashlib.sha512,
}


def hash_word(word: str, algo: str) -> str:
    return HASH_FUNCS[algo](word.encode()).hexdigest()


def analyze_strength(password: str) -> dict:
    """Unique feature: analyzes WHY a cracked password was weak."""
    length = len(password)
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)

    pool = 0
    if has_lower:
        pool += 26
    if has_upper:
        pool += 26
    if has_digit:
        pool += 10
    if has_symbol:
        pool += len(string.punctuation)

    entropy = length * (pool.bit_length() - 1) if pool else 0

    reasons = []
    if length < 8:
        reasons.append("too short (<8 chars)")
    if not has_upper:
        reasons.append("no uppercase letters")
    if not has_digit:
        reasons.append("no digits")
    if not has_symbol:
        reasons.append("no special characters")
    if password.lower() in ("password", "admin", "letmein", "welcome", "qwerty"):
        reasons.append("common dictionary word")
    if password.isdigit():
        reasons.append("numeric only")

    if entropy < 28:
        rating = "Very Weak"
    elif entropy < 36:
        rating = "Weak"
    elif entropy < 60:
        rating = "Moderate"
    else:
        rating = "Strong"

    return {
        "length": length,
        "entropy_bits": entropy,
        "rating": rating,
        "reasons": reasons or ["none — but it was still in the wordlist!"],
    }


def crack(target_hash: str, algo: str, wordlist_path: str, verbose: bool):
    target_hash = target_hash.strip().lower()
    start = time.time()
    attempts = 0

    try:
        with open(wordlist_path, "r", errors="ignore") as f:
            for line in f:
                word = line.rstrip("\n\r")
                if not word:
                    continue
                attempts += 1
                if verbose and attempts % 50000 == 0:
                    print(f"{YELLOW}...{attempts} words tried{RESET}", file=sys.stderr)
                if hash_word(word, algo) == target_hash:
                    elapsed = time.time() - start
                    print(f"\n{GREEN}{BOLD}[+] MATCH FOUND{RESET}")
                    print(f"{GREEN}    Password : {word}{RESET}")
                    print(f"    Attempts : {attempts}")
                    print(f"    Time     : {elapsed:.2f}s\n")

                    analysis = analyze_strength(word)
                    print(f"{CYAN}{BOLD}--- Strength Analysis ---{RESET}")
                    print(f"    Rating       : {analysis['rating']}")
                    print(f"    Length       : {analysis['length']}")
                    print(f"    Est. entropy : {analysis['entropy_bits']} bits")
                    print("    Weaknesses   :")
                    for r in analysis["reasons"]:
                        print(f"      - {r}")
                    return True
    except FileNotFoundError:
        print(f"{RED}[!] Wordlist not found: {wordlist_path}{RESET}")
        sys.exit(1)

    elapsed = time.time() - start
    print(f"\n{RED}[-] No match after {attempts} attempts ({elapsed:.2f}s){RESET}")
    return False


def main():
    print(BANNER)
    parser = argparse.ArgumentParser(
        prog="musty",
        description="MUSTY - educational dictionary-based hash cracker. "
                     "Only use on hashes you own or are authorized to test.",
    )
    parser.add_argument("-H", "--hash", required=True, help="Target hash to crack")
    parser.add_argument(
        "-a", "--algo", choices=HASH_FUNCS.keys(), default="md5",
        help="Hash algorithm (default: md5)"
    )
    parser.add_argument(
        "-w", "--wordlist", required=True,
        help="Path to wordlist file (e.g. rockyou.txt)"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="Show progress every 50,000 attempts"
    )
    args = parser.parse_args()

    print(f"{CYAN}[*] Algorithm : {args.algo}{RESET}")
    print(f"{CYAN}[*] Wordlist  : {args.wordlist}{RESET}")
    print(f"{CYAN}[*] Target    : {args.hash}{RESET}\n")

    crack(args.hash, args.algo, args.wordlist, args.verbose)


if __name__ == "__main__":
    main()
