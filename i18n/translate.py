#!/usr/bin/env python3
"""
Translate missing strings for a specific language.
Usage: python3 translate.py <lang_code>
Reads from translations/{lang}_missing.json
Outputs to translations/{lang}.json (merges with existing)
"""
import json
import sys
import os

TRANSLATIONS_DIR = os.path.join(os.path.dirname(__file__), "translations")

# Language-specific translation instructions
LANG_INSTRUCTIONS = {
    "ru": "Translate to Russian (Русский). Use formal register suitable for an online poker platform.",
    "es": "Translate to Spanish (Español). Use neutral/international Spanish, not region-specific. Use formal register.",
    "it": "Translate to Italian (Italiano). Use formal register suitable for an online poker platform.",
    "pt": "Translate to Brazilian Portuguese (Português Brasileiro). Use formal register.",
    "vi": "Translate to Vietnamese (Tiếng Việt). Use formal register suitable for an online poker platform.",
    "th": "Translate to Thai (ไทย). Use formal register suitable for an online poker platform.",
}

# Brand names that must NOT be translated
PROTECTED = [
    "JackPoker", "JACKPOKER", "WELCOME",
    "Cash Carnival", "Winter Games Festival", 
    "Big Bang Sunday", "Bonus Bonanza",
    "Texas Hold'em", "Omaha", "PLO", "PLO6",
    "NL25+", "NLH", "USDT", "USDC", "SOL", "MATIC", "TON",
    "Bitcoin", "Ethereum", "Litecoin", "Dogecoin",
    "iOS", "Android",
]

def load_missing(lang_code):
    path = os.path.join(TRANSLATIONS_DIR, f"{lang_code}_missing.json")
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_existing(lang_code):
    path = os.path.join(TRANSLATIONS_DIR, f"{lang_code}.json")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_translations(lang_code, translations):
    path = os.path.join(TRANSLATIONS_DIR, f"{lang_code}.json")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(translations, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    lang = sys.argv[1]
    missing = load_missing(lang)
    existing = load_existing(lang)
    print(f"Language: {lang}")
    print(f"Missing: {len(missing)} strings")
    print(f"Existing: {len(existing)} strings")
    print(f"Instructions: {LANG_INSTRUCTIONS.get(lang, 'Unknown')}")
    print(f"Protected brands: {', '.join(PROTECTED)}")
