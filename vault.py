# ============================================
# NECHE CODING AGENT - Vault (File Protection)
# ============================================
# This protects sensitive files like Paystack,
# Flutterwave configs from being touched by AI

import json
import os
from config import VAULT_FILE

def load_vault():
    """Load list of locked/protected files"""
    if not os.path.exists(VAULT_FILE):
        return []
    with open(VAULT_FILE, 'r') as f:
        return json.load(f)

def save_vault(locked_files):
    """Save locked files list"""
    with open(VAULT_FILE, 'w') as f:
        json.dump(locked_files, f, indent=2)

def lock_file(filepath):
    """Lock a file so AI cannot touch it"""
    vault = load_vault()
    if filepath not in vault:
        vault.append(filepath)
        save_vault(vault)
        print(f"🔒 LOCKED: {filepath} is now protected")
    else:
        print(f"⚠️ Already locked: {filepath}")

def unlock_file(filepath):
    """Unlock a file so AI can work on it"""
    vault = load_vault()
    if filepath in vault:
        vault.remove(filepath)
        save_vault(vault)
        print(f"🔓 UNLOCKED: {filepath}")
    else:
        print(f"⚠️ File was not locked: {filepath}")

def is_locked(filepath):
    """Check if a file is locked"""
    vault = load_vault()
    return filepath in vault

def show_vault():
    """Show all locked files"""
    vault = load_vault()
    if not vault:
        print("🔓 No files currently locked")
        return
    print("\n🔒 LOCKED FILES (AI cannot touch these):")
    for f in vault:
        print(f"   → {f}")